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

### Setting Variables

```bash
# Simple assignment
(@let A 'HELLO WORLD');
# Export variable
(@export A 'HELLO WORLD');
```

### Utilities/Functions

```bash
# Start with @
(@gzip 'myfile');
# Command-line parameters
(@gzip ~9 'myfile');
```

### Backticks

```bash
(@exec 'date');
```
### If-Else

```bash
(@if-else (== 1 2) (@echo (@exec 'date')) (@exec 'ls'));
```

## TODO

1. Documentation
2. Tests
3. More samples/examples

## Dependencies

  1. `pip install ply`
  2. `pip install argparse`
