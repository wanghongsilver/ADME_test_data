# 主函数，用户使用
import new_dag_deal

def main():
    """主函数，用于子模块的调用"""
    function_list = ['old_dag_deal', 'new_dag_deal', 'raw_data_simulate_deal', 'm433_sensor_simulate_deal']
    print("程序功能模块名称")
    print(*function_list[0:], sep='\n')
    cmd_status = -1
    cmd = input("请根据上述程序功能模块类型输入需要执行模块:\r\n")
    while cmd_status == -1:
        for func_num, func_name in enumerate(function_list):
            print(func_num, func_name)
            if cmd == func_name or cmd == str(func_num):
                cmd_status = func_num
                print("准备执行:", func_name)
                break
            else:
                cmd_status = -1
        if cmd_status == -1:
            cmd = input("输入模块名称错误，请重新输入:\r\n")

    if cmd_status == 0:     # old_dag_deal
        pass
    elif cmd_status == 1:   # new_dag_deal
        filename = input("请输入new_dag_log:")
        new_dag_deal.func_new_dag_deal('../data/txt/'+filename)
    elif cmd_status == 2:   # raw_data_simulate_deal
        pass
    elif cmd_status == 3:   # m433_sensor_simulate_deal
        pass
    else:                   # err
        pass


main()
