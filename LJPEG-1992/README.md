# JPEG 1992 Lossless Compression
In this file I will try to summarize everything I know about JPEG 1992 standard related to compress RAW image.

What I am concerned about is how to use the lossless mode of JPEG 1992 standard in encoding the RAW Bayer image coming out of the sensor.

I will short it with LJPEG.

## General Overview
LJPEG depends mainly on two things, the predictor functions and Huffman coding. It does support any bit-depth from 2 to 16. It can be used in parallel to encode several parts of the image in parallel.

The main idea is to use a predictor function to estimate the pixel value, then we subtract the predicted value from the real value, and we only concerned about the difference. Given that the pixels are close in values to each other we can easily predict the value of the wanted pixel from the neighbor pixels. So -hopefully- the output of the subtraction will be small and can be encoded in small number of bits.
When it comes to RAW images it slightly different as not all the neighbor pixels represent the same color.

Huffman coding used to encode SSSS values -will be explained later-, the main purpose of this is to give smaller number of bits to the more frequent pixel values.
Huffman coding is only used on SSSS values not on the pixel values or the predicted pixel values or the subtracted pixel values, so it is not a replacement of a good predictor function. 

## Predictor Functions
```
     |     |     |     |     |
+---------------------------------+
     |     |  C  |  B  |     |
+---------------------------------+
     |     |  A  |  X  |     |
+---------------------------------+
     |     |     |     |     |
```
- X: is the pixel we currently try to encode.
- A: is the pixel on left of it.
- B: is the pixel on top of it.
- C is the pixel on top-left of it.

##### LJPEG introduced 8 prediction functions.

|Selection Value|Prediction Function|
|----|----|
|0|No Prediction|
|1|Px = Ra|
|2|Px = Rb|
|3|Px = Rc|
|4|Px = Ra + Rb - Rc|
|5|Px = Ra + ((Rb - Rc)/2)|
|6|Px = Rb + ((Ra - Rc)/2)|
|7|Px = ((Ra + Rb)/2)|
- Px: is the predicted value of pixel X.
- Ra: is the value of pixel A.
- Rb: is the value of pixel B.
- Rc: is the value of pixel C.
- Note: division is implemented as shift right arithmetic operation.
- Note: selection-value 0 can't be used for our compression purpose, it shall only be used for differential coding in the hierarchical mode of operation.
- Note: each prediction is calculated with full integer arithmetic precision, and without clamping of either underflow or overflow.

The first step is to choose predictor function that will predict close value to the predicted pixel.

And here is our first problem. We know that RAW Bayer image like RGGB is ordered as follows,
R G R G R G R G ..... R G 
G B G B G B G B ..... G B
which will make all the prediction functions not accurate, specially for red and blue pixels.

The solution to this problem by tricking the encoder/decoder by giving the dimension {width*2, height/2} instead of {width, height}. that will effectively make the pattern as follows,
R G R G .... R G G B G B G B .... G B
R G R G .... R G G B G B G B .... G B
which will make function-2 a good predictor function, but what even better is function-6 which add to Rb half the difference of (Ra, Rc), why this works? because (Ra, Rc) are same color, so the change from Rc to Ra is a good estimator of the change from Rb to Rx.

Note: When using function-X, the first pixel of the image is predicted as (2^(bit-depth - 1)) and the pixels in the first row is predicted using function-1 and the first pixel of each column is predicted using function-2. The rest of the pixels is predicted using function-X.

## SSSS Values
After selecting the predictor function we do frequency scan. That mean we will predict each pixel as 'Px', then calculate the difference between real value 'Rx' and predicted value 'Px' as 'diff = Rx - Px', 'diff' can be wide in values, for example in function-6, Px = [-32767, 98302], Rx = [0, 65535], diff = [-98302, 98302].
The first step in processing the 'diff' is by 'diff mod 2^16'. now diff = [-65535, 65535].

##### LJPEG introduce SSSS values.
| SSSS | Difference values|
|  :---: |  :---: |
|0|0|
|1|–1,1|
|2|–3,–2,2,3|
|3|–7..–4,4..7|
|4|–15..–8,8..15|
|5|–31..–16,16..31|
|6|–63..–32,32..63|
|7|–127..–64,64..127|
|8|–255..–128,128..255|
|9|–511..–256,256..511|
|10|–1023..–512,512..1023|
|11|–2047..–1024,1024..2047|
|12|–4095..–2048,2048..4095| 
|13|–8191..–4096,4096..8191|
|14|–16383..–8192,8192..16383|
|15|–32767..–16384,16384..32767|
|16|32768|

How 'diff' relates to SSSS values?
LJPEG classify each 'diff' value to SSSS class. Then we use huffman coding to assign each SSSS class a code. then the pixel is encoded as 'SSSS-code' concatenate 'bits-to-identify-difference-value-in-class'.
For example let's assume that
- diff = -5400
- diff = diff%(2^16) = -5400
- diff = abs(diff) = 5400
- binary(diff) = 00000000000000000001010100011000
- SSSS-class = 32 - (number of preceding zeros in binary representation) 19 =  13.
- number of bits to represent this pixel = huffman_code(SSSS-class = 13) + 13bits.

##### Putting all together.
- Choose predictor function.
- Do frequency scan and count number of pixels in each SSSS-class.
- Based on the count of each SSSS-class, do Huffman coding to assign value to each SSSS-class.
- Do another loop on all the pixels to do actual compressing by replacing each pixel by 'huffman_code(SSSS-class)' concatenate 'bits-to-identify-difference-value-in-class'.

| SSSS-class | number of bits to identify difference value|
|  :---: |  :---: |
|0|0|
|1|1|
|2|2|
|3|3|
|4|4|
|5|5|
|6|6|
|7|7|
|8|8|
|9|9|
|10|10|
|11|11|
|12|12|
|13|13|
|14|14|
|15|15|
|16|0|

## Encoder Implementation Details:
### First phase: scan diff values
- Use the predictor function to estimate the value of each pixel.
- diff % (2^16)
- abs(diff)
- SSSS-class = 32 - number_of_preceding_zeros(diff)
- Increment that SSSS-class counter by one.
##### At the end of this phase we should have vector named 'SSSS_histogram' which consists of 17 entry [0 to 16] and contain number of pixels in each SSSS-class.

### Second phase: generate BITS and HUFFVAL vectors -Huffman Coding-
- BITS is a vector of length 16, BITS represent count of each code-size and total number of nodes in the tree. For example BITS={0,3,1,1,1,1,0,0,0,0,0,0,0,0,0,0} means that it represent a tree with a total of 7 nodes. With three nodes of code-size=2, one node of code-size=3, one node of code-size=4, one node of code-size=5, one node of code-size=6. This mean only 7 of SSSS-class have data and encoded but which SSSS-class have data and which not can't be known from BITS vector.
- HUFFVAL is a vector of length equal to number of nodes in the tree, its job is to specify exactly which SSSS classes are used and what is the order, so the the class with the most pixels will get the shortest code-size and the class with the least number of pixels will get the longest code-size. for example, for given BITS vector BITS={0,3,1,1,1,1,0,0,0,0,0,0,0,0,0,0}, HUFFVAL={1,2,0,4,5,9,7}, that mean SSSS-class=1 have the most number of pixels and will get assigned the shortest available code-size and class=7 have the least pixels and will get the longest available code-size,and any class not mentioned have zero pixels. Combining both BITS and HUFFVAL vectors, that means the following {Class=1 have code-size of 2, Class=1 have code-size of 2, Class=0 have code-size of 2, Class=4 have code-size of 3, Class=5 have code-size of 4, Class=9 have code-size of 5, Class=7 have code-size of 5}
- LJPEG only use BITS and HUFFVAL vectors to generate the huffman tree in the encoding/decoding process. LJPEG specification do not specify strictly how to generate BITS and HUFFVAL vectors out of SSSS_histogram vector, but It propose a way of generating BITS and HUFFVAL vectors. As long as BITS and HUFFVAL vectors represents correct Huffman tree, then it's accepted.

#### Proposed way to build BITS and HUFFVAL.
For BITS vector: CCITT Rec. T.81 (1992 E) pages 144,145,146 and 147.
For HUFFVAL vector: CCITT Rec. T.81 (1992 E) page 148.
Examples for combination of BITS and HUFFVAL: CCITT Rec. T.81 (1992 E) page 158.

Note: In JPEG format, every Byte with 0xFF is followed by Byte with 0x00. The proposed way to build BITS and HUFFVAL is designed so that you never assign a code with all 1Bits. So if you used another way to build BITS and HUFFVAL make sure that you don't use code with all 1 bits or it will make your compression worse.
Note: As far as I know, the proposed way always have a code size of one, you might get better results if you remove this codeword and used 3 code size of 2.

### Third phase: generate HUFFSIZE and HUFFCODE vectors.
- After generating BITS and HUFFVAL vectors, these vectors are encoded in the header and will be used to generate two vectors HUFFSIZE and HUFFCODE which will be used to encode/decode the image.
- HUFFSIZE is vector contains the code-size of each class. for example BITS={0,3,1,1,1,1,0,0,0,0,0,0,0,0,0,0}, HUFFVAL={1,2,0,4,5,9,7}, HUFFSIZE = {2,2,2,0,3,4,0,6,0,5} which mean class-0 consists of 2bits, class-1 consists of 2bits, class-2 consists of 2bits, class-3 consists of 0bits-as it is not in HUFFVAL-, class-4 consists of 3bits and so on.
- HUFFCODE is a vector contains the actual code for each class, for example BITS={0,3,1,1,1,1,0,0,0,0,0,0,0,0,0,0}, HUFFVAL={1,2,0,4,5,9,7}, HUFFSIZE = {2,2,2,0,3,4,0,6,0,5}, HUFFCODE = {0b00,0b01,0b10,0b0,0b110,0b1110,0b0,0b111110,0,0b11110}.
- To generate HUFFSIZE and HUFFCODE, CCITT Rec. T.81 (1992 E) pages 54,55,56 and 57.

### Fourth phase: Compressing the data.
- We will need to do another scan, use predictor function to estimate the pixel value, get diff value and get the SSSS-class of this pixel.
- We need to do write the Huffman coding for this class + bits to identify the difference within this class.
- Firstly we write the Huffman code for this class placed toward the MSB. If code-size=13, First 8 bits will be placed in a Byte toward the MSB, then other 5 bits will be placed in the next byte toward the MSB and consuming 5 bits.
- After writing the class code, we will write the difference from most negative to most positive, for example in class-3 we know we need 3 bits to for the "diff" value, in class-3 we have the following diff values [-7, -4] and [4, 7] in total of 8 values, so -7 will be 0b000, -6 will be 0b001, -5 will be 0b010, -4 will be 0b011, 4 will be 0b100, 5 will be 0b101, 6 will be 0b110, 7 will be 0b111.
- Note: whenever we write a Byte with 0xFF we must write the following Byte 0x00.

##### Notes about Bit ordering from CCITT Rec. T.81 (1992 E)
```
C.3 Bit ordering within bytes
The root of a Huffman code is placed toward the MSB (most-significant-bit) of the byte, and successive bits are placed in the direction MSB to LSB (least-significant-bit) of the byte. Remaining bits, if any, go into the next byte following the same rules.
Integers associated with Huffman codes are appended with the MSB adjacent to the LSB of the preceding Huffman code.
```

### Read more
- [Wikipedia - Lossless JPEG](https://en.wikipedia.org/wiki/Lossless_JPEG).
- [How DNG compresses raw data with lossless JPEG92](https://thndl.com/how-dng-compresses-raw-data-with-lossless-jpeg92.html).
- [CCITT Rec. T.81 (1992 E) - PDF](https://www.w3.org/Graphics/JPEG/itu-t81.pdf).
- [Github - aaalgo/ljpeg](https://github.com/aaalgo/ljpeg).
- [Github - ilia3101/MLV-App/liblj92](https://github.com/ilia3101/MLV-App/tree/master/src/mlv/liblj92).
