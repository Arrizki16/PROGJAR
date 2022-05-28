import socket
import json
import base64
import logging
import shlex

# Mesin 1 sebagai server
server_address=('0.0.0.0',6666)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    command_str += "\n"
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received="" #empty string
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False

def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False

def remote_post(filename="",data=""):
    if (data == ""):
        try:
            with open(filename,'rb') as fp:
                data = base64.b64encode(fp.read()).decode('utf-8')
        except FileNotFoundError:
            print("error: file not found")
            return False
        except Exception as e:
            print(f"error: {e}")
            return False

    if " " in filename:
        filename = f'"{filename}"'

    command_str=f"POST {filename} {data}"
    hasil = send_command(command_str)
    if not remote_error(hasil):
        print("File berhasil diupload")
        return True
    else:
        print("Gagal")
        return False

def remote_delete(filename=""):
    command_str=f"DELETE {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f"Error message: {hasil['data']}")
        return False
    else:
        print("Gagal")
        return True
    
def remote_error(hasil):
    if (hasil['status']=='OK'):
        return False

    if (hasil['data']):
        print(f"Error message: {hasil['data']}")
        
    return True

if __name__=='__main__':
    server_address=('127.0.0.1',6666)
    remote_list()
    remote_get(filename="pokijan.jpg")
    remote_get(filename="donalbebek.jpg")
    remote_get(filename="rfc2616.pdf")
    remote_delete(filename="pokijan.jpg")
    remote_delete(filename="donalbebek.jpg")
    remote_delete(filename="rfc2616.pdf")
    remote_post(filename="pdm_bangkit.jpeg")


