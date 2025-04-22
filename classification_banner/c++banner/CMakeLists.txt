cmake_minimum_required(VERSION 3.14)
project(banner-app LANGUAGES CXX)

find_package(Qt6 COMPONENTS Widgets REQUIRED)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)

add_executable(banner-app main.cpp)

# Link Qt6 and libconfig++
target_link_libraries(banner-app Qt6::Widgets config++)

