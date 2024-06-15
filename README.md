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

## Menu Options
1. Read and clean data: Reads and cleans the data.
2. Print biggest handguns and longguns: Prints the state and year with the highest number of handguns and longguns.
3. Group by state and clean states: Groups data by state and cleans the data.
4. Merge datasets and calculate relative values: Merges the datasets and calculates relative values.
5. Analyze state data: Analyzes state data.
6. Create choropleth maps: Creates choropleth maps for permit percentage, handgun percentage, and longgun percentage.
7. Execute all steps: Executes all the above steps sequentially.

## Testing
To run the tests, use:
```bash
python -m unittest discover tests
```
