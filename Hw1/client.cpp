# include <sys/types.h>
# include <sys/socket.h>
# include <netinet/in.h>
# include <arpa/inet.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>

# define PORT_TO_USE 1100
# define SOCKET_DEBUG false

bool NOT( bool proposition ) {
  return ! proposition ;
} // NOT()

void DP( bool printIt, char * msg ) {
  if ( printIt )
    printf( "%s\n", msg ) ;
} // DP()

int main( void ) {

  int bytesRead, callConnectionFD;
  char* msgToSend = (char *) "Hello from client";
  char msgReceived[1024] = { 0 };

  struct sockaddr_in aSocket;  // THE fax machine
  int addressConversionResult; // 1 : success ; 0 : source not a string ; -1 : errorNo
  int aSocketFileFD = socket( PF_INET, SOCK_STREAM, IPPROTO_TCP ) ;  // creation of a paper

  if ( -1 == aSocketFileFD ) {
    perror( "cannot create socket" ) ;
    exit( EXIT_FAILURE );
  } // if socket creation error

  // // Geekforgeeks :
  // int sock = 0 ;
  // if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
  //     printf("\n Socket creation error \n");
  //     return -1;
  // }

  // Tediously clean the fax machine and set it up for making calls

  memset( &aSocket, 0, sizeof( struct sockaddr_in ) ) ;

  aSocket.sin_family = AF_INET;
  aSocket.sin_port = htons( PORT_TO_USE ); // port : PORT_TO_USE

  // prepare the fax machine for making a very specific connection (where to call to)

  addressConversionResult = inet_pton( AF_INET, "127.0.0.1", &aSocket.sin_addr );  
                                                // was : "192.168.1.3"

  if ( addressConversionResult < 0 ) {  // was : 0 > addressConversionResult
    perror( "error: first parameter is not a valid address family" );
    close( aSocketFileFD );
    exit( EXIT_FAILURE );
  } // if

  else if ( addressConversionResult == 0 ) { // was : 0 == addressConversionResult
    perror("char string (second parameter does not contain valid ipaddress");
    close( aSocketFileFD );
    exit( EXIT_FAILURE );
  } // else if

  else // addressConversionResult > 0
    ;  // OK

  DP( SOCKET_DEBUG, (char *) "Now we can try to make a connection attempt." ) ;

  // put the paper and the fax machine in a bundle and try to make a connection attempt

  // // kshuang version
  // if ( -1 == connect( aSocketFileFD, ( const struct sockaddr * ) &aSocket, sizeof( struct sockaddr_in ) ) ) {
  //   perror( "connect() failed" ) ;
  //   close( aSocketFileFD );
  //   exit( EXIT_FAILURE );
  // } // if the connection attempt failed

  // Geeksforgeeks version
  if ( ( callConnectionFD
         = connect( aSocketFileFD, 
                    ( struct sockaddr* ) &aSocket,
                    sizeof( aSocket )
                  )
       ) < 0 
     ) {
    printf( "\nThe attempt to connect to the server via port %d Failed \n", PORT_TO_USE ) ;
    return -1;
  } // if connect() failed

  DP( SOCKET_DEBUG, (char *) "Connection attempt succeeded." ) ;

  /* perform read write operations ... */

  send(aSocketFileFD, msgToSend, strlen(msgToSend), 0);
  // DP( SOCKET_DEBUG, (char *) "Hello message sent to server." );

  // bytesRead = read( aSocketFileFD, msgReceived, 1024 );

  if ( SOCKET_DEBUG ) 
    printf( "Message received from server : %s\n", msgReceived );

  // close( aSocketFileFD ); 
  // Geeksforgeeks says 'close' the one returned by 'connect' (and not 'aSocketFileFD')
  close( callConnectionFD ) ;

  shutdown( aSocketFileFD, SHUT_RDWR );

  return 0;

} // main()
