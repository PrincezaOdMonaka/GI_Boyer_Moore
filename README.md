# GI_Boyer_Moore - Project 6

## Wrapper function
main.py

* -f &nbsp; &nbsp; &nbsp; Path to a file that is to be searched in, if not specified, all files from ./test directory will be used
* -p &nbsp; &nbsp; &nbsp; Patterns to be searched for searching, has to be specified, using space as a delimiter
* -h &nbsp; &nbsp; &nbsp; Heuristics to be used, has to be specified, using space as a delimiter and each pattern has to be one of the following:
    * **bc** - Bad Character Rule
    * **sgs** - Strong Good Suffix Rule
    * **wgs** - Weak Good SUffix Rule
    * **hs** - Heuristics 1 (Horspool Sunday 2)
    * **cr** - Heuristics 2 (Composite Rule)

## Benchmark
Used to generate charts and tables for comparison of following algorithms:
* Boyer-Moore - Heuristics 1 + Heuristics 2
* Boyer-Moore - Heuristics 1
* Boyer-Moore - Heuristics 2
* Boyer-Moore - Strong good suffix rule and bad character rule

benchmark.py
* -f &nbsp; &nbsp; &nbsp; Path to a file that is to be searched in, if not specified, all files from ./test directory will be used
* -p &nbsp; &nbsp; &nbsp; Patterns to be searched for searching, has to be specified, using space as a delimiter


## Unit tests

unit_tests.py

## Link to presentation
[Video presentation](https://youtu.be/FLkQJUnB2zc)
