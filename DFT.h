#include <stdio.h>
#include <complex.h>
#include <stdlib.h>
#include <math.h>

// Will hopefully turn this into a lib for DFT and FFT in C

#ifndef _DFT_h
#define _DFT_h
#define M_PI   3.14159265358979323846264338327950288

double complex * DFT (double complex * arr, size_t DFT_size);
double complex * FFT (double complex * arr, size_t DFT_size);
double complex sum(double complex * arr, int index, int DFT_size);
int nextPow(int size);
void printSignal (double complex * arr, size_t DFT_size);

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

    int padding_size = nextPow(FFT_size);
    // Zero pad first
    double complex * padded = malloc(sizeof(double complex) * padding_size);

    // Copy over first elements

    for (int i = 0; i < FFT_size; i++) padded[i] = arr[i];

    for (int i = FFT_size; i < padding_size; i++) padded[i] = 0;

    int half = padding_size / 2; 

    double complex * even = malloc(sizeof(double complex) * half);
    double complex * odd = malloc(sizeof(double complex) * half);

    int count = 0;
    for (int i = 0; i < padding_size; i = i + 2) {
        even[count++] = padded[i];
    }

    count = 0;
    for (int i = 1; i < padding_size; i = i + 2) {
        odd[count++] = padded[i];
    }

    double complex * even_DFT = malloc(sizeof(double complex) * half);
    double complex * odd_DFT = malloc(sizeof(double complex) * half);

    // NOT GOING TO LIE: This took me ages, I kept messing up the values... zero-pad but don't use
    // the size INCLUDING the pad. E.g. N = 8 even if there are 8 zero-pad vals

    for (int j = 0; j < half; j++) {
        double complex sum = 0;
        for (int i = 0; i < half; i++) {
            sum = sum + (even[i] * cexp(-I * 2 * M_PI * (i * 2) * j / FFT_size));
        }
        even_DFT[j] = sum;
    }

    for (int j = 0; j < half; j++) {
        double complex sum = 0;
        for (int i = 0; i < half; i++) {
            sum = sum + (odd[i] * cexp(-I * 2 * M_PI * (i * 2 + 1) * j / FFT_size));
        }
        odd_DFT[j] = sum;
    }

    double complex * overall_FFT = malloc(sizeof(double complex) * half);
    for (int i = 0; i < half; i++) {
        overall_FFT[i] = even_DFT[i] + odd_DFT[i];
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