import socket
import time

import crcmod



serial_flag = 0x0001
trans = {
    "Began_to_detect":"0x912C",
    "End_detect":"0x912D",
    "Query_state":"0x922E"
}

def gen_data(f_data):
    global serial_flag
    if serial_flag != 0xFFFF:
        serial_flag = int(hex(serial_flag + 1),16)
        print(hex(serial_flag))
    else:
        serial_flag = hex(0x0001)
    OID = trans[f_data]
    data = "0XEFEF" + "0x0006" + "0x0001" + hex(serial_flag) +OID
    crc32_func = crcmod.mkCrcFun(0X18005, initCrc=0, xorOut=0xFFFFFF)
    CRC_check = crc32_func(data.encode())
    data += str(CRC_check)
    return data



tcp_server_ip = '127.0.0.1'
tcp_server_port = 8888
ADDR = (tcp_server_ip,tcp_server_port)
tcpClientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpClientSock.connect(ADDR)

for i in range(30):
    tcpClientSock.send(gen_data("Query_state").encode('utf8'))
    time.sleep(0.5)