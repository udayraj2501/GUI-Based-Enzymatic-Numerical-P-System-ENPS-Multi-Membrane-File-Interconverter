#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// NOTE: Currently only arithmatic operations (+, -, /, *, ^) are supported

#define BLOCK_SIZE 1024
#define CEIL(a, b) ((a-1)/b +1)
#define BUFFER 256 // max number of characters in variables and membrane names

#define END 0
#define CON -1
#define VAR -2

// operators in order of precedence
#define LB  1   // (
#define EQ  2   // ==
#define NE  3   // !=
#define LT  4   // <
#define LE  5   // <=
#define GT  6   // >
#define GE  7   // >=
#define ADD 8   // +
#define SUB 9   // -
#define MUL 10  // *
#define MOD 11  // %
#define DIV 12  // /
#define EXP 13  // ^
#define NEG 14  // !
#define RB  15  // )

// limit for checking equality of 2 float values
#define LIMIT (float)0.00001

// NOTE: The cumulative length of production and distribution shouldn't be greater than INT_MAX

// check error
#define printError(func)                                                \
{                                                                       \
  cudaError_t E  = func;                                                \
  if(E != cudaSuccess)                                                  \
  {                                                                     \
    printf( "\nError at line: %d ", __LINE__);                          \
    printf( "\nError:  %s ", cudaGetErrorString(E));                    \
  }                                                                     \
} \

//for postfix expression
typedef struct {
    int type;
    int i, j;
    float value;

} PostfixElement;

typedef struct {
    int proportion; // is zero for eof
    int i, j; // position of variable in variables list
} DistFuncElement;

typedef struct {
    int i, j; // position of the enzyme in variables list
} EnzymeObject;

// return precedence of operators
__device__ int precedence(int op) {
    return op;
}

// used to parse constant from the input string, updates string iterator i
__device__ float parseConstant(const char exprParsed[], int *i, int end = INT_MAX) {
   
    float temp = 0;

    while(exprParsed[*i] >= '0' && exprParsed[*i] <= '9' && (*i) < end) {
        temp = temp*10 + (exprParsed[*i] - '0');
        (*i)++;

        if(exprParsed[*i] == '.') {
            (*i)++;
            float mul = 10;
            while(exprParsed[*i] >= '0' && exprParsed[*i] <= '9' && (*i) < end) {
                temp = temp + (exprParsed[*i] - '0')/mul;
                mul *= 10; 
                (*i)++;
            }
        }
    }

    return temp;
}

// used to parse variable from the input string, updates string iterator i
__device__ int* parseVarible(const char exprParsed[], int *i, int end = INT_MAX) {
    
    int* p = (int*) malloc(sizeof(int)*2);
    *i = *i+2;

    p[0] = parseConstant(exprParsed, i, end);
    (*i)++;
    p[1] = parseConstant(exprParsed, i, end);

    return p;
}

// used to parse operator from the input string, updates string iterator i
__device__ int parseOp(const char exprParsed[], int *i) {
    
    int temp = 0;

    switch(exprParsed[*i]) {
        case '+': 
            temp = ADD;
            break;
        case '-':
            temp = SUB;
            break;
        case '*':
            temp = MUL;
            break;
        case '/':
            temp = DIV;
            break;
        case '^':
            temp = EXP;
            break;
        case '%':
            temp = MOD;
            break;
        case '(':
            temp = LB;
            break;
        case ')':
            temp = RB;
            break;
        case '<':
            temp = LT; // <
            if(exprParsed[*i+1] == '=') { // <=
                temp = LE;
                (*i)++;
            }
            break;
        case '>':
            temp = GT; // >
            if(exprParsed[*i+1] == '=') { // >=
                temp = GE;
                (*i)++;
            }
            break;
        case '=':
            if(exprParsed[*i+1] == '=') { // ==
                temp = EQ;
                (*i)++;
            }
        case '!':
            temp = NEG; // !
            if(exprParsed[*i+1] == '=') { // !=
                temp = NE;
                (*i)++;
            }
            break;
    }

    (*i)++;
    return temp;
}

/* Kernel function :
*  Each thread is assigned a set of programs in the ENPS model. They perform the 
*  following tasks on their respective programs:
*  1. Parses production function string and converts it to postfix expression
*  2. Parses distribution function into easy to handle data structure 
*  3. Simulates program "steps" number of times
*/
__global__ void enps(char *prodFunction, int *posProd, char *distFunction, int *posDist, int *numberOfVariables, 
	float *variables, int steps, int numberOfPrograms, EnzymeObject *enzymes, PostfixElement *postfix, 
    DistFuncElement *distribution, int numberOfMembranes, int *stackOfOps, float *stackPostfixEval, 
    float *minVariableInPosFunc, float *valueOfProdFunc, float *sumOfProportions, bool *isProgramActive) {
    
    
    int ID = threadIdx.x; //index of each thread

    for(int id = ID; id < numberOfPrograms; id += blockDim.x) {
        /* 
        *  pbegin : beginnig of production function
        *  pend   : ending of production function
        *  dbegin : beginning of distibution function
        *  dend   : ending of distribution function
        *           of each thread's respective programs
        */

        int pbegin = posProd[id], pend = posProd[id+1], dbegin = posDist[id], dend = posDist[id+1];

        int top = -1; // top of stackOfOps
        int pos = 0; // pos of postfix expression
        int i;

        // converting production function to postfix expression

        for(i = pbegin; i < pend;) {
            if(prodFunction[i] == '$') { // parsing a variable
                int *p = parseVarible(prodFunction, &i, pend);
                postfix[pos+pbegin].type = VAR;
                postfix[pos+pbegin].i = p[0];
                postfix[pos+pbegin].j = p[1];
                pos++;
            }
            else if(prodFunction[i] >= '0' && prodFunction[i] <= '9') { // parsing a constant
                float constant = parseConstant(prodFunction, &i, pend);
                postfix[pos+pbegin].type = CON;
                postfix[pos+pbegin].value = constant;
                pos++;
            }
            else { // parsing an operator
                int op = parseOp(prodFunction, &i);  

                if(op == LB) { // is '('
                    //push to stack
                    top++;
                    stackOfOps[top + pbegin] = op;
                }
                else if(op == RB) { // is ')'
                    while(top != -1 && stackOfOps[top + pbegin] != LB) { //not '('
                        int temp = stackOfOps[top + pbegin];
                        top--;
                        postfix[pos+pbegin].type = temp;
                        pos++;
                    }
                    top--; // pop '('
                }
                else { // is operator
                    while(top != -1 && precedence(op) <= precedence(stackOfOps[top + pbegin])) {
                        int temp = stackOfOps[top + pbegin];
                        top--;
                        postfix[pos+pbegin].type = temp;
                        pos++;
                    }

                    // push to stack
                    top++;
                    stackOfOps[top + pbegin] = op;
                }
            }
        }

        // pop out any remaining elements in stackOfOps
        while(top != -1) {
            int temp = stackOfOps[top + pbegin];
            top--;
            postfix[pos+pbegin].type = temp;
            pos++;
        } 

        // add terminating character
        postfix[pos+pbegin].type = END;
        pos++; // (possible optimization, this anyways stores last index, eof not neccesary)

        int pos1 = 0; // position of distribution
        sumOfProportions[id] = 0; // sum of proportions of distribution function

        // extracting proportion and variable from distribution function 
        for(i = dbegin; i < dend; ) {

            distribution[pos1+dbegin].proportion = parseConstant(distFunction, &i, dend);
            i++;

            int *p = parseVarible(distFunction, &i, dend);

            distribution[pos1+dbegin].i = p[0];
            distribution[pos1+dbegin].j = p[1];

            sumOfProportions[id] += distribution[pos1+dbegin].proportion;

            pos1++;
            i++;

        }
        
        distribution[pos1+dbegin].proportion = 0; //terminating condition

    }

    __syncthreads();

    int step = 0;   
    
    // computation for given number of steps
    while(step < steps) {

        for(int id = ID; id < numberOfPrograms; id += blockDim.x) {

            int pbegin = posProd[id];

            int pos = 0;
            int top = -1;
            minVariableInPosFunc[id] = 1e300; // minimum value of variables in production function

            while(postfix[pos+pbegin].type != END) {
                
                if(postfix[pos+pbegin].type == CON) { // constant
                    top++;
                    stackPostfixEval[top + pbegin] = postfix[pos+pbegin].value;
                }
                else if(postfix[pos+pbegin].type == VAR) { // variable
                    int a = postfix[pos+pbegin].i-1, b = postfix[pos+pbegin].j-1;
                    top++;
                    stackPostfixEval[top + pbegin] =  variables[numberOfVariables[b] + a];
                    if(variables[numberOfVariables[b] + a] < minVariableInPosFunc[id])
                        minVariableInPosFunc[id] = variables[numberOfVariables[b] + a];
                }
                else { // operator
                    float a = stackPostfixEval[top + pbegin - 1], b = stackPostfixEval[top + pbegin], result = 0;
                    top--;
                    switch(postfix[pos+pbegin].type) {
                        case ADD:
                            result = a + b;
                            break;
                        case SUB:
                            result = a - b;
                            break;
                        case MUL:
                            result = a * b;
                            break;
                        case DIV:
                            result = a / b;
                            break;
                        case EXP:
                            result = powf(a, b);
                            break;
                        case MOD:
                            result = fmod(a, b);
                            break;
                        case LT:
                            result = (a < b)?1:0;
                            break;
                        case GT:
                            result = (a > b)?1:0;
                            break;
                        case LE:
                            result = (a <= b)?1:0;
                            break;
                        case GE:
                            result = (a >= b)?1:0;
                            break;
                        case EQ:
                            result = (fabs(a-b) < LIMIT)?1:0;
                            break;
                        case NE:
                            result = (a != b)?1:0;
                            break;
                        case NEG:
                            result = (!b);
                            break;
                    }
                    stackPostfixEval[top + pbegin] = result;
                }
                pos++;

            }

            if(minVariableInPosFunc[id] == 1e300) { // if no variable in production function
                minVariableInPosFunc[id] = -1;
            } 

            valueOfProdFunc[id] = stackPostfixEval[pbegin];
        }

        __syncthreads();

        for(int id = ID; id < numberOfPrograms; id += blockDim.x) {
         
            int a = enzymes[id].i - 1, b = enzymes[id].j - 1;
            isProgramActive[id] = (variables[numberOfVariables[b] + a] > minVariableInPosFunc[id] &&
                 variables[numberOfVariables[b] + a] > 0)?true:false; // for POS
        }

        __syncthreads();

        for(int id = ID; id < numberOfPrograms; id += blockDim.x) {

            int pbegin = posProd[id];

            if(isProgramActive[id]) {   // if production function is active
                int pos = 0;

                while(postfix[pos+pbegin].type != END) {
                    
                    if(postfix[pos+pbegin].type == VAR) {
                        int a = postfix[pos+pbegin].i-1, b = postfix[pos+pbegin].j-1;
                        variables[numberOfVariables[b] + a] = 0;
                    }
                    
                    pos++;
                }
            }
            
        }

        __syncthreads();

        for(int id = ID; id < numberOfPrograms; id += blockDim.x) {
        
            int dbegin = posDist[id];
            int pos1 = 0;
            // distribute among variables

            if(isProgramActive[id]) { // if production function is active
                while(distribution[pos1+dbegin].proportion != 0) { 
                    int a = distribution[pos1+dbegin].i - 1, b = distribution[pos1+dbegin].j - 1;
                    atomicAdd(variables + numberOfVariables[b] + a, valueOfProdFunc[id] * (((float)distribution[pos1+dbegin].proportion)/sumOfProportions[id]));
                    pos1++;
                }
            }
        }

        step++;
        __syncthreads();
    }
}


int main(int argc, char **argv) {

    FILE *ptr = fopen(argv[1], "r");
    
    int ctr;

    // Reading number of programs
    int numberOfPrograms;
    fscanf(ptr, "%d", &numberOfPrograms);

    // Reading number of membranes
    int numberOfMembranes;
    fscanf(ptr, "%d", &numberOfMembranes);

    // Reading the production functions
    int sizeOfProdFunction;
    fscanf(ptr, "%d", &sizeOfProdFunction);
    char *prodFunction = (char*)malloc(sizeOfProdFunction+1);
    fscanf(ptr, "%s", prodFunction);

    // Reading the position of production functions
    int sizeOfPosProd;
    fscanf(ptr, "%d", &sizeOfPosProd);
    int *posProd = (int*)malloc(sizeOfPosProd*sizeof(int));
    for(ctr=0; ctr<sizeOfPosProd; ctr++){
        fscanf(ptr, "%d", &posProd[ctr]);
    }


    // Reading the distribution functions
    int sizeOfDistFunction;
    fscanf(ptr, "%d", &sizeOfDistFunction);
    char *distFunction = (char*)malloc(sizeOfDistFunction+1);
    fscanf(ptr, "%s", distFunction);

    // Reading the position of distribution functions
    int sizeOfPosDist;
    fscanf(ptr, "%d", &sizeOfPosDist);
    int *posDist = (int*)malloc(sizeOfPosDist*sizeof(int));
    for(ctr=0; ctr<sizeOfPosDist; ctr++){
        fscanf(ptr, "%d", &posDist[ctr]);
    }

    // Reading the cumulative number of variables
    int sizeOfNumberOfVariables;
    fscanf(ptr, "%d", &sizeOfNumberOfVariables);
    int *numberOfVariables = (int*)malloc(sizeOfNumberOfVariables*sizeof(int));
    for(ctr=0; ctr<sizeOfNumberOfVariables; ctr++){
        fscanf(ptr, "%d", &numberOfVariables[ctr]);
    }
    int max_a = 1, max_b = ctr + 1; // programs with no enzymes are assigned with this enzyme indices 

    // Reading the variable values
    int sizeOfVariables;
    fscanf(ptr, "%d", &sizeOfVariables);
    sizeOfVariables++; // to accomadate very large enzyme (for programs without enzymes)
    float *variables = (float*)malloc(sizeOfVariables*sizeof(float));
    for(ctr=0; ctr<sizeOfVariables-1; ctr++){
        fscanf(ptr, "%f", &variables[ctr]);
    }
    variables[ctr] = 1e300; // programs with no enzyme is assigned this enzyme

    int sizeOfEnzymes = numberOfPrograms;
    EnzymeObject *enzymes = (EnzymeObject*)malloc(sizeOfEnzymes*sizeof(EnzymeObject)); // can directly assign size of programs
    for(ctr=0; ctr < sizeOfEnzymes; ctr++) {

        int a, b;
        fscanf(ptr, "%d", &a);
        fscanf(ptr, "%d", &b);

        if(a == -1 && b == -1){ // if no enzyme assigned to the program
            enzymes[ctr].i = max_a;
            enzymes[ctr].j = max_b;
        }
        else{
            enzymes[ctr].i = a;
            enzymes[ctr].j = b;
        }
    }



    // Reading the number of steps
    int numberOfIterations;
    fscanf(ptr, "%d", &numberOfIterations);

    char *d_prodFunction, *d_distFunction;
    int *d_posProd, *d_posDist, *d_numberOfVariables, *d_stackOfOps;
    float *d_variables, *d_stackPostfixEval, *d_minVariableInPosFunc, *d_valueOfProdFunc, *d_sumOfProportions;
    bool *d_isProgramActive;
    EnzymeObject *d_enzymes;
    PostfixElement *d_postfix;
    DistFuncElement* d_distribution;

    printf("Allocating memory\n");
    printError(cudaMalloc((void**) &d_prodFunction, sizeOfProdFunction * sizeof(char)));
    printError(cudaMalloc((void**) &d_posProd, sizeOfPosProd * sizeof(int)));
    printError(cudaMalloc((void**) &d_distFunction, sizeOfDistFunction * sizeof(char)));
    printError(cudaMalloc((void**) &d_posDist, sizeOfPosDist * sizeof(int)));
    printError(cudaMalloc((void**) &d_numberOfVariables, sizeOfNumberOfVariables * sizeof(int)));
    printError(cudaMalloc((void**) &d_variables, sizeOfVariables * sizeof(float)));
    printError(cudaMalloc((void**) &d_enzymes, sizeOfEnzymes * sizeof(EnzymeObject)));
    printError(cudaMalloc((void**) &d_postfix, sizeOfProdFunction * sizeof(PostfixElement)));
    printError(cudaMalloc((void**) &d_distribution, sizeOfDistFunction * sizeof(DistFuncElement)));
    printError(cudaMalloc((void**) &d_stackOfOps, sizeOfProdFunction * sizeof(int)));
    printError(cudaMalloc((void**) &d_stackPostfixEval, sizeOfProdFunction * sizeof(float)));
    printError(cudaMalloc((void**) &d_minVariableInPosFunc, numberOfPrograms * sizeof(float)));
    printError(cudaMalloc((void**) &d_valueOfProdFunc, numberOfPrograms * sizeof(float)));
    printError(cudaMalloc((void**) &d_sumOfProportions, numberOfPrograms * sizeof(float)));
    printError(cudaMalloc((void**) &d_isProgramActive, numberOfPrograms * sizeof(bool)));
    printf("Allocated memory\n");
        
    printError(cudaMemcpy(d_prodFunction, prodFunction, sizeOfProdFunction * sizeof(char), cudaMemcpyHostToDevice));
    printError(cudaMemcpy(d_posProd, posProd, sizeOfPosProd * sizeof(int), cudaMemcpyHostToDevice));
    printError(cudaMemcpy(d_distFunction, distFunction, sizeOfDistFunction * sizeof(char), cudaMemcpyHostToDevice));
    printError(cudaMemcpy(d_posDist, posDist, sizeOfPosDist * sizeof(int), cudaMemcpyHostToDevice));
    printError(cudaMemcpy(d_numberOfVariables, numberOfVariables, sizeOfNumberOfVariables * sizeof(int), cudaMemcpyHostToDevice));
    printError(cudaMemcpy(d_variables, variables, sizeOfVariables * sizeof(float), cudaMemcpyHostToDevice));
    printError(cudaMemcpy(d_enzymes, enzymes, sizeOfEnzymes * sizeof(EnzymeObject), cudaMemcpyHostToDevice));
    printf("Copied data\n");

    // Kernel call

    cudaEvent_t start, stop;
	cudaEventCreate(&start);
	cudaEventCreate(&stop);

	cudaEventRecord(start);

	printf("Entered Kernel\n");
    enps<<<1, BLOCK_SIZE>>>(d_prodFunction, d_posProd, d_distFunction, 
    	d_posDist, d_numberOfVariables, d_variables, numberOfIterations, numberOfPrograms, d_enzymes,  
        d_postfix, d_distribution, numberOfMembranes, d_stackOfOps, d_stackPostfixEval, d_minVariableInPosFunc, 
        d_valueOfProdFunc, d_sumOfProportions, d_isProgramActive);

    cudaDeviceSynchronize();
    cudaEventRecord(stop);
	cudaEventSynchronize(stop);
	float milliseconds = 0;
	cudaEventElapsedTime(&milliseconds, start, stop);

	printf("Exited kernel\n");
	printf("Time taken : %f ms\n", milliseconds);
    
    cudaMemcpy(variables, d_variables, sizeOfVariables * sizeof(float), cudaMemcpyDeviceToHost);

    char name[BUFFER+1];
    printf("\nComputed variable values:\n\n");
    
    // Output computed values

    printf("num_ps = {\n");
    for(int i = 0; i < numberOfMembranes; i++) {

        fscanf(ptr, "%s", name);
        printf("  %s:\n", name);
        
        printf("    var = {");
        int j;
        for(j = numberOfVariables[i]; j < numberOfVariables[i+1]; j++) {
            fscanf(ptr, "%s", name);
            if(name[0] == '$') {
                break;
            }
    		printf(" %s: %f, ", name, variables[j]);
        } 

        printf("}\n    E = {");

        for(; j < numberOfVariables[i+1]; j++) {
            fscanf(ptr, "%s", name);
            printf(" %s: %f, ", name, variables[j]);
        }

        printf("}\n");

    }
    printf("}\n");

    return 0;
}
