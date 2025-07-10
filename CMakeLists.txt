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
		-march=rv32i
		
		-O2
		-Wall -g
		-ffreestanding
		-nostartfiles
		
		# warns
		-Wdouble-promotion -Wfloat-conversion
		-Wno-strict-aliasing -Wno-unused-function
		
		# custom linker script
		-Wl,-T${CMAKE_SOURCE_DIR}/linker.ld
		
		# wrap malloc, dirty, no sdk support
		-Wl,--wrap=malloc,--wrap=free
		-fno-builtin-malloc
		
		# remove unused
		-fdata-sections -ffunction-sections
		-Wl,--gc-sections
		-Wl,-e_start
		)

add_compile_options(${OPTS})
add_link_options(${OPTS})

add_compile_definitions(
		NDEBUG
		PRINTF_INCLUDE_CONFIG_H=1
		)

# custom fpu support
option(XFPU "Enable a custom FPU support" OFF)
if(XFPU)
	add_compile_definitions(RISCV_XFPU)
endif(XFPU)

include_directories(include)

# libraries
add_subdirectory(lib/fogml_sdk)
add_subdirectory(lib/printf)
add_subdirectory(lib/lwmem)

# this project private files files
add_executable(${PROJECT_NAME}
		main.c
		src/random_forest_model.c
		)

target_link_libraries(${PROJECT_NAME}
		fogml_sdk
		printf
		lwmem
		)

add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
		COMMAND ${CMAKE_SIZE} ${PROJECT_NAME}
		COMMENT "Size")
		
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
		COMMAND ${CMAKE_OBJCOPY} -O ihex ${PROJECT_NAME} ${PROJECT_NAME}.hex
		COMMENT "Hexdump")

