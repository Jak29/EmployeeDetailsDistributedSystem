# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:44:11 2022

@author: culli
"""

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))

channel = connection.channel()
channel.queue_declare(queue="hello")

def callback(ch, methord, properties, body):
    toRemove = ("(", ")", "'", '"')
    print(" [x] Recieved %r" % body.decode().replace("(", "").replace(")", "").replace("'", "").replace('"', ""))
    
    
channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)


print("[*] Waiting for messages.")
channel.start_consuming()