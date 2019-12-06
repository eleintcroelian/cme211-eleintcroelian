1.1 

A: 3
B: 2 Index outside of static array size
C: 3 
D: 1 type of variable declared as int first
E: 2 since char can store up to 255 values with 8 bits, when the value is more than 255, it overflows. also, (p+1) converts the variable to be printed to an int implicitly, so the printed value would be 1
F: Since computer architectures are designed to hold finite significant digits of numbers, the precision of arithmetic operations have a limit. Computing the product of small numbers may not be accurate if the rounding errors accumulate at a considerable level. So the programmer should be careful about the rounding-off errors.

1.2

A: Stack is a smaller memory portion compared to heap in which the local scopes of functions and classes are erased after called. It is like an operating area for the total memory. Heap on the other hand is larger and limited by the computer hardware, where large data can be stored and the collecting memory is controlled by the programmer.

B: The printed values are different because the pointer to the triplet was pointing a memory in the stack and after the local scope of the function, its allocation was erased. When the program returned to main(), it looked for the memory pointed, since it was erased. This is undefined behavior and the function should have stored its variables in heap.

C: As we use new, the variable is now stored in heap and it won't be erased after the function scope ends. Thus, the program is working as desired.

D: Since we used new, but did not use delete to erase the allocated memory after the variables use ended, there will be a memory leak.

E: If the programmer used the vector class instead of static arrays, which takes care of memory allocation automatically, there wouldn't be a need of new and delete[]
