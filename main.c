extern unsigned int _bss_start, _bss_end;
extern unsigned int _data_start, _data_end, _data_src;
extern unsigned int _heap_start, _heap_end;

__attribute__ ((section(".boot")))
__attribute__ ((naked))
void _start(void) {
	// init stack to 0x10000
	// end of ram, grows downwards
    asm("lui sp, 0x10");
	// clear bss
	for (unsigned int* bss=&_bss_start; bss<&_bss_end; *bss++ = 0);
	// load data
	for (unsigned int* data=&_data_start, *idata=&_data_src; data<&_data_end; *data++ = *idata++);
	asm("j main");
}

#define UART0_BASE 	0x10010
#define UART_DATA 	(*(volatile unsigned int*)(UART0_BASE + 0))
#define UART_STATUS	(*(volatile unsigned int*)(UART0_BASE + 4))
#define UART_HAS_RX		(UART_STATUS & (1<<0))
#define UART_TX_EMPTY	(UART_STATUS & (1<<1))

void putchar_(char data) {
	while (!UART_TX_EMPTY);
	UART_DATA = data;
}

int readchar() {
	while (!UART_HAS_RX);
	return UART_DATA;
}

void delay_ms(int x) {
	// tuned manually
	// picorv32:  91 @ 24 MHz
	// vexriscv: 167 @ 16 MHz
	int i = 167 * x * 16;
	while(i--) asm("");
}

#define TIMER_BASE 	0x10018
#define TIME (*(volatile unsigned int*)(TIMER_BASE))

#include <printf/printf.h>
#include <lwmem/lwmem.h>
void* __wrap_malloc(size_t size) { return lwmem_malloc(size); }
void __wrap_free(void* ptr) { lwmem_free(ptr); }

//#define DEBUG
#define EOT 0x04

#include "fogml_config.h"
float my_time_series[ACC_TIME_TICKS * ACC_AXIS];

float readfloat() {
	// read little endian float
	unsigned int buf = 0;
	buf |= readchar();
	buf |= readchar() << 8;
	buf |= readchar() << 16;
	buf |= readchar() << 24;
	return *(float*)&buf;
}

int main() {
	lwmem_region_t regions[] = { { &_heap_start, (&_heap_end - &_heap_start) }, { NULL, 0 }	};
	lwmem_assignmem(regions);
	
	int ticks_stored = 0;
	int pass = 0;
	
	while (1) {
		my_time_series[ticks_stored * ACC_AXIS + 0] = readfloat();
		my_time_series[ticks_stored * ACC_AXIS + 1] = readfloat();
		my_time_series[ticks_stored * ACC_AXIS + 2] = readfloat();
		
		#ifdef DEBUG
			// cast to prevent warnings (yes, I know about double promotion here)
			printf("storing tick %2d: %10.7f %10.7f %10.7f\n", ticks_stored,
				(double)my_time_series[ticks_stored * ACC_AXIS + 0],
				(double)my_time_series[ticks_stored * ACC_AXIS + 1],
				(double)my_time_series[ticks_stored * ACC_AXIS + 2]);
		#endif
			
		ticks_stored++;

		if (ticks_stored == ACC_TIME_TICKS) {
			pass++;
			
			#ifdef DEBUG
			printf("pass %2d select action...\n", pass);
			#endif
			
			//int cl;
			char action = readchar();
			switch (action) {
				case 'R':
					// reservoir fill only (no learn)
					#ifdef DEBUG
					printf("filling...\n");
					#endif
					
					fogml_learning(my_time_series, 0);
					
					#ifdef DEBUG
					printf("finished filling...\n");
					#endif
					break;
				
				case 'L':
					// reservoir fill + learn
					printf("feature vector size: %d\n", FOGML_VECTOR_SIZE);
					printf("\nlearning...\n");
					fogml_learning(my_time_series, 1);
					printf("finished learning\n\n");
					break;
				
				case 'C':
					// classify
					#ifdef DEBUG
					printf("classifying...\n");
					#endif
					
					float score;
					fogml_processing(my_time_series, &score);				
					printf("LOF Score = %5.2f, %s\n\n", (double)score, (score > 2.5f ? "fail" : "ok"));
					
					break;
					
				case 'F':
					// forest
					//fogml_classification(my_time_series, &cl);
					//printf("RF class = %d\n", cl);
					break;
					
				default:
					printf("incorrect action: %c\n", action);
					break;
			}
			
			ticks_stored = 0;
			printf("%c\n", EOT);
		}
	}
}

