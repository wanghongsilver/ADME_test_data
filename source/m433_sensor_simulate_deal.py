import serial
import time
import threading
from global_func import CRCGenerator as CRC_G

def str_to_hex(s):
    return ''.join([hex(ord(c)).replace('0x', '') for c in s])

def func_m433_sensor_open(usr_com, usr_baud):
    """传感器打开设置"""
    ser = serial.Serial(port=usr_com, baudrate=usr_baud, bytesize=8, parity='N', stopbits=1, timeout=5)  # 设置串口
    if ser.isOpen() == False:
        ser.open()
    print(ser)  # 打印串口状态
    return ser

def func_m433_sensor_rec(ser):
    """传感器接收函数"""
    Crc = CRC_G()
    while True:
        #接收数据
        ser_data = ser.readline()
        # ser_data = "##START*8C\r\n"
        print(ser_data)
        # 进行数据判断，crc
        if len(ser_data) < 1:
            continue
        crcbuf = Crc.create(str_to_hex(ser_data[:-5]))
        crcstr = str(crcbuf).upper()
        crcresult = str(crcstr[2:])

        print(crcresult)
        if crcresult in ser_data:
            if "##CFG" in ser_data:
                write_str = "$$CFG:OK\r\n"
                ser.write(write_str.encode())
            elif "##START" in ser_data:
                write_str = "$$START:OK\r\n"
                ser.write(write_str.encode())
            elif "##TURNOFF" in ser_data:
                write_str = "$$STURNOFF:OK\r\n"
                ser.write(write_str.encode())
            elif "##READ:" in ser_data:
                write_str = "READ"
                ser.write(write_str.encode())
            else:
                print(ser_data)
        time.sleep(0.1)




def func_m433_sensor_send():
    pass

def func_m433_sensor_simulate_deal(input_file_name, usr_com, usr_baud):
    """
    433传感器模拟处理函数
    input_file_name：新版DAG日志文件 从mcloud下载，格式为txt
    """
    usr_ser = func_m433_sensor_open(usr_com, usr_baud)
    func_m433_sensor_rec(usr_ser)
    # Crc = CRC_G()
    # data_str = 'MDM,1912A4T,ADS,2006251907,S,0620,$$READ:9,ADS,1701,4500+8.5190+0.0000+23.8,3.6'
    # crcdata = Crc.create(str_to_hex(data_str))
    # crcstr = str(crcdata).upper()
    # print(crcstr[2:])
    # Crc.create('2424524541443a382c4144532c313635312c343030302b372e383930312b302e303030302b32332e382c332e36')

func_m433_sensor_simulate_deal('../data/txt/1912A4T_RawData_2020-06-27-16-39-58.txt','COM5', 115200)



