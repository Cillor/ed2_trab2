#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "timeControl.h"
#include "utils.h"

void quicksort(int* vector,int c, int f){
    if (c>=f){
        return;
    }
    int m = (c+f)/2;
    int pivot = vector[m];
    int i = c;
    int j = f;
    while(1){
        while (vector[i]<pivot)
        {
            i++;
        }
        while(vector[j]>pivot){
            j--;
        }
        if(j <= i){
            break;
        }
        int tmp = vector[i];
        vector[i] = vector[j];
        vector[j] = tmp;
        i++;
        j--;
    }
    quicksort(vector,c,j);
    quicksort(vector,j+1,f);
}

int ex1d(int n_testes, int* entradas_original, int* consultas_original){
    for(int j = 0; j < n_testes; j++){
        unsigned encontrados = 0;
        int* entradas = duplicarArray(entradas_original, INPUTSIZE);
        int* consultas = duplicarArray(consultas_original, INPUTSIZE);
        printf("Busca %d: \n", j);

        // ordenar entrada
        quicksort(entradas,0,INPUTSIZE);

        // criar tabela de indice


        // realizar consultas na tabela de indices 
        clock_t _ini = inicia_tempo();
        for (int i = 0; i < INPUTSIZE; i++) {
            // buscar o elemento consultas[i] na entrada
        }
        double tempo_busca = finaliza_tempo(_ini);

        printf("Tempo de busca: %fs | ", tempo_busca);
        printf("Itens encontrados: %d\n", encontrados);
    }
    return 0;
}