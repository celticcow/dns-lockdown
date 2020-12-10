#!/usr/bin/python3

import requests
import csv
import sys
from dnsconn import dnsconn


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

    dns_conn_list = list()

    with open(file1) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            tmp = dnsconn(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

            if(len(dns_conn_list) == 0):
                #first time in ... for loop will be going against 0
                dns_conn_list.append(tmp)
            else:
                for i in range(len(dns_conn_list)):
                    if(dns_conn_list[i] == tmp):
                        dns_conn_list[i].increment()
                    else:
                        dns_conn_list.append(tmp)
            #print(row[0])

    print("**************************")
    print(len(dns_conn_list))
    print("--------------------------")
    """
    connections = set()
    conn1 = dnsconn("172.31.124.18", "catch1", "10.9.52.197", "204.135.52.19", "17", "53", "Accept")
    conn2 = dnsconn("172.31.124.18", "catch1", "10.9.52.197", "204.135.52.19", "17", "53", "Accept")
    conn3 = dnsconn("172.31.124.18", "catch1", "10.9.52.19", "204.135.52.1", "17", "53", "Accept")

    connections.add(conn1)
    connections.add(conn2)
    connections.add(conn3)

    print(type(connections))
    print(type(conn1))

    print("----------------------------")
    print(connections)
    
    if(conn1 == conn1):
        print("equal")
    else:
        print("not")
    """

    print("end")
#end of main

if __name__ == "__main__":
    main()
#end of program