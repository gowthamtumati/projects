// C program to find GCD of two numbers 
#include <stdio.h> 
  
// Recursive function to return gcd of a and b 
int gcd(int a, int b) 
{ 
    int gcd = 1;
    for(int i = 2; i <= a && i <= b; ++i)
    {
        // Checks if i is factor of both integers
        if(a % i == 0 && b % i == 0)
            gcd = i;
    }
    return gcd;
} 
  
// Driver program to test above function 
int main() 
{ 
    int a = 98, b = 56; 
    printf("GCD of %d and %d is %d ", a, b, gcd(a, b)); 
    return 0; 
} 
