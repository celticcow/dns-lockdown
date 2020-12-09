#!/usr/bin/python3

import sys
import requests

def main():
    print("__start__")

    var1 = "127.0.0.1"
    var2 = "8.8.8.8"
    var3 = "53"

    print(hash((var1,var2,var3)))

if __name__ == "__main__":
    main()
#end