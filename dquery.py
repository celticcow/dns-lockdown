#!/usr/bin/python3

import requests
import csv
import sys
import dnsconn


"""
Greg Dunlap / Celticcow

edc2fl : 204.135.120.136/.137
edc3fl : 204.135.120.134/.135
wtc1fl : 172.31.124.18/.19
wtc2fl : 172.31.104.14/.15
"""

def main():
    print("start of main")

    file1 = "file1.csv"

    with open(file1) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            print(row[0])



if __name__ == "__main__":
    main()
#end of program