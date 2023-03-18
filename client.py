# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 19:48:15 2022

@author: culli
"""

import socket
import json
import sys

SERVER = "127.0.0.1"
PORT = 64002

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER, PORT))


while True:
    
    info = {0:"", 1:"", 2:""}
    moduleID = (input("What is the module id: "))
    info[0] = moduleID
    info[1] = 0
    info = json.dumps(info)
    sock.sendall(bytes(info, 'UTF-8'))
    data = sock.recv(1024).decode()
    if data == "False":
        print("Invaid Input")
        continue
    
    while True:
        info = {0:"", 1:"", 2:""}
        choice1 = input("(L)earning Outcomes, (C)ourses, (A)ssessments or e(X)it? ").upper()
        info[0] = choice1
        
        if choice1 == "X":
            info[1] = 10
            info = json.dumps(info)
            sock.sendall(bytes(info, 'UTF-8'))
            sys.exit()
        elif choice1 == "L":
            info[1] = 1
        elif choice1 == "C":
            info[1] = 2
        elif choice1 == "A":
            info[1] = 3
        else: 
            print("Invalid Input")
            continue
    
        info = json.dumps(info)
        sock.sendall(bytes(info, 'UTF-8'))
        data2 = sock.recv(1024)
        data2 = json.loads(data2)
        for x in range(len(data2)):
            print(f"{x+1}.", data2[x])
        
        if choice1 == "L": 
            while True:

                info = {0:"", 1:"", 2:""} 
                choice2 = input("(A)dd, (E)dit, (D)elete or (R)eturn? ").upper()
                
                if choice2 == "R":
                    break
                
                elif choice2 == "A":
                    newLO = input("Enter new LO description: ")
                    info[1] = 4
                    info[2] = newLO
                    info = json.dumps(info)
                    sock.sendall(bytes(info, 'UTF-8'))
                    data2 = sock.recv(1024)
                    data2 = json.loads(data2)
                    for x in range(len(data2)):
                        print(f"{x+1}.", data2[x])
                
                elif choice2 == "E":
                    while True:
                        choice3 = input("Enter LO #: ")
                        try:
                            if int(choice3) > len(data2) or int(choice3) <= 0:
                                print("Invalid input")
                            else: 
                                break
                        except:
                            print("Invalid input")
                    updatedLO = input("Enter new LO Description: ")
                    info[0] = choice3
                    info[1] = 5
                    info[2] = updatedLO
                    info = json.dumps(info)
                    sock.sendall(bytes(info, 'UTF-8'))
                    data2 = sock.recv(1024)
                    data2 = json.loads(data2)
                    for x in range(len(data2)):
                        print(f"{x+1}.", data2[x])
                    
                
                elif choice2 == "D":
                    while True:
                        choice3 = input("Enter LO #: ")
                        try:
                            if int(choice3) > len(data2) or int(choice3) <= 0:
                                print("Invalid input")
                            else: 
                                break
                        except:
                            print("Invalid input")
                    info[0] = choice3
                    info[1] = 6
                    info = json.dumps(info)
                    sock.sendall(bytes(info, 'UTF-8'))
                    data2 = sock.recv(1024)
                    data2 = json.loads(data2)
                    for x in range(len(data2)):
                        print(f"{x+1}.", data2[x])
                
                else:
                    print("Invalid Input")
                    continue
                
        
    
    
    
sock.close()