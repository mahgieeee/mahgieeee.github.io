/*
	Maggie Cao
	Uniq program prints out the uniq lines data from a file input using 
	delimiters and strcpy of the original buffer. Max buffer size for read is 
	1024 bytes.
*/
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define MAX 1024
#define MAXBUFFER 1024 //max number of bytes allowed to be read in a file 

char **split(char *);

/*splits char*buffer that was read into an array of strings*/
char **split(char *input){

	char **argv = calloc(MAX, sizeof(char*) );
	
	/*allocate space for each string*/
	int j;
	for (j=0; j<MAX; j++)
		argv[j]=malloc(MAX*(sizeof(char)));

	//char *delim= " \t\n";
	char *delim= "\n";
	int i=0;
	argv[i]= strtok(input, delim);

	while (argv[i]!=NULL){
		i++;
		argv[i] = strtok(NULL, delim);
	}

	argv[i+1]=NULL;

	return argv;
}
int main (int argc, char *argv[]){

    int fd, numread,writeread;
	char buffer[MAXBUFFER];
	fprintf(stdout,"usage: ./a.out file.txt \n");

    fd=open(argv[1],O_RDONLY);
    if (fd==-1){
		perror("can't open file");
            exit(EXIT_FAILURE);
    }
	
	
	int i=0;
	int newlines=0;
    while((numread=read(fd, buffer, sizeof(buffer))) != 0){
    	//Display the characters read
        writeread=write(1,buffer,numread);	
	}
	
	char *newbuffer=malloc(writeread*(sizeof(char)));
	strcpy(newbuffer,buffer);
	
	//fprintf(stdout, "new truncated string at bytesread length:\n%s", newbuffer);	

	char *newbuffer1=malloc(writeread*(sizeof(char)));
	strcpy(newbuffer1,buffer);

	/*find out number of lines in the file*/
	char *delim="\n";
	char *token;
	token=strtok(newbuffer1,delim);
	while (token!=NULL){
		newlines++;
		token=strtok(NULL,delim);
	}
	
	fprintf(stdout, "numlines total is %d \n", newlines);

	char **buffersplit=split(newbuffer);
	int k=0;
	/*prints uniq lines to standard output*/
	while (k<(newlines-1)){
		strstr(buffersplit[k], buffersplit[k+1]);
		if (strstr(buffersplit[k], buffersplit[k+1]) == NULL){
			write(1,buffersplit[k],strlen(buffersplit[k]));
			fprintf(stdout, "\n");
		}
		k++;
	}
			
	close(fd);
	free(buffersplit);
	free(newbuffer);
	free(newbuffer1);
    return 0;
}
