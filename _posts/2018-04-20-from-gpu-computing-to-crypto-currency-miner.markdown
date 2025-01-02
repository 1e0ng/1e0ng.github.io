---
layout: post
title: "From GPU Computing to Cryptocurrency Miner"
date: 2018-04-20 22:33:44 +0800
comments: true
categories: 
- GPU
- Cryptocurrency
---

OpenCL (Open Computing Language) is a new framework for writing programs that execute in parallel on different computing devices (such as CPUs and GPUs) from different vendors (AMD, Intel, ATI, Nvidia etc.). The framework defines a language to write “kernels” in. These kernels are the functions which are to run on the different computing devices. In this post, I explain how to get started with OpenCL and how to make a small OpenCL program that will compute the sum of two lists in parallel. After that, I will show you how to write a GPU Cryptocurrency miner with the help of OpenCL based on the knowledge we just learned.

<!--more -->

### The kernel

The kernel is written in the OpenCL language which is a subset of C and has a lot of math and vector functions included. The kernel to perform the vector addition operation is defined below.

{% highlight cpp linenos %}
__kernel void vector_add(__global const int *A, __global const int *B, __global int *C) {
 
    // Get the index of the current element to be processed
    int i = get_global_id(0);
 
    // Do the operation
    C[i] = A[i] + B[i];
}
{% endhighlight %}


### The host program

The host program controls the execution of kernels on the computing devices. The host program is written in C, but bindings for other languages like C++ and Python exists. The OpenCL API is defined in the cl.h (or opencl.h for apple) header file. Below is the code for the host program that executes the kernel above on computing device. I will not go into details on each step as this is supposed to be an introductory article.

{% highlight cpp linenos %}
#include <stdio.h>
#include <stdlib.h>
 
#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif
 
#define MAX_SOURCE_SIZE (0x100000)
 
int main(void) {
    // Create the two input vectors
    int i;
    const int LIST_SIZE = 1024;
    int *A = (int*)malloc(sizeof(int)*LIST_SIZE);
    int *B = (int*)malloc(sizeof(int)*LIST_SIZE);
    for(i = 0; i < LIST_SIZE; i++) {
        A[i] = i;
        B[i] = LIST_SIZE - i;
    }
 
    // Load the kernel source code into the array source_str
    FILE *fp;
    char *source_str;
    size_t source_size;
 
    fp = fopen("vector_add_kernel.cl", "r");
    if (!fp) {
        fprintf(stderr, "Failed to load kernel.\n");
        exit(1);
    }
    source_str = (char*)malloc(MAX_SOURCE_SIZE);
    source_size = fread( source_str, 1, MAX_SOURCE_SIZE, fp);
    fclose( fp );
 
    // Get platform and device information
    cl_platform_id platform_id = NULL;
    cl_device_id device_id = NULL;   
    cl_uint ret_num_devices;
    cl_uint ret_num_platforms;
    cl_int ret = clGetPlatformIDs(1, &platform_id, &ret_num_platforms);
    ret = clGetDeviceIDs( platform_id, CL_DEVICE_TYPE_DEFAULT, 1, 
            &device_id, &ret_num_devices);
 
    // Create an OpenCL context
    cl_context context = clCreateContext( NULL, 1, &device_id, NULL, NULL, &ret);
 
    // Create a command queue
    cl_command_queue command_queue = clCreateCommandQueue(context, device_id, 0, &ret);
 
    // Create memory buffers on the device for each vector 
    cl_mem a_mem_obj = clCreateBuffer(context, CL_MEM_READ_ONLY, 
            LIST_SIZE * sizeof(int), NULL, &ret);
    cl_mem b_mem_obj = clCreateBuffer(context, CL_MEM_READ_ONLY,
            LIST_SIZE * sizeof(int), NULL, &ret);
    cl_mem c_mem_obj = clCreateBuffer(context, CL_MEM_WRITE_ONLY, 
            LIST_SIZE * sizeof(int), NULL, &ret);
 
    // Copy the lists A and B to their respective memory buffers
    ret = clEnqueueWriteBuffer(command_queue, a_mem_obj, CL_TRUE, 0,
            LIST_SIZE * sizeof(int), A, 0, NULL, NULL);
    ret = clEnqueueWriteBuffer(command_queue, b_mem_obj, CL_TRUE, 0, 
            LIST_SIZE * sizeof(int), B, 0, NULL, NULL);
 
    // Create a program from the kernel source
    cl_program program = clCreateProgramWithSource(context, 1, 
            (const char **)&source_str, (const size_t *)&source_size, &ret);
 
    // Build the program
    ret = clBuildProgram(program, 1, &device_id, NULL, NULL, NULL);
 
    // Create the OpenCL kernel
    cl_kernel kernel = clCreateKernel(program, "vector_add", &ret);
 
    // Set the arguments of the kernel
    ret = clSetKernelArg(kernel, 0, sizeof(cl_mem), (void *)&a_mem_obj);
    ret = clSetKernelArg(kernel, 1, sizeof(cl_mem), (void *)&b_mem_obj);
    ret = clSetKernelArg(kernel, 2, sizeof(cl_mem), (void *)&c_mem_obj);
 
    // Execute the OpenCL kernel on the list
    size_t global_item_size = LIST_SIZE; // Process the entire lists
    size_t local_item_size = 64; // Divide work items into groups of 64
    ret = clEnqueueNDRangeKernel(command_queue, kernel, 1, NULL, 
            &global_item_size, &local_item_size, 0, NULL, NULL);
 
    // Read the memory buffer C on the device to the local variable C
    int *C = (int*)malloc(sizeof(int)*LIST_SIZE);
    ret = clEnqueueReadBuffer(command_queue, c_mem_obj, CL_TRUE, 0, 
            LIST_SIZE * sizeof(int), C, 0, NULL, NULL);
 
    // Display the result to the screen
    for(i = 0; i < LIST_SIZE; i++)
        printf("%d + %d = %d\n", A[i], B[i], C[i]);
 
    // Clean up
    ret = clFlush(command_queue);
    ret = clFinish(command_queue);
    ret = clReleaseKernel(kernel);
    ret = clReleaseProgram(program);
    ret = clReleaseMemObject(a_mem_obj);
    ret = clReleaseMemObject(b_mem_obj);
    ret = clReleaseMemObject(c_mem_obj);
    ret = clReleaseCommandQueue(command_queue);
    ret = clReleaseContext(context);
    free(A);
    free(B);
    free(C);
    return 0;
}
{% endhighlight %}

You can also refer to <https://www.eriksmistad.no/getting-started-with-opencl-and-gpu-computing/> to get a more detailed getting started guide, and the above code is from that article.


### Compiling an OpenCL program

The easiest way is to create a Makefile and in this way, we don't need to remember those compile library and compilation parameters.

{% highlight makefile linenos %}
ifeq ($(shell uname -s),Darwin)
    CC ?= clang
    LDLIBS += -lcurl -framework OpenCL
else
    CC ?= gcc
    LDLIBS += -lOpenCL -lcurl
endif

CFLAGS += -c -std=c11 -Wall -pedantic -O2

TARGET = vector-addition

SOURCES = vector-addition.c

OBJECTS = $(patsubst %.c,%.o,$(SOURCES))

all: $(TARGET)

%.o: %.c
    $(CC) $(CFLAGS) -o $@ $<

$(TARGET): $(OBJECTS)
    $(CC) -o $@ $^ $(LDLIBS)

clean:
    rm -f $(TARGET) $(OBJECTS)

.PHONY: all clean
{% endhighlight %}

### GPU Miner

To write a GPU Miner with OpenCL is very easy now as all need to do is to implement an algorithm.
As an exapmle, a GPU Miner for blake2b (from <https://github.com/NebulousLabs/Sia-GPU-Miner/blob/master/sia-gpu-miner.cl>):

{% highlight cpp linenos %}
static inline ulong rotr64( __const ulong w, __const unsigned c ) { return ( w >> c ) | ( w << ( 64 - c ) ); }

__constant static const uchar blake2b_sigma[12][16] = {
    { 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15 } ,
    { 14, 10, 4,  8,  9,  15, 13, 6,  1,  12, 0,  2,  11, 7,  5,  3  } ,
    { 11, 8,  12, 0,  5,  2,  15, 13, 10, 14, 3,  6,  7,  1,  9,  4  } ,
    { 7,  9,  3,  1,  13, 12, 11, 14, 2,  6,  5,  10, 4,  0,  15, 8  } ,
    { 9,  0,  5,  7,  2,  4,  10, 15, 14, 1,  11, 12, 6,  8,  3,  13 } ,
    { 2,  12, 6,  10, 0,  11, 8,  3,  4,  13, 7,  5,  15, 14, 1,  9  } ,
    { 12, 5,  1,  15, 14, 13, 4,  10, 0,  7,  6,  3,  9,  2,  8,  11 } ,
    { 13, 11, 7,  14, 12, 1,  3,  9,  5,  0,  15, 4,  8,  6,  2,  10 } ,
    { 6,  15, 14, 9,  11, 3,  0,  8,  12, 2,  13, 7,  1,  4,  10, 5  } ,
    { 10, 2,  8,  4,  7,  6,  1,  5,  15, 11, 9,  14, 3,  12, 13, 0  } ,
    { 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15 } ,
    { 14, 10, 4,  8,  9,  15, 13, 6,  1,  12, 0,  2,  11, 7,  5,  3  } };

// Target is passed in via headerIn[32 - 29]
__kernel void nonceGrind(__global ulong *headerIn, __global ulong *nonceOut) {
    ulong target = headerIn[4];
    ulong m[16] = {    headerIn[0], headerIn[1],
                    headerIn[2], headerIn[3],
                    (ulong)get_global_id(0), headerIn[5],
                    headerIn[6], headerIn[7],
                    headerIn[8], headerIn[9], 0, 0, 0, 0, 0, 0 };

    ulong v[16] = { 0x6a09e667f2bdc928, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
                    0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179,
                    0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
                    0x510e527fade68281, 0x9b05688c2b3e6c1f, 0xe07c265404be4294, 0x5be0cd19137e2179 };

#define G(r,i,a,b,c,d) \
    a = a + b + m[blake2b_sigma[r][2*i]]; \
    d = rotr64(d ^ a, 32); \
    c = c + d; \
    b = rotr64(b ^ c, 24); \
    a = a + b + m[blake2b_sigma[r][2*i+1]]; \
    d = rotr64(d ^ a, 16); \
    c = c + d; \
    b = rotr64(b ^ c, 63);

#define ROUND(r)                    \
    G(r,0,v[ 0],v[ 4],v[ 8],v[12]); \
    G(r,1,v[ 1],v[ 5],v[ 9],v[13]); \
    G(r,2,v[ 2],v[ 6],v[10],v[14]); \
    G(r,3,v[ 3],v[ 7],v[11],v[15]); \
    G(r,4,v[ 0],v[ 5],v[10],v[15]); \
    G(r,5,v[ 1],v[ 6],v[11],v[12]); \
    G(r,6,v[ 2],v[ 7],v[ 8],v[13]); \
    G(r,7,v[ 3],v[ 4],v[ 9],v[14]);

    ROUND( 0 );
    ROUND( 1 );
    ROUND( 2 );
    ROUND( 3 );
    ROUND( 4 );
    ROUND( 5 );
    ROUND( 6 );
    ROUND( 7 );
    ROUND( 8 );
    ROUND( 9 );
    ROUND( 10 );
    ROUND( 11 );
#undef G
#undef ROUND

    if (as_ulong(as_uchar8(0x6a09e667f2bdc928 ^ v[0] ^ v[8]).s76543210) < target) {
        *nonceOut = m[4];
        return;
    }
}
{% endhighlight %}

Please note after BitMain released A3 ASIC for blake2b algorithm (<https://www.bitsonline.com/review-antminer-a3-blake-2b-asic-miner/>), it's not profitable anymore to mining blake2b coins with GPU.

Here, this code is only for learning GPU Miner.


### References

Blake2: <https://blake2.net/blake2.pdf>

RFC7693: <https://tools.ietf.org/html/rfc7693#ref-BLAKE2>
