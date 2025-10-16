# include <stdio.h>

extern char **environ ;    // alternatively, we can just use '# include <unistd.h> ;'

int main( int argc, char **argv ) {  
// some compilers allow a third argument >>char** envp<< which is not POSIX-compliant  
// # 謎之聲：what is 'POSIT-compliant'?

  for ( int i = 0 ; environ[i] != NULL ; i++ ) {

     printf( "environ[%d] : >>%s<<\n", i, environ[i] ) ;

     // printf( "envp[%d]    : >>%s<<\n", i, envp[i] ) ;

  } // for every environment variable-value pair (every 'NAME=VALUE' string) in environ[]

  return 0 ;

} // main()
