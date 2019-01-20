import random
from datetime import timedelta, datetime

import numpy

from mysql import with_connection

order_len_probability_distribution_init = [10, 20, 30, 45, 40, 35, 30, 25, 20]
order_len_probability_distribution = [
    i / sum(order_len_probability_distribution_init) for i in order_len_probability_distribution_init]

order_time_before_pd_init = [5, 5, 10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 50, 50, 50, 50, 50, 50, 60, 60, 60, 60, 50,
                             50, 50, 50, 60, 60, 60, 60, 70, 70, 40, 40, 40, 40, 40, 40, 40, 40, 30, 30, 30, 30, 30, 20,
                             20, 20, 20, 20, 20, 10, 10, 10, 10, 10, 20, 20, 20, 20, 30, 30, 10, 10, 10, 10, 10, 10, 10,
                             10, 10, 10, 20, 20, 20]
order_time_before_pd = [i / sum(order_time_before_pd_init) for i in order_time_before_pd_init]


# 已测试
def rand_gen(start, end):
    """
    随机数生成
    :param start:
    :param end:
    :return:
    """
    rand_gen = random.SystemRandom()
    return rand_gen.randint(start, end)


# 已测试
def random_pick(probability_distribution):
    """
    根据概率密度生成第几个 30 分钟
    :param p:
    :return:
    """
    return numpy.random.choice(numpy.arange(0, len(probability_distribution)), p=probability_distribution)


def split_time(start_time, end_time, probability_distribution):
    """
    根据概率密度生成分割结束时间
    :param start_time:
    :param end_time:
    :return: 结束时间
    """
    # pd_sum = sum(probability_distribution)
    # rand_num = rand_gen(0, pd_sum)
    nth = random_pick(probability_distribution)
    return timedelta(minutes=int(nth) * 30)


@with_connection
def insert_into_order_mysql(conn, start_time, end_time, parking_id):
    delta_time = split_time(start_time=start_time, end_time=end_time, probability_distribution=order_time_before_pd)
    cursor = conn.cursor()
    tmpl = "insert into t_order(parking_id, start_time, end_time, order_time) VALUES ('{}', '{}', '{}', '{}')"
    cursor.execute(
        tmpl.format(
            parking_id, start_time, end_time,
            start_time - delta_time - timedelta(minutes=rand_gen(0, 30), seconds=rand_gen(0, 60))))
    cursor.close()


@with_connection
def test_order_mysql(conn):
    cursor = conn.cursor()
    tmpl = "select * from t_order limit 1000"
    cursor.execute(tmpl)
    for row in cursor:
        print(row)
    cursor.close()



@with_connection
def order_data_gen(conn):
    """
    分割出租时间段，生成订单信息
    :param conn:
    :return:
    """
    cursor = conn.cursor()
    tmpl = "select * from  t_publish"
    cursor.execute(tmpl)
    rowcount = cursor.rowcount
    count = 0
    order_num = 0
    for row in cursor:
        count += 1
        start_time = row[1]
        (_, start_time, end_time, parking_id) = row
        delta_time = timedelta(minutes=30)
        while (start_time < end_time and delta_time != 0):
            delta_time = split_time(
                start_time=start_time, end_time=end_time, probability_distribution=order_len_probability_distribution)
            if delta_time == 0 or end_time < start_time + delta_time:
                order_num += 1
                insert_into_order_mysql(start_time=start_time, end_time=end_time, parking_id=parking_id)
            else:
                order_num += 1
                insert_into_order_mysql(start_time=start_time, end_time=start_time + delta_time, parking_id=parking_id)
            start_time = start_time + delta_time
        print("progress:{}/{}; order_num={}".format(count, rowcount, order_num))
    cursor.close()


if __name__ == '__main__':
    test_order_mysql()
    # print(random_pick(30))
    # print(rand_gen(0, 10))
    # order_data_gen()
    # data = load_data_from_csv()
    # dat = init_dat_dict()
    # split_parking(data, dat)
    # plot_data(data)
    # connect_to_mysql()
    # init_parking_spaces()
    # test_decorator(ss="123")
    # split_parking(data, dat)
    # print("1")
