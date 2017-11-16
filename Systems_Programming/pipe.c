#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>

/*make childpid static since popen and pclose shares this*/
static pid_t childpid;
/*max number of arguments*/
int MAX=10;

char** split(char*);
FILE *popen(const char *,const char *);
int pclose(FILE *);

/*
splits command line into a string of character arrays
cmd=split[0]
char *cmd="ls"
char *argv[3];
argv[0]="ls"
argv[1]="-la"
argv[2]=NULL;
*/

char** split(char *input){

	char **argv = calloc( MAX, sizeof(char*) );
	
	/*allocate space for each string*/
	int j;
	for (j=0; j<MAX; j++)
		argv[j]=malloc(MAX*(sizeof(char)));

	char *delim= " \t\n";

	int i=0;
	argv[i]= strtok(input, delim);

	while (argv[i]!=NULL){
		//printf("split: arguments=%s i=%d \n", argv[i],i);
		i++;
		argv[i] = strtok(NULL, delim);
	}
	
	argv[i+1]=NULL;

	return argv;
}


/*
	opens pipe for parent and child (child executes command)
	parent waits for child to be done executing before returning
*/
FILE *popen(const char *command,const char *mode){

	char **argv;
	char *command1=malloc(12*sizeof(char));

	strcpy(command1,command);
	
	printf("command1: %s \n", command1);

	argv=split(command1);
	
 	/*test prints*/
	printf("popen: argv[0]: %s \n", argv[0]);
	printf("popen: argv[1]: %s \n", argv[1]);
	printf("popen: argv[2]: %s \n", argv[2]);

	/*fd[0] is for read, fd[1] is for write*/
	int fd[2]; 
	FILE *fptr;
	size_t lengthmode=strlen(mode); /*to make sure mode input is one character*/

	/*error checking for invalid input for mode*/
	if (*mode != 'r' && *mode != 'w' && lengthmode != 1){
		errno=EINVAL;
		return NULL;
	}

	
	if (pipe(fd) == -1){
		perror("Failed to create the pipe");
		return NULL;
	} 

	/*parent forks child*/
	childpid=fork();
	
	if ( childpid == -1){
		perror("Failed to fork child");
		return NULL;
	}

	/*parent writes into read input for child
	  write mode: parent closes read end of pipe and opens pipe[1] to write
	  read mode: parent closes write end of pipe and opens pipe[0] to read
	*/
	if (childpid>0){
		if (*mode == 'w'){
			close(fd[0]);
			if( (fptr=fdopen(fd[1],mode)) == NULL)
				perror("segfault");
			wait(NULL); /*Wait for child*/
		}
		else if (*mode == 'r'){
			close (fd[1]);
			if ( (fptr=fdopen(fd[0],mode)) == NULL)
				perror("segfault");
			wait(NULL); /*Wait for child*/
		}
	}

	/*child process*/
	if (childpid==0){
		if (*mode == 'w'){
			//parent closes read, child closes write, child takes in input from read pipe 	
			close (fd[1]);
			if (fd[0] != STDIN_FILENO){
				dup2(fd[0],STDIN_FILENO); /*redirects read input in write mode*/
				close (fd[0]);
			}
		}
		else if (*mode == 'r'){
			//parent closes write, child closes read, child takes in output from write pipe
			close (fd[0]);
			if ( fd[1] != STDOUT_FILENO){
				dup2(fd[1],STDOUT_FILENO);
				close (fd[1]);
			}
		}
		//after child redirects to input and output,runs exec command
		//the child will execute the file specified on the command line
		//reinterpret command argument using white space delimiter
		//execvp(const char *file,char *const argv[])

		if ( (execvp(argv[0],argv)) < 0){ 
				perror ("child failed the execvp command");
				exit(1);
		}
	}
	free(command1);
	return fptr;

}


/*
pclose closes a stream opened by popen() by using fclose, wait for the command to terminate
and returns the termination status of the process that was running the command
one error, pclose returns -1 and set errno to indicate the error: wait(),
waitpid(), popen
*/
int pclose(FILE *stream){
	int status; /*termination status of process*/
	
	/*popen was never called*/
	if (childpid<0){
		errno=EINVAL;
		return -1;
	}

	/*wait for child before closing stream
		use waitpid for status*/	
	while ( (waitpid(childpid,&status,0)) < 0)
		return -1;	
	
	/*close popen's stream*/
	if (fclose(stream) == EOF)
		return -1;

	return status;

}

int main(){

	FILE *fptr;
	char inputline[1024];
	
	/*get the input line*/
	printf("Type in command: ");
	fgets(inputline,1024,stdin);

	if ( (fptr = popen(inputline,"w")) == NULL){ 
		perror("popen failed");
		return 1; 
	}
	
	pclose(fptr);

	return 0;
}
