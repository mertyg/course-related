cmake_minimum_required(VERSION 2.8.12.2)
project(project2)

set (CMAKE_CXX_STANDARD 11)
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp System.h Barista.h Cashier.h Barista.cpp Cashier.cpp System.cpp Customer.h Event.h Event.cpp Customer.cpp DivSystem.h DivSystem.cpp)
add_executable(project2 ${SOURCE_FILES} System.h Barista.h Cashier.h Customer.h Event.h Event.cpp DivSystem.h DivSystem.cpp)