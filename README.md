# FogML-RiscV

Based on [FogML-Arduino](https://github.com/tszydlo/FogML-Arduino).

## Compilation
This project uses CMake, so: `mkdir build`, `cd build`, `cmake ..`, `make`

## Usage
For now, you'll need dummy data from [FogML-Linux](https://github.com/MrJake222/FogML-Linux/).
- Generate data: `gendata/sim.py > data-sim-x24` (FogML-Linux),
- Redirect & send data: `./send.py < data-sim-x24`,
- Observe the model learn for 16, then ok for 8, and fail for 8 iterations.

### Send protocol
It sends raw float data in little-endian binary format. For each sample (3 axis x 4-byte float)
12 bytes is needed. The code echoes read data in human-readable format for verification.

### Results
In my [Risc-V survey](https://github.com/MrJake222/riscv-ice40) core VexRiscV (smprod_my, RV32I) @ 16MHz, -O2
learning took on average 28s for learning pass and 0.6s for inference pass.
Most learning time is spent in `tinyml_lof_learn()` -- 99.8%.
Out of it 98% is calculating k-nearest neighbors O(n^2) with euclidean distance.
Modifications (learning time, applied separately):
- 25s -O3,
- 24s no sqrt on distance,
- 15s taxicab distance,
- 9s with dummy +1 in loop,


## Other files
- `size.ods` -- size analysis of this code
- `tiny.pdf` -- tutorial how to make small binaries
