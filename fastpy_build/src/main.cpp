
#include<iostream>
#include<string>
#include"include/termcolor.hpp"
#include"include/builtin.hpp"










int main(){
    str name = input<str>("Input your name $");


int age = input<int>("Input your age $");


if (age > 17) {
log_info(name, true);

}

if (age > 15 && age < 18) {
log_warning(name, true);

}

if (age < 16) {
log_error(name, true);

}


}