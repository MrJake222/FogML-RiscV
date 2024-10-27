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
learning took 24s for learning pass (1-st pass, then it increases?) and 0.6s for inference pass:
```
processing...
learning...
DSP took 0.06 sec
RES took 0.00 sec
LOF took 23.98 sec
finished learning
[P 01] lof took: 24.0 sec
```
Most learning time is spent in `tinyml_lof_learn()` -- 99.8%.
Out of it 98% is calculating k-nearest neighbors O(n^2) with euclidean distance.
Modifications (learning time, applied separately):
- 24.0s -O3,
- 24.2s -Os,
- 23.4s no sqrt on distance,
- 14.3s taxicab distance,
-  8.5s with dummy +1 in loop,
-  0.4s no loop.

Random forest takes 0.1s to complete (including 0.06s for DSP).
Only -Os tested (-O2 random forest won't fit):
```
RF DSP took 0.06 sec
RF cls took 0.00 sec
RF class = 2
[P 01] rf took: 0.1 sec
```

## Other files
- `size.ods` -- size analysis of this code
- `tiny.pdf` -- tutorial how to make small binaries