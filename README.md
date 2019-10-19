# CodeChecker :computer:

## Purpose
This repository assesses a program file and outputs the number of in-line, regular, and block comments. 
It also outputs the total number of lines in the program, and the total number of ```TODO:```.

## Test
I have created a bash script that runs sample tests for your convenience. Check ```run_test.bash``` in the repository to see the tests executed.

Run the test via ```bash run_test.bash```, and see the output in ```test_output.txt```.

## Run
You can run the code simply with ```python3 main.py -f <filename>```. 

Supported extensions/languages are currently:
- [x] Python
- [x] Java
- [x] Javascript
- [x] TypeScript
- [x] C
- [x] C++
- [x] C#
- [x] GoLang

However, it will work with any language that uses either ```//```, ```/*``` and ```*/``` OR ```#``` and ```'''``` for its comment syntax.

## Remarks
All Rights Reserved.
Copyright Gaurav Kumar Karna 2019
