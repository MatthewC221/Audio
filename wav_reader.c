#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "wav.h"

// A very basic wav reader, reads the header, then the data. Transfers it to a different file


int main(int argc, char *argv[])
{

    // Write to new.wav
    
    if (argc != 2) {
        fprintf(stderr, "Usage ./test <.wav file>\n");
    } else {
        FILE *in = fopen(argv[1], "r");
        if (!in) fprintf(stderr, "Invalid read of .wav\n");

        FILE *out = fopen("new.wav", "wb");
        
        int frame_size = 512;
        int count = 0;
        short int bits[frame_size];
        int chunks = 0;
        
        WavHeader * new_header = malloc(sizeof(*new_header));
        
        fread(new_header, 1, sizeof(WavHeader), in);
        printf("Size of header file = %lu\n", sizeof(new_header));
        printf("Sampling rate of header file = %zu\n", new_header->sample_rate);
        printf("Number of samples in .wav = %zu\n", new_header->subchunk2Size);
        fwrite(new_header, 1, sizeof(*new_header), out);
        
        while (!feof(in)) {
            chunks = fread(bits, 1, frame_size, in);
            count++;
            fwrite(bits, 1, chunks, out);
        }
        
        /*
        for (int i = 0; i < frame_size; i++) {
            printf("%d\n", bits[i]);
        }
        */
        printf("Number of frames in .wav = %d\n", count);
    }

    return EXIT_SUCCESS;
}
