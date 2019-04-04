// ssyncer.c
// 20181122
//
//
//

# include <sys/types.h>
# include <sys/stat.h>
# include <unistd.h>
# include <string.h>
# include <stdio.h>

struct stat get_mata(char *dir);
int main(int ar, char * av) {
// get_meta(av) ;
  printf("%ld",sizeof(stat));
  return 0;

}


struct stat get_mata(char *dir){
  return stat(dir, sizeof(stat));
}
