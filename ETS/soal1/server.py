import sys
import socket
import logging
import json
import os
import ssl
import time

alldata = dict()
alldata['1']=dict(nomor=1, nama="Edouard Mendy", posisi="goalkeeper")
alldata['2']=dict(nomor=2, nama="Reece James", posisi="right fullback")
alldata['3']=dict(nomor=3, nama="Ben Chilwell", posisi="left fullback")
alldata['4']=dict(nomor=4, nama="Antonio Rudiger", posisi="center back")
alldata['5']=dict(nomor=5, nama="N Golo Kante", posisi="defending midfielder")
alldata['6']=dict(nomor=6, nama="Christian Pulisic", posisi="right midfielder")
alldata['7']=dict(nomor=7, nama="Kennedy", posisi="left midfielder")
alldata['8']=dict(nomor=8, nama="Mateo Kovacic", posisi="central midfielder")
alldata['9']=dict(nomor=9, nama="Mason Mount", posisi="attacking midfielder")
alldata['10']=dict(nomor=10, nama="Kepa Arrizabalaga", posisi="goalkeeper")
alldata['11']=dict(nomor=11, nama="Cesar Azpilicueta", posisi="right fullback")
alldata['12']=dict(nomor=12, nama="Marcos Alonso", posisi="left fullback")
alldata['13']=dict(nomor=13, nama="Andreas Christensen", posisi="center back")
alldata['14']=dict(nomor=14, nama="Jorginho", posisi="defending midfielder")
alldata['15']=dict(nomor=15, nama="Callum Hudson-Odoi", posisi="right midfielder")
alldata['16']=dict(nomor=16, nama="Ruben Loftus-Cheek", posisi="central midfielder")
alldata['17']=dict(nomor=17, nama="Hakim Ziyech", posisi="attacking midfielder")
alldata['18']=dict(nomor=18, nama="Marcus Bettinelli", posisi="goalkeeper")
alldata['19']=dict(nomor=19, nama="Trevoh Chalobah", posisi="center back")
alldata['20']=dict(nomor=20, nama="Malang Sarr", posisi="center back")
alldata['21']=dict(nomor=21, nama="Thiago Silva", posisi="center back")
alldata['22']=dict(nomor=22, nama="Ross Barkley", posisi="central midfielder")
alldata['23']=dict(nomor=23, nama="Saul Niguez", posisi="central midfielder")
alldata['24']=dict(nomor=24, nama="Kai Havertz", posisi="attacking midfielder")
alldata['25']=dict(nomor=25, nama="Charly Musonda", posisi="attacking midfielder")
alldata['26']=dict(nomor=26, nama="Petr Cech", posisi="goalkeeper")
alldata['27']=dict(nomor=27, nama="Thibaut Courtois", posisi="goalkeeper")
alldata['28']=dict(nomor=28, nama="Gary Cahill", posisi="central midfielder")
alldata['29']=dict(nomor=29, nama="Eden Hazard", posisi="forwarder attacker")
alldata['30']=dict(nomor=30, nama="Didier Drogba", posisi="attacking midfielder")


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
                hasil = alldata[nomorpemain]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    return hasil


def serialisasi(a):
    serialized =  json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized

def run_server(server_address,is_secure=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    sock.listen(1000)


    while True:
        logging.warning("waiting for a connection")
        koneksi, client_address = sock.accept()
        logging.warning(f"Incoming connection from {client_address}")

        try:
            connection = koneksi

            selesai=False
            data_received=""
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
        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 12000),is_secure=True)
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        logging.warning("seelsai")
