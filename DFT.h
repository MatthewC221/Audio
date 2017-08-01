#include <stdio.h>
#include <complex.h>
#include <stdlib.h>
#include <math.h>
#include <inttypes.h>

// Will hopefully turn this into a lib for DFT and FFT in C

#ifndef _DFT_h
#define _DFT_h
#define M_PI   3.14159265358979323846264338327950288
#define POW 20

double complex * DFT (double complex * arr, size_t DFT_size);
double complex * FFT (double complex * arr, size_t DFT_size);
double complex sum(double complex * arr, int index, int DFT_size);
int nextPow(int size);
void printSignal (double complex * arr, size_t DFT_size);

int powers_of_2[20] = {2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 
    2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 2097152};

/*
int main(int argc, char *argv[])
{

    double complex tmp[5];

    for (int i = 1; i < 6; i++) tmp[i - 1] = i;    
    double complex * new = DFT(tmp, 5);

    return EXIT_SUCCESS;
}
*/

// Basic DFT O(n^2)
double complex * 
DFT (double complex * arr, size_t DFT_size) 
{
     
    double complex * DFT = malloc(sizeof(double complex) * DFT_size);

    for (int i = 0; i < DFT_size; i++) DFT[i] = sum(arr, i, DFT_size);

    return DFT;
}


// Radix-2 FFT, need to do recursion to break down into NlogN
double complex *
FFT (double complex *arr, size_t FFT_size)
{

    int padding_size = -1;
    for (int i = 0; i < POW; i++) {
        if (powers_of_2[i] > FFT_size) {
            padding_size = powers_of_2[i];
            break;
        }
    }
    printf("padding size = %d\n", padding_size);
    
    // Zero pad first
    double complex * padded = malloc(sizeof(double complex) * padding_size);

    // Copy over first elements

    for (int i = 0; i < FFT_size; i++) padded[i] = arr[i];

    for (int i = FFT_size; i < padding_size; i++) padded[i] = 0;

    int half = padding_size / 2; 

    // NOT GOING TO LIE: This took me ages, I kept messing up the values... zero-pad but don't use
    // the size INCLUDING the pad. E.g. N = 8 even if there are 8 zero-pad vals

    double complex * overall_FFT = malloc(sizeof(double complex) * FFT_size);

    for (int j = 0; j < FFT_size; j++) {

        double complex sum_odd = 0;
        double complex sum_even = 0;

        for (int i = 0; i < half; i++) {
            int index = (i * 2) + 1;
            sum_odd = sum_odd + (padded[index] * cexp(-I * 2 * M_PI * index * j / FFT_size));
        }
        for (int i = 0; i < half; i++) {
            int index = i * 2;
            sum_even = sum_even + (padded[index] * cexp(-I * 2 * M_PI * index * j / FFT_size));
        }

        overall_FFT[j] = sum_odd + sum_even;
    }

    return overall_FFT;
}

// Does the summation for the index
void 
printSignal (double complex * arr, size_t DFT_size) 
{
    printf("[  ");
    for (int i = 0; i < DFT_size; i++) {
        printf("%.2f+%.2fi", creal(arr[i]), cimag(arr[i]));
        if (i != DFT_size - 1) {
            printf(",  ");
        } else {
            printf("  ]\n");
        }
    }

}


double
complex sum(double complex * arr, int index, int DFT_size) 
{
    double complex sum = 0;

    for (int i = 0; i < DFT_size; i++) {
        sum = sum + (arr[i] * cexp(-I * 2 * M_PI * i * index / DFT_size));
    }
    
    return sum; 
}

double 
complex * convert(uint8_t * arr, int size)
{
    double complex * new_arr = (double complex *)malloc(sizeof(double complex) * size);
    for (int i = 0; i < size; i++) new_arr[i] = arr[i] + 0 * I;

    return new_arr;
}

// Use later for padding
int
nextPow(int size) 
{

    int i = 1;
    int padding = 0;
    while (size > i) {
        i = i * 2;
    }

    return i * 2;
}

#endif