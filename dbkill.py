#!/usr/bin/env python3

'''
DBKILL
'''

import os

def main():  
    files = os.listdir()       
    if input("This will delete ALL database files in this directory. Continue? (y/n)") != "y":
        exit()
    for item in files:
        if item.endswith(".db"):
            os.remove(item)
    print("Removed!")
    
if __name__ == '__main__':
    main()