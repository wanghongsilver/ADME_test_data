import global_func
import re
import time
import csv

def func_new_dag_deal(input_file_name):
    """
    新版DAG数据处理函数
    input_file_name：新版DAG日志文件 从mcloud下载，格式为txt
    输出文件格式： SN号+处理时间+文件后缀
    """
    print(input_file_name)
    # 判断文件格式是否为txt
    if global_func.decide_file_type(input_file_name, 'txt') == False:
        print("请输入txt文件...")
        exit(-1)

    # 获得处理文件SN号
    with open(input_file_name) as f:
        sn_line = f.readline()
        sn_list = re.findall(r"\S{6}T", sn_line)  # 正则表达式6C+T
        sn_str = sn_list[0]
        print("SN:{}".format(sn_str))

    # 将日志文件分拆
    sys_time_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    with open(input_file_name) as f:  # 读取文件多行
        file_lines = f.readlines()
    for file_line in file_lines:  #将文件分拆
        if re.findall(r"Motor Stop;", file_line):  # 运动停机相关数据
            with open('../data/txt/'+sn_str+'_MotorStop_'+sys_time_str+'.txt',
                      'a', encoding='utf-8') as f_motor:
                f_motor.write(str(file_line))
        elif re.findall(r"READ:", file_line):  # 原始测量数据
            with open('../data/txt/'+sn_str+'_RawData_'+sys_time_str+'.txt',
                      'a', encoding='utf-8') as f_read:
                f_read.write(str(file_line))
        elif re.findall(r",D,", file_line):   # 平台上传数据
            with open('../data/txt/' + sn_str + '_PlatformData_' + sys_time_str + '.txt',
                      'a', encoding='utf-8') as f_platform:
                f_platform.write(str(file_line))

    # # 数据处理，获得设备运动停机相关数据，并处理 csv,excel,svg,Motor
    # with open('../data/txt/' + sn_str + '_MotorStop_' + sys_time_str + '.txt') as f_motor:
    #     f_motor_lines = f_motor.readlines()
    #
    # # 新建csv文件 写入文件中
    # csv_list = ['date', 'workcnt', 'distance_set', 'distance_bmqac', 'distance_jmqac']
    # with open('../data/csv/' + sn_str + '_MotorStop_' + sys_time_str + '.csv', 'a') as f_motor_csv:
    #     writer = csv.writer(f_motor_csv)
    #     writer.writerow(csv_list)
    #
    # for f_motor_line in f_motor_lines:
    #     re_listbuf = re.findall(r"\d{10}", f_motor_line)
    #     f_motor_date = re_listbuf[0]
    #     re_listbuf = re.findall(r"=\d+", f_motor_line)
    #     f_motor_workcnt_str = re_listbuf[0]
    #     f_motor_workcnt = f_motor_workcnt_str[1:]
    #     re_listbuf = re.findall(r"\d+\s", f_motor_line)
    #     if len(re_listbuf) == 3:
    #         f_motor_distance_set = re_listbuf[0]
    #         f_motor_distance_bmqac = re_listbuf[1]
    #         f_motor_distance_jmqac = re_listbuf[2]
    #     print(f_motor_date, f_motor_workcnt, f_motor_distance_set, f_motor_distance_bmqac, f_motor_distance_jmqac)
    #     #写入csv文件
    #     csv_list[0] = f_motor_date
    #     csv_list[1] = f_motor_workcnt
    #     csv_list[2] = f_motor_distance_set
    #     csv_list[3] = f_motor_distance_bmqac
    #     csv_list[4] = f_motor_distance_jmqac
    #
    #     with open('../data/csv/' + sn_str + '_MotorStop_' + sys_time_str + '.csv', 'a') as f_motor_csv:
    #         writer = csv.writer(f_motor_csv)
    #         writer.writerow(csv_list)

    # 数据处理，获得原始测量数据，并处理 csv,excel,svg,$$READ
    # 数据处理，获得上传平台数据，并处理 csv,excel,svg,MDM，D
    # 数据处理，上传平台数据并做差，并处理 csv,excel,svg,MDM，D

func_new_dag_deal('../data/txt/MCLOUD-2020-06-26_112307.txt')