/* ls01.c -- list file details.
 * this is a test program.
 * Mar 8th, 2017
 */

#include<stdio.h>
#include<dirent.h>
#include<stdlib.h>	/* To import exit(int n), otherwise pop a varning. */

void list(char *);
int main(int ac, char *av[])
{
	if ( ac == 1 )
		list(".");
	else 
		while ( --ac )
			list(*++av);

	return 0;

}

void list(char *dir)
/* list a directory */
{
	DIR *od;
	struct dirent *sd;
	if (( od = opendir(dir)) == NULL ){
		fprintf(stderr, "Unable to access %s.\n", dir);
		exit(1);  // need include stdlib.h, otherwise pop a warning.
	}
	while (( sd = readdir(od)) != NULL )
		printf("%s\n", sd->d_name);
	
	closedir(od);
}
