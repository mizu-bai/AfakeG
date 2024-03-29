# AfakeG

**大师大法好！**

## Introduction

AfakeG is a tool for Amesp output file visualization. It can convert the output file of geometry optimization task to Gaussian-like format.

## Features

- Optimization
- Frequencies
- Transition state
- IRC (WIP)

## Usage

To use the script `AfakeG.py`, make sure GaussView has been installed.

Here is an example in folder `example/`, type this command:

```bash
$ python3 /path/to/AfakeG.py H2O-opt-freq.aop
>>> Found geometry optimization step 1
>>> Found geometry optimization step 2
>>> Found geometry optimization step 3
>>> Found geometry optimization step 4
>>> Found frequency
大师大法好！
```

Then a new file `H2O-opt-freq_fake.out` will be generated, which can be loaded by GaussView.

## Acknowledgements

This work is inspired by:

- Tian Lu, OfakeG program, http://sobereva.com/soft/OfakeG (accessed Feb 22, 2024)
