#pragma once

// requirements

#include<iostream>
#include<string>
#include"termcolor.hpp"



// builtin types

typedef std::string str;



// builtin functions

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

template<typename T>
T input(const str &t) {
    if (!t.empty()) {
        log(t);
    }

    T inp;
    if constexpr (std::is_same_v<std::decay_t<decltype(inp)>, str>)
        getline(std::cin, inp);
    else
        std::cin>>inp;

    return inp;
}
