from functools import reduce

code_str = '0XEFEF0x00060x00010x00060x922E0x007d'
def parse_code(code_str):
    FB = code_str[:6]
    FL = code_str[6:12]
    if FL[-1] == '6':
        UserLocalNumber = code_str[12:18]
        F_ID = code_str[18:24]
        F_COMM = code_str[24:30]
        Data = ''
        CRC = code_str[30:36]
    check_data = code_str.replace(FB,'').replace(CRC,'')
    print(check_data)
    check_t = reduce(lambda x, y: x ^ y, [ord(i) for i in check_data])
    check_code = '0x'+"{:0>4s}".format(hex(check_t).replace('0x',''))
    print(FB,FL,UserLocalNumber,F_ID,F_COMM,Data,CRC)

parse_code(code_str)

