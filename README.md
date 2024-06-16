# Gunstats

## Overview
This project analyzes firearm statistics in the United States. It includes functionality to read, clean, process, and visualize data related to firearm permits and requests by year and statels.

## Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/mlavinv117/gunstats
cd gunstats
pip install -e .
```

## Usage
To run the main script, use:
```bash
python -m gunstats.main
```
Or:
```bash
python3 -m gunstats.main
```

## Menu Options
0. Execute all exercises
1. Exercise 1: Read and clean data
2. Exercise 2: Data processing
3. Exercise 3: Data grouping
4. Exercise 4: Time Analysis
5. Exercise 5: State analysis
6. Exercise 6: Choropleth maps
7. Exit program

## Testing
To run the tests, use:
```bash
python -m unittest discover tests
```
Or:
```bash
python3 -m unittest discover tests
```

## Note
The module code assumes that gunstats is run from its installation folder,
as per indicated in the installation step "cd gunstats".
It directly calls the data from the relative path "./data/".
To further increase the portabillity of the code, collaborations are welcome!
Contact mlavinv@uoc.edu to be added to the contributors and create a pull
request. Thank you!
