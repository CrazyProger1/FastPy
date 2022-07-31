
#include<iostream>
#include<string>
#include"include/termcolor.hpp"
#include"include/builtin.hpp"


int sm(int a, int b) {
    return a + b;


};


int main() {
    sm(20, sm(10, sm(10, 20)));


}