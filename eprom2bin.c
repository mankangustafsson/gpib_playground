#include <stdio.h>
#include <stdint.h>

int main(int argc, char* argv[])
{
  if (argc != 4) {
    fprintf(stderr, "Usage: %s infile1 infile2 outfile\n", argv[0]);
    return -1;
  }

  FILE* inFile1 = fopen(argv[1], "r");
  if (inFile1 == NULL) {
    fprintf(stderr, "Failed to open infile1: %s", argv[1]);
    return -1;
  }

  int exitCode = -1;
  
  FILE* inFile2 = fopen(argv[2], "r");
  if (inFile2 == NULL) {
    fprintf(stderr, "Failed to open infile1: %s", argv[2]);
    goto E1;
  }

  FILE* outFile = fopen(argv[3], "w");
  if (outFile == NULL) {
    fprintf(stderr, "Failed to open outfile: %s", argv[3]);
    goto E2;
  }
  
  uint8_t inData1[32 * 1024];
  if (fread(inData1, sizeof(inData1), 1, inFile1) != 1) {
    fprintf(stderr, "Failed to read infile1\n");
    goto E3;
  }

  uint8_t inData2[32 * 1024];
  if (fread(inData2, sizeof(inData2), 1, inFile2) != 1) {
    fprintf(stderr, "Failed to read infile2\n");
    goto E3;
  }
  
  uint8_t outData[64 * 1024];
  uint8_t* r1 = inData1;
  uint8_t* r2 = inData2;
  uint8_t* w = outData;
  for (int n = 0; n < sizeof(inData1); ++n) {
    *w++ = *r1++;
    *w++ = *r2++;
  }

  if (fwrite(outData, sizeof(outData), 1, outFile) != 1) {
    fprintf(stderr, "Failed to write outfile\n");
    goto E3;
  }
  exitCode = 0;
 E3:
  fclose(outFile);
 E2:
  fclose(inFile2);
 E1:
  fclose(inFile1);
  return exitCode;
}
