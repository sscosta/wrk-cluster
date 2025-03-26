# wrk-cluster
Script that takes a csv with company names a number of workers and produces a map with the locations of the companies

# Input

CSV File with two columns:
    - Company : String
    - Num_Employees : Integer 

# Output

CSV File (companies_enriched.csv) with 5 columns: 
    - Company : String
    - Num_Employees : Integer
    - Address : String
    - Latitude : Double
    - Longitude : Double

For each company in the input file this output file contains the address and gps coordinates

2 html files: one with locations of the companies with clusters of companies that adapt as the user gets closer to the address, another file with circles with radius adjusted to the number of workers of the company.


# Usage

To install requirements run:

pip install -r requirements.txt

to run the program run:

python src/wrk-clusters.py