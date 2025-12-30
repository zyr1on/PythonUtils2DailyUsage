#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>

void shift_time(int *h, int *m, int *s, int *ms, double shift) {
    int total_ms = (*h*3600 + *m*60 + *s)*1000 + *ms + (int)(shift*1000);
    if(total_ms < 0) total_ms = 0;

    *h = total_ms / 3600000;
    total_ms %= 3600000;
    *m = total_ms / 60000;
    total_ms %= 60000;
    *s = total_ms / 1000;
    *ms = total_ms % 1000;
}

int main(int argc, char *argv[]) {
    char *input_file = NULL;
    char *output_file = NULL;
    double shift = 0.0;

    int opt;
    static struct option long_options[] = {
        {"file", required_argument, 0, 'f'},
        {"time", required_argument, 0, 't'},
        {"output", optional_argument, 0, 'o'},
        {0,0,0,0}
    };

    while((opt = getopt_long(argc, argv, "f:t:o:", long_options, NULL)) != -1) {
        switch(opt) {
            case 'f': input_file = optarg; break;
            case 't': shift = atof(optarg); break;
            case 'o': output_file = optarg; break;
            default:
                fprintf(stderr, "Usage: %s --file <file> --time <seconds> [--output <file>]\n", argv[0]);
                return 1;
        }
    }

    if(!input_file) {
        fprintf(stderr, "Enter input file, --file <file> --time <seconds> [--output <file>]\n");
        return 1;
    }

    if(!output_file) {
        char *dot = strrchr(input_file, '.');
        if(dot) {
            size_t len = dot - input_file;
            output_file = malloc(len + 20); // yeterli alan
            strncpy(output_file, input_file, len);
            output_file[len] = '\0';
            strcat(output_file, "_rsynced");
            strcat(output_file, dot); // uzantıyı ekle
        } else {
            output_file = malloc(strlen(input_file)+10);
            sprintf(output_file, "%s_rsynced", input_file);
        }
    }

    FILE *fin = fopen(input_file, "r");
    FILE *fout = fopen(output_file, "w");
    if(!fin || !fout) {
        fprintf(stderr, "File not found or file is broken.\n");
        return 1;
    }

    char line[512];
    while(fgets(line, sizeof(line), fin)) {
        int h1,m1,s1,ms1,h2,m2,s2,ms2;
        if(sscanf(line, "%d:%d:%d,%d --> %d:%d:%d,%d",
                  &h1,&m1,&s1,&ms1,&h2,&m2,&s2,&ms2) == 8) {

            shift_time(&h1,&m1,&s1,&ms1, shift);
            shift_time(&h2,&m2,&s2,&ms2, shift);

            fprintf(fout, "%02d:%02d:%02d,%03d --> %02d:%02d:%02d,%03d\n",
                    h1,m1,s1,ms1,h2,m2,s2,ms2);
        } else {
            fputs(line, fout);
        }
    }

    fclose(fin);
    fclose(fout);

    printf("Subtitle shifted and saved as '%s' and shifted %lf .\n", output_file,shift );

    if(output_file && !strstr(output_file, "_rsynced")) free(output_file);
    return 0;
}
