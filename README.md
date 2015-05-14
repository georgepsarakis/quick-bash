quick-bash
==========

A micro-language that transcompiles to BASH. 

The aim is to make code more readable and easier to remember. 

## Why?

For the fun of it! 

Also, because most of us never remember how **if-else** conditionals and **for** loops are written in Bash.

## How?

Uses the Python lex-yacc implementation (<a href="http://www.dabeaz.com/ply/ply.html">ply</a>).

## Syntax

### Macros

#### Backticks

```bash
(@exec 'date')
```

#### For Loops

```bash
(@for a ls (@echo a (* 2 2)))
```

#### If-Else

```bash
(@if-else (== 1 2) (@echo (@exec 'date')) (@exec 'ls'));
```

#### Pipe
```bash
(@pipe (@echo 'hello') (@ssh host1))
```

#### BASH comment

```bash
(@comment 'this will be a comment in the output')
```

#### Raw BASH commands

```bash
(@raw 'cat myfile.txt | gzip --best - > myfile.txt.gz')
```

#### Arrays

```bash
(@let ARR (@range 1 10))
```

### Logical Operators

```bash
// [ 1 -eq 2 ]
(@-eq 1 2)
// [ 2 -gt 1 ]
(@-gt 2 1)
// [ 3 -ge 4 ]
(@-ge 3 4)
// [ 4 -lt 5 ]
(@-lt 4 5)
// [ 6 -le 8 ]
(@-le 6 8)
// [ 1 -ne 1 ]
(@-ne 1 1)
```

Python logical operators can be used for pre-calculated boolean output:

```bash
// false
(== 1 2)
// true
(> 2 3)
```

### Comments

C++ style comments are supported:

```cpp
// Single line comments start with // and will be omitted in the output
/* Multiline comments as well */
```

### Setting Variables

```bash
# Simple assignment
(@let A 'HELLO WORLD')

# Export variable
(@export A 'HELLO WORLD')
```

### Utilities/Functions

Functions start with `@`:

```bash
# Start with @
(@gzip 'myfile')

# Command-line parameters are passed with `~`
(@gzip ~9 'myfile')

# Long form options can be passed with ~~
(@grep ~~max-count 4 ~~regexp '[a-z][0-9]' a.txt)

# Logical expressions
(@eq? 1 2)
```

### Python Standard Library

Python functions can be invoked and the return value used as a string:

```bash
# Start with :
(@let CURRENT_TIME (:datetime.datetime.utcnow))
(@let A_DATETIME (:datetime.datetime.strptime "2014-05-06" "%Y-%m-%d"))
```

## To-dos

1. Documentation
2. More examples

## Dependencies

```pip install ply argparse pyparsing```
