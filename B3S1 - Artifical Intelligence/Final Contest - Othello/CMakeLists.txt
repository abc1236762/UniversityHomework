# cmake_minimum_required(VERSION <specify CMake version here>)
project(reversi C)

set(CMAKE_C_STANDARD 11)

add_executable(reversi main.c reversi.c)
