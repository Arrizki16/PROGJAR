from ast import arg
from multiprocessing import connection
import sys
import socket   
import logging
import json
import os
import ssl
import threading
import time
from time import sleep

list_player = dict()

with open ('../../data.txt', 'r') as f:
    lines = f.readlines()
    index = 1
    for line in lines:
        data_split = line.strip().split(", ")
        list_player[index] = {}
        for comma in data_split:
            data_split_comma = comma.split("=")
            list_player[index][data_split_comma[0]] = data_split_comma[1]
        index+=1


def versi():
    return "versi 0.0.1"


def proses_request(request_string):
    cstring = request_string.split(" ")
    hasil = None
    try:
        command = cstring[0].strip()
        if (command == 'getdatapemain'):
            logging.warning("getdata")
            nomorpemain = cstring[1].strip()
            try:
                logging.warning(f"data {nomorpemain} ketemu")
                hasil = list_player[int(nomorpemain)]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    
    sleep(0.1)
    return hasil


def handle_request(connection, client_address):
    data_received=""
    selesai=False
    while True:
        data = connection.recv(32)
        logging.warning(f"received {data}")
        if data:
            data_received += data.decode()
            if "\r\n\r\n" in data_received:
                selesai=True

            if (selesai==True):
                hasil = proses_request(data_received)
                logging.warning(f"hasil proses: {hasil}")
                hasil = serialisasi(hasil)
                hasil += "\r\n\r\n"
                connection.sendall(hasil.encode())
                selesai = False
                data_received = ""
                break

        else:
           logging.warning(f"no more data from {client_address}")
           break


def serialisasi(a):
    serialized =  json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized

def run_server(server_address):
    cert_path = os.getcwd() + '/certs/'
    socket_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    socket_context.load_cert_chain(
        certfile=cert_path + 'domain.crt',
        keyfile=cert_path + 'domain.key'
    )
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    sock.listen(1000)

    client_worker = []

    while True:
        logging.warning("waiting for a connection")
        koneksi, client_address = sock.accept()
        logging.warning(f"Incoming connection from {client_address}")

        client = threading.Thread(target=handle_request, args=(koneksi, client_address))
        client.start()

        logging.warning(f'{client.name} started')
        client_worker.append(client)

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 12000))
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        logging.warning("seelsai")
