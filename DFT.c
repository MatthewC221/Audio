#include <stdio.h>
#include <complex.h>
#include <stdlib.h>
#include <math.h>

// Will hopefully turn this into a lib for DFT and FFT in C

double complex * DFT (double complex * arr, int size);
double complex sum(double complex * arr, int index, int DFT_size);
int nextPow(int size);

int main(int argc, char *argv[])
{

    double complex tmp[5];

    for (int i = 1; i < 6; i++) tmp[i - 1] = i;    
    double complex * new = DFT(tmp, 5);

    return EXIT_SUCCESS;
}

// Basic DFT O(n^2)
double complex * DFT (double complex * arr, int DFT_size) 
{
     
    double complex * DFT = malloc(sizeof(double complex) * DFT_size);
    printf("[ ");
    for (int i = 0; i < DFT_size; i++) {
        DFT[i] = sum(arr, i, DFT_size);
        printf("%.2f+%.2fi ", creal(DFT[i]), cimag(DFT[i]));
    }
    printf("]\n");

    return DFT;
}

// Does the summation for the index
double complex sum(double complex * arr, int index, int DFT_size) 
{
    double complex sum = 0;
    for (int i = 0; i < DFT_size; i++) {
        sum = sum + (arr[i] * cexp(-I * 2 * M_PI * i * index / DFT_size));
    }
    
    return sum; 
}

// Use later for padding
int nextPow(int size) 
{

    int i = 1;
    while (size > i) i = i * 2;
    
    return i;
}
