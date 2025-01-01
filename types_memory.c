#include <stdio.h>
#include <stdlib.h>


typedef struct rigString{

    char* content;
    size_t lenght;
} rigString;


typedef struct rigConnection{
    
    rigString protocol;
    rigString host;
    rigString port;
} rigConnection;


typedef struct rigTable{

    rigString* fields;
    size_t fieldsAmount;
} rigTable;


typedef struct rigDatabase{
    
    rigTable* tables;
    size_t tablesAmount;
} rigDatabase;


rigString rigStrInit(char* text){

    rigString *ptr = NULL;
    ptr = (rigString *) malloc(sizeof(char) * strlen(text));

    if (ptr){

        ptr->content = text;
        ptr->lenght = strlen(text);

        return *ptr;
        free(ptr);
    }
    else{

        printf("%s\n", "Attempt to memory allocate had been failed.");
        free(ptr);
    };
};


rigConnection rigConInit(rigString protocol, rigString host, rigString port){

    rigConnection *ptr = NULL;
    ptr = (rigConnection *) malloc(sizeof(protocol) + sizeof(host) + sizeof(port));

    if (ptr){

        ptr->protocol = protocol;
        ptr->host = host;
        ptr->port = port;

        return *ptr;
        free(ptr);
    }
    else{

        printf("%s\n", "Attempt to memory allocate had been failed.");
        free(ptr);
    };
};


rigTable rigTabInit(rigString* *fields){

    size_t tableSize = 0;

    while (fields[tableSize]){

        tableSize++;
    };

    rigTable *ptr = NULL;
    ptr = (rigTable *) calloc(tableSize, sizeof(rigString));

    if (ptr){

        ptr->fields = fields;
        ptr->fieldsAmount = tableSize;
        
        return *ptr;
        free(ptr);
    }
    else{

        printf("%s\n", "Attempt to memory allocate had been failed.");
        free(ptr);
    };
};


rigDatabase rigDBInit(rigTable* *tables){

    size_t amountOfTables = 0;

    while (tables[amountOfTables]){

        amountOfTables++;
    };

    rigDatabase *ptr = NULL;
    ptr = (rigDatabase *) calloc(amountOfTables, sizeof(rigTable));

    if (ptr){

        ptr->tables = tables;
        ptr->tablesAmount = amountOfTables;

        return *ptr;
        free(ptr);
    }
    else{

        printf("%s\n", "Attempt to memory allocate had been failed.");
        free(ptr);
    };
}


int main(void){

    return 0;
};
