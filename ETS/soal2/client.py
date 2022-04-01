import sys
import socket
import json
import logging
import ssl
import os
from time import process_time
import concurrent.futures
import random

server_address = ('localhost', 12000)

def make_socket(destination_address='localhost',port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserialisasi(s):
    logging.warning(f"deserialisasi {s.strip()}")
    return json.loads(s)
    

def send_command(command_str,is_secure=False):
    alamat_server = server_address[0]
    port_server = server_address[1]
    
    sock = make_socket(alamat_server,port_server)

    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received=""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = deserialisasi(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False


def getdatapemain(nomor=0,is_secure=False):
    start_time = process_time()
    cmd=f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    if (hasil):
        print(hasil['nama'], hasil['posisi'])
        return process_time() - start_time
    else: 
        return False


def lihatversi(is_secure=False):
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil

def get_output(client_worker, request_count, response_count, latency, execution_time):
    print(f'With {client_worker} workers')
    print(f'Request count: {request_count}')
    print(f'Response count: {response_count}')
    print(f'Average Latency: {(latency / response_count) * 1000:.3f} ms')
    print(f'Execution time: {(execution_time) * 1000:.3f} ms')


def multi_thread(latency=0, client_worker=0):
    request_count = 2000
    response_count = 0
    
    job = {}
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=client_worker)
    
    start_time = process_time()
    
    for i in range(request_count):
        nomor_pemain = random.randint(1,30)
        job[i] = executor.submit(getdatapemain, nomor_pemain)
        
    for i in range(request_count):
        hasil = job[i].result()
        if (hasil):
            response_count += 1
            latency += hasil
    
    finish_time = process_time()
    execution_time = finish_time - start_time
    get_output(client_worker, request_count, response_count, latency, execution_time)

if __name__=='__main__':
    h = lihatversi()
    if (h):
        print(h)
        
    client_worker = int(input("Masukkan jumlah worker pada client: "))
    multi_thread(0, client_worker)
