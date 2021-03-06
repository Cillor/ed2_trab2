#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
#include <string.h>
#include <math.h>

#include "timeControl.h"
#include "utils.h"
#include "linkedList.h"

unsigned h_div(string str, unsigned B){
    unsigned x = converter(str);
    return x % B;
}

unsigned h_mul(string str, unsigned B){
    const double A = 0.6180;
    unsigned x = converter(str);
    return fmod(x * A, 1) * B;
}

unsigned h_improved(string s, unsigned B) {
   unsigned h = 1;
   const unsigned p1 = 189437;

   for (int i = 0; s[i] != '\0'; i++) 
      h = (h * s[i] * p1)%B;
   return h;
}

unsigned h_duplo(string s,unsigned B){
    return (h_mul(s, B) + h_div(s, B))%B;
}

void printHashTable(Node **hash_table, string file_id){
    string file_start = "build/hash_table_";
    string file_extension = ".txt";
    string file_loc = (string) malloc(sizeof(char) * (strlen(file_start) + strlen(file_id) + strlen(file_extension) + 1));
    file_loc[0] = '\0';
    strcat(file_loc, file_start);
    strcat(file_loc, file_id);
    strcat(file_loc, file_extension);

    FILE* fp = fopen(file_loc, "a");
    for (int i = 0; i < INPUTSIZE; i++){
        printList(&hash_table[i], fp);
        fprintf(fp, "\n");
    }
    fclose(fp);

    free(file_loc);
}

void hashTester(unsigned (*hash_function)(string, unsigned), string* insercoes, string* consultas, string id){
    const unsigned B = 150001;
    unsigned encontrados = 0;
    unsigned colisoes = 0;

    //cria uma tabela hash com todos os buckets nulos
    Node** hash_table = (Node**) malloc(sizeof(Node*) * B);
    for (unsigned i = 0; i < B; i++){
        hash_table[i] = NULL;
    }
    
    // inserção dos dados na tabela hash com hash por divisão        
    clock_t _ini = inicia_tempo();
    for (int i = 0; i < INPUTSIZE; i++) {
        // inserir insercoes[i] na tabela hash
        unsigned key = hash_function(insercoes[i], B); //chama o ponteiro para uma função hash
        if(hash_table[key] != NULL)
            colisoes++; //colisão é contada apenas uma vez
        insert(&hash_table[key], insercoes[i]); //insere o elemento de forma ordenada no bucket daquela posição hash
    }
    double tempo_insercao = finaliza_tempo(_ini);

    //mostra a hash table em um arquivo
    printHashTable(hash_table, id);
    
    // busca dos dados na tabela hash com hash por divisão
    _ini = inicia_tempo();
    for (int i = 0; i < CONSULTASIZE; i++) {
        // buscar consultas[i] na tabela hash
        unsigned key = hash_function(consultas[i], B);

        if(hash_table[key] == NULL)
            continue; //avança para frente se o bucket onde a consulta deveria estar estiver vazio
        
        if(findInList(&hash_table[key], consultas[i]) != NULL)
            encontrados++;
    }
    double tempo_busca = finaliza_tempo(_ini);

    // destroi tabela hash com hash por divisão
    for(unsigned i = 0; i < B; i++)
        freeList(&hash_table[i]);
    free(hash_table);

    string file_loc = retornarFileLoc("out/busca_hash_", id, ".csv");
    generateHashSearchTimeCSV(file_loc, encontrados, colisoes, tempo_insercao, tempo_busca);
    free(file_loc);

    printf("Hash por %s \t-> ", id);
    printf("Colisões na inserção: %d | ", colisoes);
    printf("Tempo de inserção: %fs | ", tempo_insercao);
    printf("Tempo de busca: %fs | ", tempo_busca);
    printf("Itens encontrados: %d", encontrados);
    printf("\n");
}

int ex2c(int n_testes, string* insercao_original, string* consultas_original){
    for(int j = 0; j < n_testes; j++){ //faz o número de testes pedidos
        printf("Busca %d: \n", j);

        //duplica o array orginal para não altera-lo
        string* insercoes = duplicarString(insercao_original, INPUTSIZE);
        string* consultas = duplicarString(consultas_original, CONSULTASIZE);

        //utiliza de ponteiro para função para chamar um hashTester para cada função de hash do trabalho
        hashTester(&h_div, insercoes, consultas, "aberto_divisao");
        hashTester(&h_mul, insercoes, consultas, "aberto_multiplicacao");
        hashTester(&h_improved, insercoes, consultas, "aberto_primos"); //uma função hash melhorada para servir de comparação efetiva
        hashTester(&h_duplo, insercoes, consultas, "aberto_duplo"); //o sistema de hash duplo do exercicio 2b, para comparações mais efetivass

        free(insercoes);
        free(consultas);
    }

    return 0;
}
