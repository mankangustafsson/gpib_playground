#include <stdio.h>
#include <stdint.h>

int main(int argc, char* argv[])
{
  if (argc != 3) {
    fprintf(stderr, "Usage: %s infile outfile\n", argv[0]);
    return -1;
  }

  FILE* inFile = fopen(argv[1], "r");
  if (inFile == NULL) {
    fprintf(stderr, "Failed to open infile: %s", argv[1]);
    return -1;
  }

  int exitCode = -1;
  
  FILE* outFile = fopen(argv[2], "w");
  if (outFile == NULL) {
    fprintf(stderr, "Failed to open outfile: %s", argv[2]);
    goto E1;
  }
  
  uint8_t inData[16 * 1024];
  if (fread(inData, sizeof(inData), 1, inFile) != 1) {
    fprintf(stderr, "Failed to read infile\n");
    goto E2;
  }
  
  uint8_t outData[8 *1024];
  uint8_t* r = inData;
  uint8_t* w = outData;
  for (int n = 0; n < sizeof(outData); ++n) {
    ++r;
    *w++ = *r++;
  }

  if (fwrite(outData, sizeof(outData), 1, outFile) != 1) {
    fprintf(stderr, "Failed to write outfile\n");
    goto E2;
  }
  exitCode = 0;
 E2:
  fclose(outFile);
 E1:
  fclose(inFile);
  return exitCode;
}
