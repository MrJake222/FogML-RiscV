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

#define DEBUG

#include "fogml_config.h"
float my_time_series[ACC_TIME_TICKS * ACC_AXIS];

#define LEARNING_SAMPLES    16

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
	//printf("heap start %p (size %d)\n", regions[0].start_addr, regions[0].size);
	lwmem_assignmem(regions);
	
	//printf("please input data\n");
	
	int ticks_stored = 0;
	int learning = 1;
	int learning_samples = 0;
	
	while (1) {
		my_time_series[ticks_stored * ACC_AXIS + 0] = readfloat();
		my_time_series[ticks_stored * ACC_AXIS + 1] = readfloat();
		my_time_series[ticks_stored * ACC_AXIS + 2] = readfloat();
		
		#ifdef DEBUG
			printf("storing tick %2d: %10.7f %10.7f %10.7f\n", ticks_stored,
				my_time_series[ticks_stored * ACC_AXIS + 0],
				my_time_series[ticks_stored * ACC_AXIS + 1],
				my_time_series[ticks_stored * ACC_AXIS + 2]);
		#endif
			
		ticks_stored++;

		if (ticks_stored == ACC_TIME_TICKS) {
			 printf("processing...\n");
			
			if (learning) {
				printf("learning...\n");

				fogml_learning(my_time_series);
				learning_samples++;

				if (learning_samples == LEARNING_SAMPLES) {
					learning_samples = 0;
					learning = 0;
					//printf("learning end\n");
				}
				
				printf("finished learning\n");
			}
			else {
				printf("classifying...\n");
				
				float score;
				fogml_processing(my_time_series, &score);				
				printf("LOF Score = %5.2f, %s\n", score, (score > 2.5f ? "fail" : "ok"));
			}
			
			int cl;
			fogml_classification(my_time_series, &cl);
			printf("RF class = %d\n", cl);
						
			ticks_stored = 0;
		}
	}
}

