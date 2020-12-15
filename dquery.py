#!/usr/bin/python3

import requests
import csv
import sys
from collections import Counter
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
    debug = 0

    file1 = "file1.csv"

    ## bulk list .. lot of dups
    dns_conn_list = list()

    with open(file1) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            tmp = dnsconn(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            dns_conn_list.append(tmp)
    #end of read file in

    if(debug == 1):
        print("**************************")
        print(len(dns_conn_list))
        ##print(Counter(dns_conn_list).keys())
        print(Counter(dns_conn_list).values())
        print("\n\n")
        print(len(Counter(dns_conn_list).keys()))
        print("--------------------------")
        ##print(my_counter)
    my_counter = Counter(dns_conn_list)

    uniq_conn = list()
    count_keys = 0

    for ele in my_counter:
        my_tmp_conn = dnsconn(ele.get_origin(), ele.get_rule_name(), ele.get_src(), ele.get_dst(), ele.get_proto(), ele.get_service(), ele.get_action(), my_counter[ele])

        if(debug == 1):
            print(ele.get_origin())
            print(ele.get_rule_name())
            print(ele.get_src())
            print(ele.get_dst())
            print(ele.get_proto())
            print(ele.get_service())
            print(ele.get_action())
            print(my_counter[ele])
            my_tmp_conn.conn_print()

        #print(ele.get_src() + " " + ele.get_dst())
        #print(ele, my_counter[ele])
        uniq_conn.append(my_tmp_conn)

    print(len(uniq_conn))
    uniq_conn[1001].conn_print()
    

    print("end")
#end of main

if __name__ == "__main__":
    main()
#end of program