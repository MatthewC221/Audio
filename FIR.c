#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "wav.h"

#define frame_size 512
// A very basic wav reader, reads the header, then the data. Transfers it to a different file
// (identical files)

void FILTER(uint8_t *bits, uint8_t *filtered, int count);

double simple_filter[3] = {0.25, 0.5, 0.25};
uint8_t last_val = 0;

// The changed values
uint8_t temp_filter[frame_size];


int main(int argc, char *argv[])
{

    // Write to new.wav
    
    if (argc != 2) {
        fprintf(stderr, "Usage ./test <.wav file>\n");
    } else {       
    
        FILE *in = fopen(argv[1], "rb");
        
        if (!in) fprintf(stderr, "Invalid read of .wav\n");

        FILE *out = fopen("FIR.wav", "wb");
        
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
        uint8_t filtered[frame_size];

        while (!feof(in)) {
            chunks = fread(bits, 1, frame_size, in);
                   
            FILTER(bits, filtered, count);  
            
            count++;
            fwrite(filtered, 1, chunks, out);
        }
        
        printf("Number of frames in .wav = %d\n", count);
    }

    return EXIT_SUCCESS;
}

void FILTER(uint8_t *bits, uint8_t *filtered, int count)
{
    
    // bits[-1] and bits[size + 1] = 0
    filtered[0] = bits[0] * simple_filter[1] 
        + bits[1] * simple_filter[2];
        
    if (count) filtered[0] = filtered[0] + simple_filter[0] * last_val;

    for (int i = 1; i < frame_size; i++) {
        filtered[i] = bits[i - 1] * simple_filter[0] + bits[i] * simple_filter[1];
        if (i != frame_size - 1) {
            filtered[i] = filtered[i] + bits[i + 1] * simple_filter[2];
        } else {
            last_val = bits[i];
        }

    }
    
}
    













