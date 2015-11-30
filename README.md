# The Center Star Method for MSA

Before the beginning, I recommend you to know some basic of pairwise alignment algorithms such as Needleman-Wunch algorithm because I use to calculate pairwise alignments by Needleman-Wunch.

## What is the center star method?

### The Center Star Algorithm:
1. Find Sc maximizing Σic D(Sc, Si ).(Note: Some resources say minimizing)
2. Iteratively construct the multiple alignment Mc:
    1. Mc={Sc}
    2. Add the sequences in S\{Sc} to Mc one by one so that the induced alignment aMc(Sc, Si) of every newly added sequence Si with Sc is optimal. Add spaces, when needed, to all pre-aligned sequences.

### What is the running complexity?
`Combination(k,2) * O(n^2) = O(k^2 * n^2)`

### Merging example
```
AC-BC
DCABC
```    
+
```
AC--BC
DCAABC
```
=
```
AC--BC
DCA-BC
DCAABC
```

## File format

The format of the input file must be this way;

```
{matchScore},{mismatchScore},{gapScore}
{sequence1}
{sequence2}
{sequence3}
.
.
.
{sequenceN}
```

for example; whether matchScore = 1, mismatchScore = -1, gapScore = -4 and four strings, the file should be;

```
1,-1,-4
MPE
MKE
MSKE
SKE
```

## Usage

`python cstar.py inputfile outputfile`

## TODOs

* Score matrix support []
