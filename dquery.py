#!/usr/bin/python3

import requests
import csv
import sys
import socket
import argparse
import ipaddress
from collections import Counter
from dnsconn import dnsconn
from dnspkt import SendDNSPkt
from zone import Zone
from network import Network

from cmdb_query import cmdb_query


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

def get_zone_list():
    debug = 1
    startZ = 1
    csvindex = 0

    list_of_zones = list()

    ##build list from file
    with open('zonedata.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            data = row[0]

            if(startZ == 1):
                #zone title
                ztemp = Zone(data)
                list_of_zones.append(ztemp)
                startZ = 0
            elif("Meta" in data):
                list_of_zones[csvindex].set_meta(data)
            elif("Policy" in data):
                list_of_zones[csvindex].set_policy(data)
            elif(data == "****"):
                #end of zone section
                startZ = 1
                csvindex = csvindex + 1
            else:
                tmp_net = Network(data)
                list_of_zones[csvindex].add_network(tmp_net)
        #end of for row
    #end of csv file

    return(list_of_zones)
#end of get_zone_list()

def zone_out(ip_addr, list_of_zones):
    debug = 1

    result = "NotFound"

    for z in list_of_zones:
        if(z.compare(ip_addr)):
            print("Match Found")
            print(z.get_name())
            result = z.get_name()
            print("******************")

    return(result)
#end of zone_out


def main():
    print("start of main")
    debug = 0

    #file1 = "edc-dns0203-2-7d.csv"
    parser = argparse.ArgumentParser(description='dns search')

    parser.add_argument("-f", required=True, help="file to import")
    parser.add_argument("-o", required=False, help="only show open conn results")

    args = parser.parse_args()

    #file1 = sys.argv[1]

    file1 = args.f

    list_of_zones = list()

    list_of_zones = get_zone_list()

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
    output = './results.txt'
    outwrite = open(output, 'w')

    google_out = './google.txt'
    gwrite = open(google_out, 'w')

    for i in range(len(uniq_conn)):
        is_fuzzy(uniq_conn[i])
        uniq_conn[i].conn_print()
        to_search = 0

        if(uniq_conn[i].get_msg() == "unknown dns"):
            tmp_src = uniq_conn[i].get_src()
            tmp_dst = uniq_conn[i].get_dst()

            if(checkDNSPortOpen(tmp_dst)):
                to_search = 1
                print("PORT OPEN")
                outwrite.write(tmp_src)
                outwrite.write(" -> ")
                outwrite.write(tmp_dst)
                outwrite.write(" OPEN ")
            else:
                to_search = 0
                if(args.o == 'y'):
                    pass
                else:
                    print("PORT CLOSED")
                    outwrite.write(tmp_src)
                    outwrite.write(" -> ")
                    outwrite.write(tmp_dst)
                    outwrite.write(" Closed ")
            
            if(args.o == 'y'):
                pass
            else:
                outwrite.write(" : ")
                outwrite.write(zone_out(tmp_src, list_of_zones))
                outwrite.write(" -> ")
                outwrite.write(zone_out(tmp_dst, list_of_zones))
                outwrite.write('\n')

            if(to_search == 1):
                q1 = cmdb_query()
                q2 = cmdb_query()

                q1.set_ip(tmp_src)
                q2.set_ip(tmp_dst)

                q1.query_cmdb()
                q2.query_cmdb()

                print("**************************************")
                print(q1.get_cmdb_info())
                print(q2.get_cmdb_info())

                outwrite.write(" *** CMDB ***\n")
                outwrite.write(q1.get_cmdb_info())
                outwrite.write("\n")
                outwrite.write(q2.get_cmdb_info())
                outwrite.write("\n *** END ***\n\n\n")
                print("--------------------------------------")
                

        elif(uniq_conn[i].get_msg() == "the googles"):
            tmp_src = uniq_conn[i].get_src()
            tmp_dst = uniq_conn[i].get_dst()
            
            gwrite.write(tmp_src)
            gwrite.write(" -> ")
            gwrite.write(tmp_dst)
            gwrite.write(" : ")
            gwrite.write(zone_out(tmp_src, list_of_zones))
            gwrite.write(" -> ")
            gwrite.write(zone_out(tmp_dst, list_of_zones))
            gwrite.write('\n')
            
            q1 = cmdb_query()
            q1.set_ip(tmp_src)
            q1.query_cmdb()

            gwrite.write("\n *** CMDB Source ***\n")
            gwrite.write(q1.get_cmdb_info())
            gwrite.write("\n *** END ***\n\n\n")
            

    
    outwrite.close()
    gwrite.close()

    print("end")
#end of main

if __name__ == "__main__":
    main()
#end of program