<div align = center>
<img src="https://i.postimg.cc/50yrsgpH/megalogo-smaller.jpg" width=200px> <br>

<h1>megaLogo</h1>

![GitHub License](https://img.shields.io/github/license/meganstumpf/megalogo?style=flat)
![GitHub Release Date](https://img.shields.io/github/release-date/meganstumpf/megalogo?style=flat)
![GitHub Release](https://img.shields.io/github/v/release/meganstumpf/megalogo?style=flat)
</div>

## Table of Contents
- [megalogo](#megalogo)
  - [Table of Contents](#table-of-contents)
    - [Introduction and Overview](#introduction-and-overview)
    - [Software Requirements and Dependencies](#software-requirements-and-dependencies)
    - [Installation](#installation)
    - [General Usage](#general-usage)

* script: [megalogo.py](https://github.com/meganstumpf/megalogo/blob/master/code/megalogo.py)  
  


### Introduction and Overview
-----------------------------
This repository contains code to create large logoplots for deep mutational scanning data with customizability. These plots visualize the absence/presence of amino acid mutations at all mutated codon positions above specified quality and count filters. Made in collaboration with [Tonya Brunetti](https://github.com/tbrunetti). 

#### Example: 
<div align = left>
<img src = "https://github.com/meganstumpf/megalogo/blob/master/outputs/sample.png?raw=true" width = 400px>
</div>


### Software Requirements and Dependencies
------------------------------------------  

For script `megalogo.py`:  

* [python >= v3.9](https://www.python.org/downloads/)  
* [pandas](https://pandas.pydata.org/docs/getting_started/install.html#installing-from-pypi)  
* [numpy](https://numpy.org/install/)  
* [matplotlib](https://matplotlib.org/stable/users/installing/index.html#installation)
* [logomaker](https://pypi.org/project/logomaker/) 


### Installation
-----------------  
There is no installation required, please just clone the repository:  
```
git clone https://github.com/meganstumpf/megalogo.git
```  

Then cd into the `code` directory where all scripts will be present:  
```
cd code  
```

### General Usage  
-----------------  

For using the `megalogo.py` script, general use is as follows:  

```
python3 megalogo.py --input ../test_data/megalogo_test_data.csv --sampleName sample --annotConfig ../ref/annotations_config.csv --refAA ../ref/wildtype.csv --codonStartPos 1 --output ../outputs/sample.png  
```
<br/>  

Which can also be executed by running the following within the `code` directory:

```
./run_test_data.sh
```

For all possible arguments available, you can run the following:  

```
python3 megalogo.py --help
```
which will show the following options and their defaults:  

```
usage: megalogo.py [-h] --input INPUT [--sampleName SAMPLENAME] [--annotConfig ANNOTCONFIG] [--codonStartPos CODONSTARTPOS] [--codonEndPos CODONENDPOS]
                   [--aaSpacing AASPACING] [--minAnnotLabel MINANNOTLABEL] [--refAA REFAA] --output OUTPUT

Generates logo plot for predefined input matrix

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT
                        Path to input csv matrix containing data to plot (default: None)
  --sampleName SAMPLENAME
                        String indicating the name to give to sample (default: sample_1)
  --annotConfig ANNOTCONFIG
                        Path to csv containing annotations. Example file located in ref folder of github repo (default: None)
  --codonStartPos CODONSTARTPOS
                        The position of which codon position you want to start at (must be present in your csv matrix provided to --input; default is to plot every
                        position in your matrix) (default: None)
  --codonEndPos CODONENDPOS
                        The position of which codon position you want to end at (must be present in your csv matrix provided to --input; default is to plot every
                        position in your matrix) (default: None)
  --aaSpacing AASPACING
                        The number of amino acids to show per line on the logo plot (default: 65)
  --minAnnotLabel MINANNOTLABEL
                        The minimum length of consecutive amino acids under an annotation bar; anything smaller (non-inclusive) than this value will not have text
                        written in the bar, to help prevent text from overflowing into margins (default: 7)
  --refAA REFAA
                        Path to csv containing reference amino acids with POSITION and REF_AA columns (default: None)
  --output OUTPUT
                        Path to save the output logoplot image (default: None)
```

 
