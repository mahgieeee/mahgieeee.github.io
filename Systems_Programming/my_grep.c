/*Maggie Cao*/
/*CISC3350*/
/*April 20, 2017*/
/*Assignment #4*/
/*Searching files using pthreads
The program doesn't print out all of the lines in the files that has the pattern because
there is a segmentation fault in the program. I can't seem to find where the memory is 
leaking. I know that function searchfile is supposed to return number of lines, but
adding that piece of code interfers with the output of the program. Thus I commented 
those lines of code out (as well as the total number of matched lines in main)
Updated: The segmentation fault was because I allocated not enough lines for a file, 
i shouldn't allocate all the lines at once for a file, but make it read a line at a time
The code mostly works, except that the numoflines return value for searchfile isn't
correctly passed back into main's function call*/

#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define NUMFILES 50

void *searchfile(void *);

/*globally accessible variables and a mutex*/
	char *pattern;
	pthread_t fileThreadsCall[NUMFILES];
	pthread_mutex_t mutexfile=PTHREAD_MUTEX_INITIALIZER;

/*Each thread runs this function via a shared resource 
using mutex synchronization*/
void *searchfile(void *filename){
	
	FILE *fileptr;	
	char *tmpfilename=filename;
	//fprintf(stdout,"print from searchfile %s \n", tmpfilename);

	char line[1000];
	
	if ( (fileptr=fopen(tmpfilename,"r")) == NULL){ 
		perror("Thread failed to open file");
		exit (EXIT_FAILURE);
	}

	void *match;
	/*for return value to return num of lines with pattern*/
	int numMatchlines=match;
	numMatchlines=0;

	while ( !(feof(fileptr)) ){
		fgets(line,1024,fileptr); /*read one line at a time*/
		strstr(line,pattern); 
		if ((strstr(line,pattern))!= NULL){
			/*synchronization is used to access the shared resource, standard output*/
			pthread_mutex_lock(&mutexfile);
			/*can print now once thread gets the lock*/
			fprintf(stdout,"Filename %s at Line: %s \n", tmpfilename, line);
			pthread_mutex_unlock(&mutexfile);
			numMatchlines++;
		}
	}

	/*close the file after done*/
	if ( fclose(fileptr) == EOF )
		perror("Failed to close file descriptor");

	printf("File: %s has a total number of %d matchlines \n", tmpfilename, numMatchlines);
	pthread_exit((void*)filename);	
	return numMatchlines;	
}



int main(int argc, char**argv){

	/*minimum of two arguments for program to work*/
	if (argc<2){
		errno=EINVAL;
		exit (EXIT_FAILURE);
	}
		
	int fileNum=argc-2;//argc-2 is the number of files being searched
	pattern=argv[1];

	/*main thread calls pthread_create() for each file to be searched 
	passing the filename as the arg.	A cast will be needed*/
	void *status;
	pthread_attr_t attr;

	void *filename; 

	char **files=calloc(fileNum, sizeof(char*));
	int k;
	for (k=0; k<fileNum; k++)
		files[k]=malloc(fileNum*sizeof(char));

	//store argv[] files separately from pattern 
	int numarg;
	for (numarg=0; numarg<fileNum; numarg++)
		files[numarg]=filename;//(char*)filename;
	
	int y;
	for (y=0; y<fileNum; y++)
		files[y]=argv[2+y];
	
	
	pthread_mutex_init(&mutexfile, NULL); //second arg is attr

	int i;
	/*void *pthreadret;
	int totalnumMatchlines=pthreadret;
	totalnumMatchlines=0;*/
	
	for (i=0; i<fileNum ; i++){
		if ( (pthread_create(&fileThreadsCall[i],NULL,searchfile,(void*)files[i])) != 0)
			perror("Cannot create pthread \n");
		//pthreadret=searchfile(files[j]);
		//totalnumMatchlines+=pthreadret;
		fprintf(stdout,"Filename %s \n", files[i]);
	}


	//printf("pthreadret %d \n", pthreadret);

	/*main thread joins all the other threads, storing their return values*/
	int j;
	int threadretval[fileNum];
	for (j=0; j<fileNum; j++){
		if ( (threadretval[j]=pthread_join(fileThreadsCall[j], &status)) != 0) //not successful
			perror("pthread_join doesn't work \n");
		fprintf(stdout, "Thread join successfully with return value: %d \n", threadretval[j]);
	}

	/*when all the other threads have terminated, the main() thread writes to standard output 
	the number of matching lines in total*/
	//fprintf(stdout, "Total Number of matching lines: %d \n", totalnumMatchlines);

	pthread_mutex_destroy(&mutexfile);
	pthread_exit(NULL);
}
