/****************************************************************************
Maggie Cao
program for executing child processes and wait for child under pr_limit time
gcc runsim.c -o runsim
gcc testsim.c -o testsim
./runsim 2 datafile
****************************************************************************/
#define _GNU_SOURCE
#include <stdio.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#define MAX 50

char **split(char *);

/*splits command line into a string of character arrays*/
char **split(char *input){

	char **argv = calloc( MAX, sizeof(char*) );//argv is a char*pointer to char[0]...char[n]
	
	/*allocate space for each string*/
	int j;
	for (j=0; j<MAX; j++)
		argv[j]=malloc(MAX*(sizeof(char)));

	char *delim= " \t\n";

	int i=0;
	argv[i]= strtok(input, delim);

	while (argv[i]!=NULL){
		i++;
		argv[i] = strtok(NULL, delim);
	}
	
	argv[i+1]=NULL;

	return argv;
}


int main(int argc, char *argv[]){

	/*pr_limit, specified at command line, is the max num of children allowed to be run at a time*/
	int pr_limit=atoi(argv[1]);
	if (pr_limit <= 0 || pr_limit >= 50){
		perror("input of children is too small or too large");
		exit(1);
	}

	/*execution of command line opens a data file with read permission: runsim 2 datafile 
	 *argv[2] is the name of the file specified at command line*/ 
	//char *filename=argv[2];
	
	/*filedata stores command line arg from file while it is opened*/
	char **filedata =calloc(MAX, sizeof(char*));
	/*delimitfiledata stores the delimited data from filedata*/
	char **delimitfiledata;//=calloc( MAX, sizeof(char*) );

	int j, i=0;
	for (j=0; j<MAX; j++){
		filedata[j]=malloc(MAX*(sizeof(char)));
		//delimitfiledata[j]=malloc(MAX*(sizeof(char)));
	}
	
	FILE *fptr=fopen(argv[2],"r");
	if (fptr == NULL){
		perror("Failed to file for reading");
		exit (EXIT_FAILURE);
	}
	
	int retcode, pr_count=0;
	int child_pid[MAX], ret_val;
	int l;

	while (!(feof(fptr))){
		fgets(filedata[i],1024,fptr);
		delimitfiledata=split(filedata[i]);
	
		if (pr_count==pr_limit){
			wait(&retcode);
			pr_count--;
		}

		/*child executes*/
		if ((child_pid[i]=fork())==0){ 
			fprintf(stdout, "proc %d data: %s %s %s at i: %d \n", getpid(), 
			delimitfiledata[0],  delimitfiledata[1], delimitfiledata[2],i);
			if (execvp (delimitfiledata[0], delimitfiledata) < 0){ 
				perror ("child failed the execvp command");
				exit(EXIT_FAILURE);
			}
			exit(errno);
		}

		pr_count++;
		i++;
		fprintf(stdout, "prcount: %d \n", pr_count);
		/*parent waits for child*/
		for (l=0; l<pr_limit;l++){
			if (child_pid[l]>0){
				if ((ret_val=waitpid(-1,&retcode,WNOHANG))>0){
					fprintf(stdout,"parent successfully waited for %d, whose ret_val %d ret_code %d\n",getpid(),ret_val, retcode);
					pr_count--;
				}
				//if ( ret_val== 0)
				//	perror("child still running");
				if (ret_val==-1){
					perror("wait for child failed");
					exit(EXIT_FAILURE);
				}
			}
		}
		
	}

	if (fclose(fptr)==EOF)
		perror("failed to close file descriptor");
	
	/*wait for the remaining (any) children to terminate*/
	int r;
	for (r=0; r<20; r++){
		ret_val = wait(&retcode);
		if (ret_val>0)
			fprintf(stdout,"wait for remaining children ret_val %d ret_code %d\n",ret_val, retcode);
	}

	free(filedata);
	free(delimitfiledata);
	exit(0);
}


