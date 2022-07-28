
#include<iostream>
#include<string>
#include"include/termcolor.hpp"
#include"include/builtin.hpp"



#include "print.hpp"



void print_hello (){
str hello_text = "Hello, ";
log_info(hello_text);

};void print_text (str txt, bool endl = true){
log_info(txt, endl);

};



int main(){
    str world_text = "World!";


auto condition = true;


if (condition) {
print_hello();
print_text(world_text);

}

print("First FastPy run from IDE!!!!!!");


}