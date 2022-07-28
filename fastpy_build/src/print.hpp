#pragma once


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






auto b = 20;


