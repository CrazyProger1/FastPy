
#include<iostream>
#include<string>
#include"termcolor.hpp"








typedef std::string str;





template<typename T>
void log(const T &t, bool endl = false) {
    std::cout << t;
    if (endl) {
        std::cout << std::endl;
    }
    std::cout << termcolor::reset;
}


template<typename T>
void log_error(const T &t, bool endl = false) {
    std::cout << termcolor::on_red << termcolor::grey;
    log(t, endl);
}

template<typename T>
void log_info(const T &t, bool endl = false) {
    std::cout << termcolor::on_blue << termcolor::grey;
    log(t, endl);

}

template<typename T>
void log_warning(const T &t, bool endl = false) {
    std::cout << termcolor::on_yellow << termcolor::grey;
    log(t, endl);
}



void world (int a, bool b, str c, int d = (1 + 1) / 1 * 1 + (1 - 1)){
int abc = 10;
auto bbc = 20;
log('World');
log((1 + 1) * 1);

};



int main(){
    int a = 200;


auto b = 10;


int c;

auto d = a;


auto e = (20 - 10) + (d + 20) + a;


world(a, true, 'bla bla bla', 91239012039);


}