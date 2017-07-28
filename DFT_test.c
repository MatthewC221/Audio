#include <stdio.h>
#include <stdlib.h>
#include "DFT.h"

int main(int argc, char *argv[])
{

    if (argc == 2) {

        int size = atoi(argv[1]);
        double complex * tmp = malloc(sizeof(double complex) * atoi(argv[1]));
        for (int i = 0; i < size; i++) tmp[i] = i;    
        double complex * new = FFT(tmp, size);
        printSignal(new, size);

    } else {
        fprintf(stderr, "Usage ./DFT_test <size_of_FFT>\n");
    }

    return EXIT_SUCCESS;
}
