#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "wav.h"

// A very basic wav reader, reads the header, then the data. Transfers it to a different file
// (identical files)

int main(int argc, char *argv[])
{

    // Write to new.wav
    
    if (argc != 3) {
        fprintf(stderr, "Usage ./test <.wav file> <percentage_volume_decrease>\n");
    } else {
    
        double percent;
        sscanf(argv[2], "%lf", &percent);
        
        if (percent > 1 || percent < 0) {
            fprintf(stderr, "Please enter valid percentage range 0->1\n");
            return EXIT_FAILURE;
        }        
    
        FILE *in = fopen(argv[1], "rb");
        
        if (!in) fprintf(stderr, "Invalid read of .wav\n");

        FILE *out = fopen("new.wav", "wb");
        
        int frame_size = 512;
        int count = 0;
        
        // I was originally using short int instead of 8-bit ints, this was the issue!
        uint8_t bits[frame_size];
        int chunks = 0;
        
        WavHeader * new_header = malloc(sizeof(*new_header));
        
        fread(new_header, 1, sizeof(WavHeader), in);
        printf("Size of header file = %lu\n", sizeof(WavHeader));
        printf("Sampling rate of header file = %zu\n", new_header->sample_rate);
        printf("Number of samples in .wav = %zu\n", new_header->subchunk2Size);
        
        // Slows down the .wav file by two times
        // new_header->sample_rate = new_header->sample_rate * 0.5;
        
        fwrite(new_header, 1, sizeof(*new_header), out);         
        percent = (1 - percent);            // Volume decrease

        while (!feof(in)) {
            chunks = fread(bits, 1, frame_size, in);
            
            // This reduces the volume!
            for (int i = 0; i < frame_size; i++) {
                bits[i] = bits[i] * percent;
            }
            
            
            count++;
            fwrite(bits, 1, chunks, out);
        }
        
        printf("Number of frames in .wav = %d\n", count);
        printf("Percentage decrease = %2f into file new.wav\n", 1 - percent);
    }

    return EXIT_SUCCESS;
}
