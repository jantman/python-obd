# FROM: https://www.scantool.net/forum/index.php?topic=794.0
#include <stdio.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>

void read_pid(int location);

int fd;
FILE *stdoutfile;

main () {
    int ret,i;
    struct termios term_struct;

    stdoutfile = fopen("results","a+");
    if(stdoutfile == NULL) {
        perror("fdopen:");
        exit(1);
    }

    fd = open("/dev/ttyS0",O_RDWR);
    if(fd < 0) {
        perror("open:");
        exit(1);
    }

    ret = tcgetattr(fd,&term_struct);
    if(ret < 0) {
        perror("tcgetattr:");
        exit(1);
    }
    cfmakeraw(&term_struct);
    ret = cfsetospeed(&term_struct,B9600);
    if(ret < 0) {
        perror("tcsetattr:");
        exit(1);
    }
    ret = tcsetattr(fd,TCSANOW,&term_struct);
    if(ret < 0) {
        perror("tcsetattr:");
        exit(1);
    }

    while(1) {
      read_pid(5);
      for(i=10;i<18;i++) read_pid(i);
    }

    close(fd);
}

void
read_pid(int location) {
    unsigned char buffer[100];
    unsigned char outgoing[100];
    int i,n,p,ret;

      n = sprintf(outgoing,"01 %02d\r",location);
      write(fd,outgoing,n);
      p = 0;
      do {
          n = read(fd,&buffer[p],1);
          if(n < 0) {
                  perror("read:");
                  exit(1);
          }
          p+=n;
          if(p > 80) break;
      } while(buffer[p-1] != 62);
      buffer[p+1] = 0;
      for(i=0;;i++) {
          if(buffer == '\r') {
                printf("\n");
                fprintf(stdoutfile,"\n");
          } else {
                printf("%c",buffer);
                fprintf(stdoutfile,"%c",buffer);
          }
          fflush(stdoutfile);
          if(buffer == '>') break;
      }
        printf("\n");
}
