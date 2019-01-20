import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import pymysql

from mysql import with_connection

rcParams['figure.figsize'] = 15, 6
MAX_PARKING_SPACES_NUM = 5500


def init_dat_dict():
    dat = dict()
    # data_element = {"is_avail": False, 'start_time': "2000-01-01 01:00:00"}
    for i in range(5501):

        dat[i] = {"is_avail": False, 'start_time': "2000-01-01 01:00:00"}
    return dat


def load_data_from_csv():
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y/%m/%d %H:%M:%S')
    data = pd.read_csv('awk_format2.csv', parse_dates=['date'], index_col='date', date_parser=dateparse)
    # x = data.index
    # y = data.data
    # data = data['data']
    return data


def plot_data(data):
    x = data.index
    y = data.data
    plt.plot(x, y)
    plt.show()


@with_connection
def init_parking_spaces(conn):
    cur = conn.cursor()
    for i in range(5501):
        cur.execute("insert into t_parking(id) values(" + str(i) + ")")


@with_connection
def write_to_db(conn, parking_id, start_time, end_time):
    cur = conn.cursor()
    tmpl = "insert into t_publish(start_time, end_time, parking_id) values('{}','{}','{}')"
    cur.execute(tmpl.format(start_time, end_time, str(parking_id)))
    # print("write to db: start_time={}; end_time={}; parking_id={}".format(start_time, end_time, str(parking_id)))
    cur.close()


def split_parking(data, dat):
    count = 0
    pre_val = 0
    for index in data.index:
        print(count)
        cur_val = data.data[index]
        if cur_val == pre_val:
            continue
        if cur_val > pre_val:
            for i in range(pre_val, cur_val):
                if dat[i]['is_avail']:
                    print("read data wrong: time={}; pre_val={}; cur_val={}; i={}".format(
                        index._repr_base, pre_val, cur_val, i))
                else:
                    dat[i]['start_time'] = index._repr_base
                    dat[i]['is_avail'] = True
        if cur_val < pre_val:
            for i in range(cur_val, pre_val):
                if dat[i]['is_avail'] == False:
                    print("write data wrong: cur_time={}".format(index._repr_base))
                else:
                    write_to_db(parking_id=i, start_time=dat[i]['start_time'], end_time=index._repr_base)
                    dat[i]['is_avail'] = False
        pre_val = cur_val
        count += 1
    # for i in data.data:
    #     if data.data[i] > MAX_PARKING_SPACES_NUM:
    #         data.data[i] = MAX_PARKING_SPACES_NUM
    #         data.data = data.data
    #         data = data
    #     if data.data[i] < 0:
    #         data.data[i] = 0
    #         data.data = data.data
    # data.to_csv('data_format.csv', index=0)
    # data.
    #
    # pre_val = 0
    # for index in data.index:
    #     cur_val = data[index]
    #     if cur_val == pre_val:
    #         continue
    #     if cur_val > pre_val:
    #         for i in range(pre_val, cur_val):
    #             if dat[i]['is_avail']:
    #                 print("{}is wrone".format(index.strptime('%Y-%m-%d %H:%M:%S')))
    #             else:
    #                 dat[i]['is_vail'] = Tru e


if __name__ == '__main__':
    data = load_data_from_csv()
    dat = init_dat_dict()
    # split_parking(data, dat)
    # plot_data(data)
    # connect_to_mysql()
    # init_parking_spaces()
    # test_decorator(ss="123")
    split_parking(data, dat)
    print("1")
