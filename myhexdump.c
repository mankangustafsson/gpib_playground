#include <stdio.h>
#include <stdint.h>

int main(int argc, char* argv[])
{
  if (argc != 2) {
    fprintf(stderr, "Usage: %s infile\n", argv[0]);
    return -1;
  }

  FILE* inFile = fopen(argv[1], "r");
  if (inFile == NULL) {
    fprintf(stderr, "Failed to open infile: %s", argv[1]);
    return -1;
  }

  int exitCode = -1;
  uint16_t inData[8/2 * 1024];
  if (fread(inData, sizeof(inData), 1, inFile) != 1) {
    fprintf(stderr, "Failed to read infile\n");
    goto E1;
  }

  uint16_t* r = inData;
  for (int n = 0; n < sizeof(inData)/sizeof(uint16_t); ++n) {
    uint16_t data = *r++;
    uint16_t be = ((data & 0xff) << 8) | ((data & 0xff00) >> 8);
    int16_t datas = ~data + 1;
    int16_t bes = ~be + 1;
    printf("0x%04x,%6d, %6u, %6d, %6u\n",
           2*n, datas, data, bes, be);
  }
  exitCode = 0;
 E1:
  fclose(inFile);
  return exitCode;
}
