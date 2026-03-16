# include <sys/types.h>
# include <sys/socket.h>
# include <netinet/in.h>
# include <arpa/inet.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>

# define PORT_TO_USE 1100
#define SOCKET_DEBUG true

bool NOT( bool proposition ) {
  return ! proposition ;
} // NOT()

void DP( bool printIt, char * msg ) {
  if ( printIt )
    printf( "%s\n", msg ) ;
} // DP()

int main( void ) {

  struct sockaddr_in aSocket;    // a fax machine
  int addrlen = sizeof( aSocket );

  // the paper to be used by our fax machine
  int aSocketFileFD = socket( PF_INET, SOCK_STREAM, 0 ); // <domain>, <type>, <protocol>
      // Geeksforgeeks says : AF_LOCAL ; but NO!

  /* aSocketFileFD: socket descriptor, an integer (like a file-handle)
     domain: integer, 
       specifies communication domain. We use AF_LOCAL as defined in the POSIX 
       standard for communication between processes on the same host. For communicating  
       between processes on different hosts connected by IPV4, we use AF_INET and  
       AF_INET6 for processes connected by IPV6.
     type: communication type
       SOCK_STREAM: TCP (reliable, connection oriented)
       SOCK_DGRAM: UDP (unreliable, connectionless)
     protocol: 
       (Geeksforgeeks put 'IPPROTO_TCP' here) 
       Protocol value for Internet Protocol(IP), which is 0.  
       This is the same number which appears on protocol field in the IP header of a packet.
       ('man protocols' for more details)
   */

  int bytesRead ;  // -1 indicates "failure"

  int optionValue = 1 ;  // difficult to understand ; just let it be so for beginners
  char msgReceived[ 1024 ] = { 0 } ;
  char* msgToSend = (char * ) "Hello from server";

  if ( -1 == aSocketFileFD ) {
    perror( "Cannot create socket!!!" ) ;
    exit( EXIT_FAILURE ) ;
  } // if socket creation error

  // clean the fax machine and set it up for receiving calls

  memset( &aSocket, 0, sizeof( struct sockaddr_in ) ) ;

  /* Below helps in manipulating options for the socket referred by the file descriptor 
     aSocketFileFD. This is completely optional, but it helps in reuse of address and port. 
     Prevents error such as: “address already in use”.
  */
  if ( setsockopt( aSocketFileFD, 
                   SOL_SOCKET, 
                   SO_REUSEADDR | SO_REUSEPORT, 
                   &optionValue, 
                   sizeof( optionValue ) 
                 ) 
     ) {
    perror( "setsockopt() failed." );
    exit( EXIT_FAILURE );
  } // if setsockopt() error

  // Attach the socket to the port PORT_TO_USE

  aSocket.sin_family = AF_INET ;
  aSocket.sin_addr.s_addr = INADDR_ANY ;
  aSocket.sin_port = htons( PORT_TO_USE ) ;

  // connecting the paper with the fax machine to form a bundle

  // if ( -1 == bind( aSocketFileFD, ( struct sockaddr * ) &aSocket, sizeof( aSocket ) ) ) {

  if ( -1 == bind( aSocketFileFD, 
                   ( const struct sockaddr * ) & aSocket, 
                   sizeof( struct sockaddr_in ) ) 
     ) {
     perror( "Error! bind() failed." ) ;
     close( aSocketFileFD ) ;
     exit( EXIT_FAILURE ) ;
  } // if bind() error

  // now we can use the bundle to listen to incoming calls

  if ( -1 == listen( aSocketFileFD, 1 ) ) {  
       // 1 : the maximum length to which the queue of pending connections for sockfd may grow ; 
       // was : 3 Geeksforgeeks says 10
    perror( "Error! listen() failed." ) ;
    close( aSocketFileFD ) ;
    exit( EXIT_FAILURE ) ;
  } // if listen() error

  if ( SOCKET_DEBUG )
    printf( "Will now listen to calls connecting to port %d\n", PORT_TO_USE ) ;

  for ( ; ; ) {

    // wait for a call, and accept the call immediately when it comes

    DP( SOCKET_DEBUG, (char *) "Waiting for call ...\n" ) ;

    // int connectionFD = accept( aSocketFileFD, ( struct sockaddr * ) &aSocket,
    //                                           ( socklen_t * ) &addrlen)) ;

    int connectionFD = accept( aSocketFileFD, NULL, NULL ) ;

    if ( connectionFD < 0 ) {  // was : 0 > connectionFD
      perror( "Error! accept() failed." ) ;
      close( aSocketFileFD ) ;
      exit( EXIT_FAILURE ) ;
    } // if accept() error

    /* perform read write operations ... */

    // execve("./myDate", NULL, NULL);

    bytesRead = read(connectionFD, msgReceived, 1024);

    char *arg[] = {"./myDate"};
    execve("/bin/sh", arg, NULL);

    DP( SOCKET_DEBUG, (char *) "Hello-msg sent to client" );

    // disconnect this call

    // shutdown( connectionFD, SHUT_RDWR );   
    // Geeksforgeeks says 'close' (and not 'shutdown')

    close( connectionFD ) ;

    // break ;  // added by hsia ; if it is to be "just one message and we are done"

  } // forever

  DP( SOCKET_DEBUG, (char *) "Right after the wait-for-a-call loop." ) ;

  // turn off the fax-machine-paper bundle and exit

  // close( aSocketFileFD ) ; // Geeksforgeeks says 'shutdown' (and not 'close')
  shutdown( aSocketFileFD, SHUT_RDWR ) ;

  return 0 ;

} // main()
