# C- Compiler

Every compiler is composed of a __Front-End__ and a __Back-End__.

* __Front-End__
  * Recognize legal programs
  * Report errors
  * Produce Intermediary Representation (IR)
  * Preliminary storage

* __Back-End__
  * Translate IR to machine code
  * Choose instructions to implement each operation
  * Decide which values will be in the registers

## Front-End

* __Scanner__ - Lexical Analyzer
  * Takes in source code and outputs token stream.
    * Uses regular expressions grammar (implemented through DFA) to recognize tokens and their type.
    * Number of automatons used is the number of token types (reserved words, identifiers, comments, etc...)
  * Report errors
