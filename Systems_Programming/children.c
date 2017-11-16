#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>

#define MODE r   /*read mode*/
#define MAX 100 /*max number of data lines*/

char** split(char*);
void execute(char**, int);

char** split(char *dataline){

	char **argv = calloc( MAX, sizeof(char*) );
	
	/*allocate space for each string*/
	int j;
	for (j=0; j<MAX; j++)
		argv[j]=malloc(MAX*(sizeof(char)));

	char *delim= " \t\n";

	int i=0;
	argv[i]= strtok(dataline, delim);

	while (argv[i]!=NULL){
		//printf("split: arguments=%s i=%d \n", argv[i],i);
		i++;
		argv[i] = strtok(NULL, delim);
	}
	
	argv[i+1]=NULL;

	return argv;
}

/*execute, sleep, repeat factor*/
int execute(char **filedata, int start){

	argv=split(filedata[start]);

	if ( (execvp(argv[0],argv)) < 0){ 
		perror ("child failed the execvp command");
		return -1;
	}

	int i;
	/*argv[1] is the repeat factor*/
	for (i=0; i<argv[1]; i++){
		if ( (execvp(argv[0],argv)) > 0)
			sleep(argv[1]);
	}

	return 0;
}

int main(int argc, int *argv[]){

	/*pr_limit, specified at command line, is the max num of children
	allowed to be run at a time*/
	int pr_limit=argv[1];
	int pr_count=0;

	pid_t *child_pid;
	pid_t child_processID;
	int status; /*status of child*/

	FILE *openfileptr;
	char* filedata[MAX]; 
	
	if (pr_limit <= 0 || pr_limit >= 50){
		perror("input of children is too small or too large");
		exit(1);
	}
	
	/*allocate a dynamic array for child processes*/
	if (child_pid==NULL){
		if ( child_pid=calloc(pr_limit,sizeof(pid_t)) == NULL){
			perror("Can't allocate childpid[pr_limit] ");
			return NULL;
		}
	}

	/*execution of command line opens a data file
	runsim 2 < data*/	
	/*argv[3] is the name of the file specified at command line*/	 
	if ( (openfileptr=fopen(argv[2],MODE)) == NULL ){
		perror("Failed to file for reading");
		return -1;
	}

	int i=0; /*number of lines*/
	/*get data from file and close the file*/
	while ( (fgets(filedata[i],10,openfileptr)) != NULL && i < MAX)
		i++;

	if ( fclose(openfileptr) == EOF )
		perror("Failed to close file descriptor");
	
	int start=0; 
	while (start < i+1){
		while (pr_count<=pr_limit){//pr_count is at 0, pr_limit is ex: 2 child proc
			
			/*fork a child process*/
			if ( child_pid[pr_count] == -1){
				perror("Cannot fork child number: %d", i);
				exit (EXIT_FAILURE);
			}

			if ( (child_pid[pr_count] = fork()) == 0) ){
				printf("child's pid = %d at i: %d, parent's pid = %d \n", getpid(), i, getppid());
					 /*start: where the current line is after child is done processing*/
					if ( execute(filedata, start) == 0){
						pr_count++; /*create more children*/
						start++;
					}
			}

			/*parent wait for child to finish then decrement pr_count when finished*/
			if ( (child_pid[pr_count]=fork()) > 0){
				/*pid_t waitpid(pid_t pid, int *status, int options) WNOHANG returns immediately*/
				if ( (child_processID=waitpid(childpid[pr_limit],&status,WNOHANG)) > 0) 
					pr_count--;
			}
			
			/*make sure child is terminated normally*/
			if (WIFEXITED(status))
				printf("child at i %d exited with status %d", i , WIFEXITED(status));
		}
	}
	
	int rem_child;
	/*wait for the remaining children after EOF: there should be at most pr_limit left*/
	for (rem_child=0; rem_child<pr_limit; rem_child++)
		waitpid(-1,&status,0); //wait for any child
	
	exit (0);
		
}

