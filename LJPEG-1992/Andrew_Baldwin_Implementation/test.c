#include <math.h>
#include <time.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lj92.h"

#define IMAGE_WIDTH (4096)
#define IMAGE_HEIGHT (3072)

#define CHECK_MEM_MALLLOC(x) {if(x==NULL){printf("Memory Allocation Failed.\n"); exit(1);}}
#define ERROR_TERMINATE(msg) {printf("%s\n", msg); exit(2);}

void sanity_check() {
    srand(time(0));
    int num_of_tests = 10;
    for(int i=16; i!=1; i--) {
        for(int j=0; j<num_of_tests; j++) {
            //create 2-image.
            uint16_t* input_image = malloc(IMAGE_WIDTH*IMAGE_HEIGHT*sizeof(uint16_t));
            uint16_t* output_image = malloc(IMAGE_WIDTH*IMAGE_HEIGHT*sizeof(uint16_t));
            CHECK_MEM_MALLLOC(input_image);
            CHECK_MEM_MALLLOC(output_image);
            //randomize input image pixels.
            for(int k=0; k<(IMAGE_WIDTH*IMAGE_HEIGHT); k++) {
                input_image[k] = rand()%((int)(pow(2,i)));
            }
            //encode the image.
            uint8_t* encoded;
            int encodedLength;
            if(lj92_encode(input_image, IMAGE_WIDTH*2, IMAGE_HEIGHT/2, i, IMAGE_WIDTH*IMAGE_HEIGHT*sizeof(uint16_t), 0, NULL, 0, &encoded, &encodedLength) != LJ92_ERROR_NONE) {
                ERROR_TERMINATE("Failed in encoding the image.");
            }
            //try to open the image to decode it.
            lj92 decode;
            int w,h,bd;
            if(lj92_open(&decode, encoded, encodedLength, &w, &h, &bd) != LJ92_ERROR_NONE) {
                ERROR_TERMINATE("Failed in opening the encoded image.");
            }
            //check the decoded dimensions.
            if(w != IMAGE_WIDTH*2 || h != IMAGE_HEIGHT/2 || bd != i) {
                ERROR_TERMINATE("Failed in reading the correct image information from encoded image.");
            }
            //decode the image.
            if(lj92_decode(decode, output_image, IMAGE_WIDTH*IMAGE_WIDTH*sizeof(uint16_t)   , 0, NULL, 0) != LJ92_ERROR_NONE) {
                ERROR_TERMINATE("Failed in decoding the encoded image.");
            }
            //compare the original image and the decoded image.
            if(memcmp(input_image, output_image, IMAGE_WIDTH*IMAGE_HEIGHT*sizeof(uint16_t)) != 0) {
                ERROR_TERMINATE("The decoder failed in decoding the encoded image.");
            }
            //success
            printf("Image %i with bit depth %i test succeeded.\n",j,i);
            free(input_image);
            free(output_image);
        }
    }
}

void optimal_case_test() {
    //create 1-image.
    uint16_t* input_image = malloc(IMAGE_WIDTH*IMAGE_HEIGHT*sizeof(uint16_t));
    CHECK_MEM_MALLLOC(input_image);
    //zero input image pixels.
    for(int k=0; k<(IMAGE_WIDTH*IMAGE_HEIGHT); k++) {
        input_image[k] = 0;
    }
    //encode the image.
    uint8_t* encoded;
    int encodedLength;
    if(lj92_encode(input_image, IMAGE_WIDTH*2, IMAGE_HEIGHT/2, 8, IMAGE_WIDTH*IMAGE_HEIGHT*sizeof(uint16_t), 0, NULL, 0, &encoded, &encodedLength) != LJ92_ERROR_NONE) {
        ERROR_TERMINATE("Failed in encoding the image.");
    }
    //check the encoded length
    if(encodedLength != 1572916) {
        printf("Encoder does not generate optimal size.\n");
        printf("Encoded size is: %d, expected is: 259252, ratio is: %lf.\n", encodedLength, (double)encodedLength/259252.0);
    }else {
        printf("Encoder: Optimal size is achieved successfully.\n");
    }
    free(input_image);  
}

int main(void) {
    optimal_case_test();
    sanity_check();
}