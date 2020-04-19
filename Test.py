"""
This is a simple test file to convert the saple.clc
"""

from clc import convertcsv, convertclc
clc = "FRAC2_demo.clc"
csv = "FRAC2.csv"

# convertclc(clc)
convertcsv(csv, type='clc')
