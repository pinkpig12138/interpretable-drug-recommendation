# #
# # import time
# # def my_function(num):
# #     time.sleep(num)
# #
# # time_list = [5]* 20
# #
# # t1 = time.time()
# #
# # for num in time_list:
# #     my_function(num)
# #
# # print(time.time()-t1)
#
# #
# # #!/usr/bin/python3
# # # -*- coding:utf-8 -*-
# # """
# # @author: zhangyuhao
# # @file: test.py
# # @time: 2022/1/10 下午8:08
# # @email: yuhaozhang76@gmail.com
# # @desc:
# # """
# import time
# import threading
# import inspect
# import csv
# csv_writer = csv.writer(open("/code/pinkpig/KDD_TX/KDD/构建图谱/data/test.csv", 'w', newline=''))
#
# def my_function(num):
#     time.sleep(num)
#
# time_list = [3]* 1000
# t1 = time.time()
#
# for i, num in enumerate(time_list):
#     globals()['thread' + str(i)] = threading.Thread(target=my_function, args=(num,))
#
#
# if __name__ == '__main__':
#     for i in range(len(time_list)):
#         globals()['thread'+str(i)].start()
#     for i in range(len(time_list)):
#         globals()['thread' + str(i)].join()
#     print(time.time() - t1)
#
#

