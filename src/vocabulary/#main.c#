#include <stdio.h>
#include <stdlib.h>

int main(void)
{
  char buffer;
  
  FILE *input = fopen("/home/zuckram/Desktop/Japanese/tools/sentences.txt", "r");

  if(input == NULL) {
    printf("error\n");
    return 1;
  }

  int count = 1;
  
  while(fread(&buffer, sizeof(char), 1, input) != 0) {
    count = count + 1;
  }
  rewind(input);
  
  char *voc = malloc(sizeof(char) * count);

  fread(voc, sizeof(char), count - 2, input);

  printf("%s\n", voc);
  
  fclose(input);
}
