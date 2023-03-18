# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 19:48:38 2022

@author: culli
"""

import socket
import threading
import pika
import json

moduleDetails = {
    "SOFT8023": {
        "learning_outcomes": ["lo1", "lo2", "lo3"],
        "assessments": ["assess1", "assess2"],
        "programmes": ["cours1", "course2"]
    },
    "SOFT8009": {
        "learning_outcomes": ["lo1", "lo2", "lo3"],
        "assessments": ["assess1", "assess2"],
        "programmes": ["cours1", "course2"]
    }
}

LOCALHOST = "127.0.0.1"
PORT = 64002
global globalModuleID
globalModuleID = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

counter = 0
connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
channel = connection.channel()
channel.queue_declare(queue="hello")

def verifyModule(moduleID):
    moduleID = moduleID.upper()
    for x in moduleDetails.keys():
        if x == moduleID:
            setModuleID(moduleID)
            return "True"
    return "False"    
            
def setModuleID(moduleID):
    globalModuleID[threading.current_thread().getName()] = moduleID
    
    
def getModuleID(currentThread):
    return globalModuleID.get(currentThread)

class ClientThread(threading.Thread):

    def __init__(self, client_address, client_socket, identity):
        threading.Thread.__init__(self)
        self.c_socket = client_socket
        print("Connection no. " + str(identity))
        print("New connection added: ", client_address)

    def run(self):
        
        print("Connection from : ", clientAddress)
        
        while True:
            data = self.c_socket.recv(2048).decode()
            data = json.loads(data)
            currentThread = threading.current_thread().getName()
            
            if not data:
                break

            if data["1"] == 0:
                msg = data["0"]
                verify = verifyModule(msg)
                self.c_socket.send(bytes(verify, 'UTF-8'))
                print(currentThread, "Recieved Module")
                channel.basic_publish(exchange="", routing_key="hello", body=str((currentThread, getModuleID(currentThread), "Recieved Module")))
                
            elif data["1"] == 1:
                moduleID = getModuleID(currentThread)
                LO = moduleDetails[moduleID]
                LO = LO["learning_outcomes"]
                LO = json.dumps(LO)
                self.c_socket.send(bytes(LO, 'UTF-8'))
                print(currentThread, "Display Learning Outcomes")
                channel.basic_publish(exchange="", routing_key="hello", body=str((currentThread, getModuleID(currentThread), "Display Learning Outcomes")))
            
            elif data["1"] == 2:
                moduleID = getModuleID(currentThread)
                LO = moduleDetails[moduleID]
                LO = LO["programmes"]
                LO = json.dumps(LO)
                self.c_socket.send(bytes(LO, 'UTF-8'))
                print(currentThread, "Display Courses")
                channel.basic_publish(exchange="", routing_key="hello", body=str((currentThread, getModuleID(currentThread), "Display Courses")))
                
            elif data["1"] == 3:
                moduleID = getModuleID(currentThread)
                LO = moduleDetails[moduleID]
                LO = LO["assessments"]
                LO = json.dumps(LO)
                self.c_socket.send(bytes(LO, 'UTF-8'))
                print(currentThread, "Display Assessments")
                channel.basic_publish(exchange="", routing_key="hello", body=str((currentThread, getModuleID(currentThread), "Display Assessments")))
                
            elif data["1"] == 4:
                moduleID = getModuleID(currentThread)
                moduleDetails[moduleID]["learning_outcomes"].append(data["2"])
                LO = json.dumps(moduleDetails[moduleID]["learning_outcomes"])
                self.c_socket.send(bytes(LO, 'UTF-8'))
                print(currentThread, "Add Learning Outcome")
                channel.basic_publish(exchange="", routing_key="hello", body=str((currentThread, getModuleID(currentThread), "Add Learning Outcome")))
                
            elif data["1"] == 5:
                moduleID = getModuleID(currentThread)
                moduleDetails[moduleID]["learning_outcomes"][int(data["0"])-1] = (data["2"])
                LO = json.dumps(moduleDetails[moduleID]["learning_outcomes"])
                self.c_socket.send(bytes(LO, 'UTF-8'))
                print(currentThread, "Edit Learning Outcome")
                channel.basic_publish(exchange="", routing_key="hello", body=str((currentThread, getModuleID(currentThread), "Edit Learning Outcome")))
                
            elif data["1"] == 6:
                moduleID = getModuleID(currentThread)
                moduleDetails[moduleID]["learning_outcomes"].pop(int(data["0"])-1)
                LO = json.dumps(moduleDetails[moduleID]["learning_outcomes"])
                self.c_socket.send(bytes(LO, 'UTF-8'))
                print(currentThread, "Delete Learning Outcome")
                channel.basic_publish(exchange="", routing_key="hello", body=str((currentThread, getModuleID(currentThread), "Delete Learning Outcome")))
                
            elif data["1"] == 10:
                channel.basic_publish(exchange="", routing_key="hello", body=str((currentThread, getModuleID(currentThread), "Disconnect")))
                print(currentThread, "Disconnect")
                break

        print("Client at ", threading.current_thread().getName(), " disconnected...") 


print("Server started")
print("Waiting for client request..")


while True:
    server.listen(1)
    my_socket, clientAddress = server.accept()
    counter = counter + 1
    new_thread = ClientThread(clientAddress, my_socket, counter)
    new_thread.name = clientAddress
    channel.basic_publish(exchange="", routing_key="hello", body=str((clientAddress, "New Connection")))
    new_thread.start()