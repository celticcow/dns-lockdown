#!/usr/bin/python3

import requests
import csv
import sys
import socket
import ipaddress
from collections import Counter
from dnsconn import dnsconn
from dnspkt import SendDNSPkt


"""
Greg Dunlap / Celticcow

edc2fl : 204.135.120.136/.137
edc3fl : 204.135.120.134/.135
wtc1fl : 172.31.124.18/.19
wtc2fl : 172.31.104.14/.15
"""

def is_fuzzy(conn):
    """
    some statics
    199.82.243.70
    146.18.173.70
    """
    ip_addr = conn.get_dst()
    if(ip_addr == "199.82.243.70" or ip_addr == "146.18.173.70"):
        conn.set_msg("outdated_dns server")
        #print(" outdated_dns server ")
        #return(False)
    elif("192.82.243.70" in ip_addr):
        conn.set_msg("misconfig dns")
        #return(False)
    elif("199.112.46" in ip_addr):
        conn.set_msg("anycast set wrong")
        #return(False)
    elif("199.81.46" in ip_addr):
        conn.set_msg("anycast set wrong")
        #return(False)
    elif("198.112.46" in ip_addr):
        conn.set_msg("anycast set wrong")
        #return(False)
    elif("192.112.45.53" in ip_addr):
        conn.set_msg("anycast set wrong")
        #return(False)
    elif("192.116.46.53" in ip_addr):
        conn.set_msg("anycast set wrong")
        #return(False)
    elif("195.112.46.53" in ip_addr):
        conn.set_msg("anycast set wrong")
    elif("192.112." in ip_addr):
        conn.set_msg("anycast set wrong?")
    elif(ip_addr == "8.8.4.4" or ip_addr == "8.8.8.8"):
        conn.set_msg("the googles")
        #return(False)
    elif(ip_addr == "10.74.4.20" or ip_addr == "10.76.4.20"):
        conn.set_msg("PGH DNS Vip")
    elif(ip_addr == "10.72.11.11"):
        conn.set_msg("FXG dnshost.ground")
    elif(ip_addr == "199.81.11.53"):
        conn.set_msg("I2E dns vip")
    else:
        conn.set_msg("unknown dns")
        #return(True)
    try:
        if(ipaddress.ip_address(ip_addr)):
            pass
            ##conn.set_msg("INVALID IP")
    except:
        ## meta data or not a valid IP so do nothing
        conn.set_msg("INVALID IP")
#end_of_is_fuzzy

def checkDNSPortOpen(possible_dns):
    # replace 8.8.8.8 with your server IP!
    s = SendDNSPkt('loki.infosec.fedex.com', possible_dns)
    portOpen = False
    for _ in range(5): # udp is unreliable.Packet loss may occur
        try:
            s.sendPkt()
            portOpen = True
            break
        except socket.timeout:
            pass
    #if portOpen:
        
    #    print('port open!')
    #else:
    #    print('port closed!')
    return(portOpen)
#end of CheckDNSPortOpen

def main():
    print("start of main")
    debug = 0

    file1 = "file4.csv"

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
    output = '/home/gdunlap/Code/python/dns-lockdown/results.txt'
    outwrite = open(output, 'w')

    for i in range(len(uniq_conn)):
        is_fuzzy(uniq_conn[i])
        uniq_conn[i].conn_print()
        if(uniq_conn[i].get_msg() == "unknown dns"):
            tmp_dst = uniq_conn[i].get_dst()
            if(checkDNSPortOpen(tmp_dst)):
                print("PORT OPEN")
                outwrite.write(tmp_dst)
                outwrite.write(" OPEN\n")
            else:
                print("PORT CLOSED")
                outwrite.write(tmp_dst)
                outwrite.write(" Closed\n")
    
    outwrite.close()
    ##uniq_conn[50].conn_print()
    ##checkDNSPortOpen("8.8.3.8")
    
    ##uniq_conn[300].conn_print()
    
    

    print("end")
#end of main

if __name__ == "__main__":
    main()
#end of program