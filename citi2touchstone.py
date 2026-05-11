#!/usr/bin/env python3
"""Convert a CITIFILE (.d1/.d2) to Touchstone (.s1p/.s2p) format using scikit-rf.

Automatically detects 1-port vs 2-port data from the DATA headers in the file.
"""

import argparse
import re
import numpy as np
import skrf as rf


def parse_citifile(filepath):
    """Parse a CITIFILE and return frequency array (Hz), S-parameter dict, and port count.

    Returns:
        frequencies: 1-D array of frequency points in Hz
        s_params:    dict mapping (row, col) -> complex array, e.g. {(1,1): ..., (2,1): ...}
        n_ports:     number of ports (1 or 2)
    """
    seg_list = []
    in_seg = False

    # First pass: collect DATA declarations and segment info
    data_keys = []          # ordered list of (row, col) tuples
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"DATA\s+S\[(\d+),(\d+)\]\s+RI", line)
            if m:
                data_keys.append((int(m.group(1)), int(m.group(2))))
            if line == "SEG_LIST_BEGIN":
                in_seg = True
                continue
            if line == "SEG_LIST_END":
                in_seg = False
                continue
            if in_seg and line.startswith("SEG"):
                parts = line.split()
                seg_list.append((float(parts[1]), float(parts[2]), int(parts[3])))

    if not data_keys:
        raise ValueError("No DATA S[i,j] RI declarations found in CITIFILE")

    n_ports = max(max(r, c) for r, c in data_keys)

    # Second pass: read data blocks in order (one BEGIN/END block per DATA declaration)
    s_params = {}
    block_idx = 0
    in_data = False
    real_vals, imag_vals = [], []

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == "BEGIN":
                in_data = True
                real_vals, imag_vals = [], []
                continue
            if line == "END":
                in_data = False
                key = data_keys[block_idx]
                s_params[key] = np.array(real_vals) + 1j * np.array(imag_vals)
                block_idx += 1
                continue
            if in_data:
                parts = line.split(",")
                real_vals.append(float(parts[0]))
                imag_vals.append(float(parts[1]))

    # Build frequency array from segments
    freq_arrays = [np.linspace(fs, fe, n) for fs, fe, n in seg_list]
    frequencies = np.concatenate(freq_arrays) if len(freq_arrays) > 1 else freq_arrays[0]

    return frequencies, s_params, n_ports


def citi_to_touchstone(input_path, output_path=None):
    """Convert CITIFILE to Touchstone format (.s1p or .s2p), auto-detected."""
    frequencies, s_params, n_ports = parse_citifile(input_path)
    n_freq = len(frequencies)

    ext = f".s{n_ports}p"
    if output_path is None:
        output_path = input_path.rsplit(".", 1)[0] + ext

    freq = rf.Frequency.from_f(frequencies / 1e9, unit="GHz")

    # Build the S-matrix: shape (n_freq, n_ports, n_ports)
    s = np.zeros((n_freq, n_ports, n_ports), dtype=complex)
    for (row, col), data in s_params.items():
        s[:, row - 1, col - 1] = data

    ntwk = rf.Network(frequency=freq, s=s, z0=50)
    ntwk.write_touchstone(output_path, form="ri")

    params = ", ".join(f"S{r}{c}" for r, c in sorted(s_params))
    print(f"Detected {n_ports}-port data ({params})")
    print(f"Converted {input_path} -> {output_path}")
    print(f"  {n_freq} points, {frequencies[0]/1e6:.1f} – {frequencies[-1]/1e6:.1f} MHz")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert CITIFILE to Touchstone (.s1p / .s2p), auto-detected"
    )
    parser.add_argument("input", help="Input CITIFILE path")
    parser.add_argument("-o", "--output", help="Output path (default: same name with .s1p/.s2p)")
    args = parser.parse_args()
    citi_to_touchstone(args.input, args.output)
