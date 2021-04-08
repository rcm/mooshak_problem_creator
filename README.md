# mooshak_python
Something to help people to automatically create MOOshak problems in Python.

## Installing
You need to install markdown

    python -m pip install markdown

## Description
* Check `teste.txt` to have a look at the syntax
* Descriptions may use markdown. Check its syntax [here!](https://daringfireball.net/projects/markdown/syntax)
* You may use `parser.py` to read one or more files in the DSL and generate the problem
* You may look at `AASB_ficha2.py` and `CP_ficha3.py` to take a look of some examples
* Please feel free to install `feedback.tcl` on `~mooshak/packages/utils/` to have a nice feedback (courtesy of *Pedro Ribeiro*)
* After generating the folders containing the problems, simply copy them to `~mooshak/data/contests/YOUR_CONTEST/problems`

## DSL description

- NAME The name of the problem
- LETTER This is the name of the folder that stores the problems and what is stored in letter
- TESTS One or more tests; it ends with an END keyword
	- INPUT One line of input
	- LONGINPUT One or more lines of input; it ends with an END keyword
	- INPUTGEN An optional integer followed by a function (either a lambda function or the name of a function in an imported module)
	- FEEDBACK A feedback message for all inputs
	- POINTS How many points to award to each of the inputs
	- SHOW if present, it shows these tests to the user
- IMPORT The name of a module to import
- CODE One or more lines, ending with an END keyword.
       This creates a module and adds the code into it.
- SOLVER This may either be a lambda function or the name of a function in an imported module
- DESCRIPTION One or more lines, using the markdown syntax, ended with the END keyword
- POINTS Evenly distributes this number of points to *all tests*

A file may have several problems, the first keyword being NAME and finished by END.
## Example
```
NAME	problema 1
LETTER	F3Ex1
TESTS
	INPUT	10 20 30
	INPUT	70 80 90
	LONGINPUT
12
13
14
15
END
	FEEDBACK	This is the feedback for these three tests
END
TESTS
	INPUT	15 25 35
END

SOLVER	lambda s: sum(int(x) ** 2 for x in s.split())
DESCRIPTION
# Sum a list of numbers

Create a program that:

-  reads a bunch of numbers and
-  prints the sum of their squares

END
POINTS 200
END
```

## TODO
- Something to automatically add sample input and output to the description
- Add support to automatic correctors