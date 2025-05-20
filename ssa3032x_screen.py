from Devices import Device
from Lab import Lab

import argparse
from datetime import datetime
from PIL import Image
import io

parser = argparse.ArgumentParser()
parser.add_argument("pngfile", metavar="output_file", help="file to save screenshot to")
parser.add_argument("-t", action="store_true", help="adds timestamp prefix to filename")
args = parser.parse_args()

# print(args)

dev = Lab.connectByType(Device.Type.SPECTRUM_ANALYZER, hint="SSA3032")
if dev is None:
    exit(1)

print("Fetching BMP data...", end="", flush=True)
dev.write(":HCOP:SDUM:DATA?")
# BMP: file header size, image header size, pixel data and message termination
dataSize = 14 + 40 + 1024 * 600 * 3 + 1
data = dev.read_raw(dataSize)
print("done.")

# data = dev.query_binary_values(':HCOP:SDUM:DATA?',
#                               datatype='B',
#                               container=bytearray,
#                               header_fmt='empty',
#                               is_big_endian=False,
#                               chunk_size=102400,
#                               expect_termination=False)

filename = args.pngfile
if args.t:
    filename = datetime.now().strftime("%Y-%m-%d_%H%M%S-") + filename
if not filename.lower().endswith(".png"):
    filename += ".png"
print(f"Saving PNG data to file {filename}...", end="", flush=True)
try:
    with Image.open(io.BytesIO(data)) as im:
        im.save(filename)
except OSError:
    print("failed to save file, {filename}")
print("done.")
dev.close()
