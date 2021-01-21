#!/usr/bin/python3

import requests
import json

class cmdb_query(object):
    """
    query cmdb to determine info of hardware

    sys_class_name //OS
    name //hostname
    fqdn //fully qualified domain name
    location //Data Center info
    ip_address //ip info we orig queried
    support_group //sysadmin pdsm group
    support_group.manager // manager over support group
    """

    #constructor
    def __init__(self, ip="127.0.0.1"):
        self.ip = ip
        self.sys_class_name = "NA"
        self.name = "N/A"
        self.fqdn = "N/A"
        self.location = "N/A"
        self.support_group = "N/A"
        self.support_group_manager = "N/A"

        http_proxy = "199.82.243.100:3128"
        https_proxy = "199.82.243.100:3128"

        self.proxyDict = {
            "http" : http_proxy,
            "https" : https_proxy
        }

    #accessors
    def get_ip(self):
        return(self.ip)
    
    def get_sys_class_name(self):
        return(self.sys_class_name)
    
    def get_name(self):
        return(self.name)
    
    def get_fqdn(self):
        return(self.fqdn)
    
    def get_location(self):
        return(self.location)
    
    def get_support_group(self):
        return(self.support_group)
    
    def get_support_group_manager(self):
        return(self.support_group_manager)
    
    def print_cmdb(self):
        out_str = "{name : " + self.name + ", ip : " + self.ip + ", fqdn : " + self.fqdn + ", location : " + self.location + ", Sys_Class_Name : " + self.sys_class_name + ", Support Group : " + self.support_group + ", Support Group Manager : " + self.support_group_manager + "}"
        print(out_str)
    
    def get_cmdb_info(self):
        out_str = "{name : " + self.name + ", ip : " + self.ip + ", fqdn : " + self.fqdn + ", location : " + self.location + ", Sys_Class_Name : " + self.sys_class_name + ", Support Group : " + self.support_group + ", Support Group Manager : " + self.support_group_manager + "}"
        return(out_str)

    #modifiers
    def set_ip(self, ip):
        self.ip = ip
    
    def set_sys_class_name(self, sys_class_name):
        self.sys_class_name = sys_class_name
    
    def set_name(self, name):
        self.name = name
    
    def set_fqdn(self, fqdn):
        self.fqdn = fqdn
    
    def set_location(self, location):
        self.location = location
    
    def set_support_group(self, support_group):
        self.support_group = support_group
    
    def set_support_group_manager(self, support_group_manager):
        self.support_group_manager = support_group_manager
    
    #worker functions
    def query_cmdb(self):
        if(self.ip == "127.0.0.1"):
            return
        else:
            #run query.
            fields = '&fields=sys_class_name,name,fqdn,sys_id,location,ip_address,support_group,support_group.manager&display_value=true'

            url = 'https://pdsmdev08.service-now.com/api/x_hclfe_cmdb_api/hardware/by_ip?ip_address=' + self.ip + fields

            key = {}
            with open('key.json', 'r') as f:
                key = json.load(f)

            #print(key['usr'])
            #print(key['pwd'])

            headers = {"Accept" : "application/json"}

            # Do the HTTP request
            response = requests.get(url, auth=(key['usr'], key['pwd']), headers=headers, proxies=self.proxyDict)

            ####
            if(response.status_code != 200):
                print("Not return code 200 ", end=" ")
                print(response.status_code)
                #print("Header returned ", end=" ")
                #print(response.headers)
                #print("Error Response ", end=" ")
                #print("{}")
                ##print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
                #exit()
                self.name = "N/A"
                self.fqdn = "N/A"
                self.location = "N/A"
                self.sys_class_name = "N/A"
                self.support_group = "N/A"
                self.support_group_manager = "N/A"
            else:
                #print("Status :", response.status_code, "headers: ", response.headers)
                #print("Response : ", end="\n")
                #print(response.json())
                tmp = response.json()
                #print("---------------------------------\n")
                #print(tmp['result']['Hardware Details'][0]['name'])
                #print(tmp['result']['Hardware Details'][0]['location'])
                #print(tmp['result']['Hardware Details'][0]['support_group'])
                #print(tmp['result']['Hardware Details'][0]['support_group.manager'])
                #print("---------------------------------\n")
                #print("\n\n")
                #print("Cookies:", response.cookies)

                self.name = tmp['result']['Hardware Details'][0]['name']
                self.fqdn = tmp['result']['Hardware Details'][0]['fqdn']
                self.location = tmp['result']['Hardware Details'][0]['location']
                self.sys_class_name = tmp['result']['Hardware Details'][0]['sys_class_name']
                self.support_group = tmp['result']['Hardware Details'][0]['support_group']
                self.support_group_manager = tmp['result']['Hardware Details'][0]['support_group.manager']

#end of class