cmake_minimum_required(VERSION 3.14)

find_file(CROSS_COMPILE riscv32-unknown-elf-gcc)
string(REGEX REPLACE "gcc$" "" CROSS_COMPILE ${CROSS_COMPILE})
set(CMAKE_ASM_COMPILER	${CROSS_COMPILE}gcc)
set(CMAKE_AR		${CROSS_COMPILE}ar)
set(CMAKE_ASM_COMPILER	${CROSS_COMPILE}gcc)
set(CMAKE_C_COMPILER	${CROSS_COMPILE}gcc)
set(CMAKE_CXX_COMPILER	${CROSS_COMPILE}g++)
set(CMAKE_CUSTOM_LINKER	${CROSS_COMPILE}gcc)
set(CMAKE_OBJCOPY		${CROSS_COMPILE}objcopy)
set(CMAKE_OBJDUMP		${CROSS_COMPILE}objdump)
set(CMAKE_SIZE			${CROSS_COMPILE}size)

project(fogml-riscv C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

option(BUILD_SHARED_LIBS OFF)
set(OPTS
		-ffreestanding
		-nostartfiles
		#-nostdlib
		-Wall -g
		-O2
		-Wdouble-promotion -Wfloat-conversion
		)

add_compile_options(${OPTS})

include_directories(include) # include printf_config

add_compile_definitions(
		NDEBUG
		PRINTF_INCLUDE_CONFIG_H=1
		)

# libraries
add_subdirectory(lib/fogml_sdk)
add_subdirectory(lib/printf)

# this project private files files
add_executable(${PROJECT_NAME}
		main.c
		)

target_link_libraries(${PROJECT_NAME}
		fogml_sdk
		printf
		)

target_link_options(${PROJECT_NAME} PRIVATE
		${OPTS}
		#-T${CMAKE_SOURCE_DIR}/linker.ld
		)

add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
		COMMAND ${CMAKE_SIZE} ${PROJECT_NAME}
		COMMENT "Size")
		
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
		COMMAND ${CMAKE_OBJCOPY} -O ihex ${PROJECT_NAME} ${PROJECT_NAME}.hex
		COMMENT "Hexdump")

