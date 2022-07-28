cmake_minimum_required(VERSION 3.20)
project(src)

set(CMAKE_CXX_STANDARD 20)

add_executable(src main.cpp print.hpp include/builtin.hpp)
