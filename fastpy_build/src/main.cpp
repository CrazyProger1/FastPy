
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

else if (age > 15) {
log_warning(name, true);

}

else {
log_error(name, true);

}


}