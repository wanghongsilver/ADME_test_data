import serial
import re
import time

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

def func_m433_sensor_rec(ser, raw_data_filename):
    """传感器接收函数"""
    Crc = CRC_G()
    last_read_cnt = -1
    while True:
        #接收数据
        ser_data = ser.readline()
        # ser_data = "##READ:10*04\r\n"
        # 进行数据判断，crc
        if len(ser_data) < 1:
            continue
        print(ser_data)
        crcbuf = Crc.create(str_to_hex(ser_data[:-5]))
        crcstr = str(crcbuf).upper()
        crcresult = str(crcstr[2:])

        print(crcresult)
        if crcresult in ser_data:
            if "##CFG" in ser_data:
                write_str = "$$CFG:OK\r\n"
                print(write_str)
                ser.write(write_str.encode())
            elif "##START" in ser_data:
                write_str = "$$START:OK\r\n"
                print(write_str)
                ser.write(write_str.encode())
            elif "##TURNOFF" in ser_data:
                write_str = "$$TURNOFF:OK\r\n"
                print(write_str)
                ser.write(write_str.encode())
            elif "##READ:" in ser_data:
                read_list = re.findall(r"\d+", ser_data)
                print(read_list)
                read_cnt = int(read_list[0])
                print(read_cnt)
                with open(raw_data_filename) as f_raw_data:
                    f_raw_data_lines = f_raw_data.readlines()
                for f_raw_data_line in f_raw_data_lines:#更新原始数据文件，如果是不相同的点数 就删除当前行
                    with open(raw_data_filename, 'w') as f_raw_data:
                        if read_cnt != last_read_cnt:  # 如果2次读取点数不同，则删除当前行
                            continue
                        f_raw_data.write(f_raw_data_line)
                for f_raw_data_line in f_raw_data_lines:#在文件中查找相同的点数，数据上传
                    raw_data_readcntlist = re.findall(r":\d+,", f_raw_data_line)
                    raw_data_readcntstr = str(raw_data_readcntlist[0])
                    raw_data_readcnt = int(raw_data_readcntstr[1:-1])
                    print(raw_data_readcnt)

                    if raw_data_readcnt == read_cnt:
                        write_strbuf = f_raw_data_line[34:-1]
                        cwrite_str_crcbuf = Crc.create(str_to_hex(write_strbuf))
                        cwrite_str_crcbuf = str(cwrite_str_crcbuf).upper()
                        write_str_crcresult = str(cwrite_str_crcbuf[2:])
                        write_str = write_strbuf + '*' + write_str_crcresult + '\r\n'
                        print(write_str)
                        ser.write(write_str.encode())
                        last_read_cnt = read_cnt# 删除原始数据
                        break
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
    func_m433_sensor_rec(usr_ser, input_file_name)
    # Crc = CRC_G()
    # data_str = 'MDM,1912A4T,ADS,2006251907,S,0620,$$READ:9,ADS,1701,4500+8.5190+0.0000+23.8,3.6'
    # crcdata = Crc.create(str_to_hex(data_str))
    # crcstr = str(crcdata).upper()
    # print(crcstr[2:])
    # Crc.create('2424524541443a382c4144532c313635312c343030302b372e383930312b302e303030302b32332e382c332e36')

func_m433_sensor_simulate_deal('../data/txt/1912A4T_RawData.txt','COM5', 115200)



