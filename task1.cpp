#include <iostream>
#include <algorithm>
using namespace std;

//Assuming a left-aligned, right angled triangle with descending widths
//For example, a 3 x 3 triangle would look like this
// *
// * *
// * * *

//Assuming m x n refers to a width of m and height of n

void printTriangle(int m, int n) {
    for (int i = 1; i <= n; ++ i) {
        cout << string(min(i, m), '*') << endl;
    }
    cout << "" << endl; //For readability if multiple triangles are printed
}

int main() {
    printTriangle(3, 4);
    printTriangle(6, 6);
    return 0;
}

int main();