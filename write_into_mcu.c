#include <stdio.h>
#include "string.h"

#define RESFILE "result.txt"
#define PREFILE "C:\\Users\\30744\\Desktop\\ComputerVision\\CV.txt"
#define ISPFILE "C:\\CodeFiles\\MCU_C51\\CV.c"
#define target_line 8

int main() {
    FILE *f = fopen(RESFILE, "r");
    char num = 0;
    int line = 0;
    fscanf(f, "%c", &num);
    fclose(f);
    if (num != 0) {
        FILE *f_old = fopen(PREFILE, "r");
        FILE *f_new = fopen(ISPFILE, "w");
        char *msg = "unsigned char timer1=";

        if (f_new != NULL && f_old != NULL) {
            printf("%s", "ok");
            char file_msg[100];
            while (fgets(file_msg, sizeof(file_msg), f_old)) {
                line++;
                if (line == target_line) {
                    fprintf(f_new, "%s%c%c%c", msg, num, ';', '\n');
                }
                else {
                    fprintf(f_new, "%s", file_msg);
                }
                memset(file_msg, '\0', sizeof(file_msg));
            }
        }
        fclose(f_new);
    }

}
