/*Maggie Cao
Program for ignoring SIGUP and SIGQUIT signals then executing another program
and sending output of this program to a file called nohup.out
gcc my_nohup.c -o my_nohup
gcc testsim -o testsim
./my_nohup testsim 5 10
*/
#include <unistd.h>   
#include <stdio.h>    
#include <stdlib.h>
#include <signal.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include <fcntl.h>
#define MAX 50

/*the standard output of the new program will be written to nohup.out.*/
char **split(char*);

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

int main(int argc, char **argv){

	/*checks for inaccurate entries: my_nohup testsim 5 10
	* testsim is the program to be executed with command line arg 5 10*/
	if (argc!=4 || argv[2] == NULL || argv[3] == NULL){
		fprintf(stderr, "Usage: my_nohup testsim sleeptime repeatfactor \n");
		exit(EXIT_FAILURE);
	}

	/*put actual command testsim 5 10 for exec separately into a cstring*/
	char *command=malloc(50*sizeof(char));
	int arg;
	for (arg=1; arg<argc;arg++){
		strcat(command,argv[arg]);
		strcat(command," ");
	}
	char **args=split(command);

	const mode_t mode= S_IRUSR | S_IWUSR; 

	const char *file="nohup.out";

	int openfd;
	
	if ((openfd=open(file,O_WRONLY | O_CREAT | O_TRUNC, mode))==-1){
		perror("couldn't create/open my_nohup.out");
		exit(EXIT_FAILURE);
	}

	if (isatty(STDOUT_FILENO)==1)
		dup2(openfd,STDOUT_FILENO);
	else if (isatty(STDERR_FILENO)==1){
		dup2(openfd,2);
		close(openfd);
	}

	/*ignore SIGHUP and SIGQUIT via sigaction() and appropriate macros
	 *int sigaction(int signum, const struct sigaction *act, struct sigaction *oldact);*/
	struct sigaction act_quit, act_sigup;

	/*Obtain the old disposition of SIGHUP*/
    if (sigaction(SIGHUP, NULL, &act_sigup) == -1) {
		perror("Could not obtain old disposition for SIGHUP");
		exit(EXIT_FAILURE);
	}
	
	//If the dispsoition was the default (termination) change it to ignore
    if (act_sigup.sa_handler == SIG_DFL) {
    	act_sigup.sa_handler = SIG_IGN;
        if (sigaction(SIGHUP, &act_sigup, NULL) == -1) {
        	perror("Could not ignore SIGHUP");
	      	exit(1);
	   }
    } 
	else if (act_sigup.sa_handler != SIG_IGN) {  //A child could inherit ignore from parent
		fprintf(stderr,"Process inherited block of SIGHUP\n");
		exit(1);
	}

	/*Obtain the old disposition of SIGQUIT*/
	if (sigaction(SIGQUIT, NULL, &act_quit) == -1) {
		perror("Could not obtain old disposition for SIGQUIT");
		exit(EXIT_FAILURE);
	}

	if (act_quit.sa_handler == SIG_DFL) {
    	act_quit.sa_handler = SIG_IGN;
        if (sigaction(SIGQUIT, &act_quit, NULL) == -1) {
        	perror("Could not ignore SIGQUIT");
	      	exit(1);
	   }
    } 
	else if (act_quit.sa_handler != SIG_IGN) {  //A child could inherit ignore from parent
		fprintf(stderr,"Process inherited block of SIGQUIT\n");
		exit(1);
	}

	/*my_nohup executable would use exec to execute testsim with command line arg 5 and 10*/
	pid_t childpid, retcode;
	int retvalue;
	childpid=fork();

	/*child executes process testsim*/
	if (childpid==0){
		fprintf(stdout, "child process %d\n", getpid());

		/*execute the commands from commandline*/
		if (execvp(args[0], args)<0){
			perror("child failed the execvp command");
			exit(EXIT_FAILURE);
		}
		exit(1);
	}
	/*parent waits for child to finish*/
	if (childpid>0){
		retvalue = waitpid(childpid,&retcode,0);
		if (retvalue==-1){
			perror("wait for child failed \n");
			exit(EXIT_FAILURE);
		}	
		fprintf(stdout,"wait ret_val %d ret_code %d \n",retvalue, retcode);
	}

	exit(0);
}
