#!/usr/bin/python3

"""
class representing items from the splunk dump and connection parts
"""

class dnsconn(object):
    """
    origin | rule_name (direction) | src | dst | proto | service | action
    """
    #constructor
    def __init__(self, origin="127.0.0.1", rule_name="null", src="127.0.0.1", dst="127.0.0.1", proto="1", service="0", action="null", count=0, msg="not_set"):
        self.origin = origin
        self.rule_name = rule_name
        self.src = src 
        self.dst = dst
        self.proto = proto
        self.service = service
        self.action = action

        self.msg = "not_set"

        if(origin == "127.0.0.1"):
            self.count = 0
        elif(count == 0):
            self.count = 0
        else:
            self.count = count

    #modifiers
    def set_origin(self, origin):
        self.origin = origin
    
    def set_rule_name(self, rule_name):
        self.rule_name = rule_name
    
    def set_src(self, src):
        self.src = src
    
    def set_dst(self, dst):
        self.dst = dst
    
    def set_proto(self, proto):
        self.proto = proto

    def set_service(self, service):
        self.service = service
    
    def set_action(self, action):
        self.action = action
    
    def increment(self):
        self.count = self.count + 1

    def set_msg(self, msg):
        self.msg = msg

    #accessors
    def get_origin(self):
        return(self.origin)
    
    def get_rule_name(self):
        return(self.rule_name)
    
    def get_src(self):
        return(self.src)
    
    def get_dst(self):
        return(self.dst)
    
    def get_proto(self):
        return(self.proto)
    
    def get_service(self):
        return(self.service)
    
    def get_action(self):
        return(self.action)

    def get_count(self):
        return(self.count)

    def get_msg(self):
        return(self.msg)

    def conn_print(self):
        print(self.src + " -> " + self.dst + " : " + self.proto + "/" + self.service + " occured " + str(self.count) + " : " + self.msg, end="\n")
        
    
    #operators
    
    def __eq__(self, other):
        if((self.origin == other.origin) and (self.rule_name == other.rule_name) and (self.src == other.src) and (self.dst == other.dst) and (self.proto == other.proto) and (self.service == other.service) and (self.action == other.action)):
            return(True)
        else:
            return(False)
    
    def __hash__(self):
        return(hash((self.origin, self.rule_name, self.src, self.dst, self.proto, self.service, self.action)))
#end of class