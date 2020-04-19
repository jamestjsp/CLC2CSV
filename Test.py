"""
This is a simple test file to convert the saple.clc
"""

from clc import convertcsv, convertclc
clcfile = "FRAC2_demo.clc"
csvfile = "FRAC2.csv"

# convertclc(clcfile)
convertcsv(csvfile, type='vec', tags=['FIC-2100'])
