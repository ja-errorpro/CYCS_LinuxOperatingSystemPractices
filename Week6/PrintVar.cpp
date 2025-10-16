# include <unistd.h>
# include <stdio.h>
# include <stdlib.h>

int main( int argc, char** argv ) {

  int pid = getpid() ;

  printf( "My pid is : %d\n", pid ) ;

  int ppid = getppid() ;

  printf( "My parent pid is : %d\n", ppid ) ;

  for ( int i = 2 ; i <= argc ; i++ ) {

    char * val = getenv( argv[i-1] ) ;
    printf( "%s : %s\n", argv[i-1], ( val == NULL ) ? "" : val  ) ;

  } // for every argument specified by the user on the command line when invoking this executable

  printf( "=== Done - PrintVar. ===\n" ) ;

} // main()

