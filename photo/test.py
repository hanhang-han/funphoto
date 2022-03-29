import socket
import threading
import time
from functools import reduce

import crcmod



serial_flag = '0x0001'
trans = {
    "Began_to_detect":"0x912C",
    "End_detect":"0x912D",
    "Query_state":"0x922E",
    "hello":"0x9212",
}

def gen_data(f_data):
    global serial_flag
    if serial_flag != 0xFFFF:
        serial_flag = hex(int(serial_flag,16) + 1).replace('0x', '')
        Z_ID = "0x" + "{:0>4s}".format(serial_flag)
    else:
        Z_ID = '0x0001'
    OID = trans[f_data]
    data = "0x0006" + "0x0001" + Z_ID +OID
    data = add_check_code(data)
    return "0XEFEF" +data

handle_list = []

tcp_server_ip = '127.0.0.1'
tcp_server_port = 8889
ADDR = (tcp_server_ip,tcp_server_port)
tcpClientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpClientSock.connect(ADDR)
time_flag = 0
def send_data(data):
    data_send = gen_data(data)
    print(data_send)
    tcpClientSock.send(data_send.encode('utf8'))
    print('sended')

def add_check_code(data):
    check_code = reduce(lambda x, y: x ^ y, [ord(i) for i in data])
    return data+'0x'+ "{:0>4s}".format(hex(check_code).replace('0x',''))

def send_hello():
    global time_flag
    time_now = time.time()
    if time_now - time_flag >= 20:
        hello_pak = gen_data('hello')
        tcpClientSock.send(hello_pak.encode('utf8'))
        time_flag = time_now

def run_tcp_client():
    global connect_flag
    global handle_list
    while True:
        send_hello()
        if handle_list:
            send_data(handle_list.pop())
        connect_flag = True
    tcpClientSock.close()
    connect_flag = False
def func():
    global handle_list
    while True:
        handle_list.append(input())
        print(handle_list)
if __name__ == '__main__':
    t1 = threading.Thread(target=run_tcp_client)
    t2 = threading.Thread(target=func)
    t1.start()
    t2.start()
    t1.join()
    t2.join()