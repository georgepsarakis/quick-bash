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

### Comment

```bash
# Comments start with `#` and will be omitted in the output
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
```

### Backticks

```bash
(@exec 'date')
```

### For Loops

```bash
(@for a ls (@echo a (* 2 2)))
```

### If-Else

```bash
(@if-else (== 1 2) (@echo (@exec 'date')) (@exec 'ls'));
```

## ToDos

1. Documentation
2. Tests
3. More samples/examples

## Dependencies

  1. `pip install ply`
  2. `pip install argparse`
  3. `pip install pyparsing`
