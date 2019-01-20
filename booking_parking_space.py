from collections import deque
from datetime import timedelta, datetime

from interval_tree import RBtree, RBnode
from linked_list_queue import llQueue, Node
from mysql import with_connection

time_buffer = timedelta(days=7)
llqueue = llQueue()
LAST_TIME = None
PERCENT_OF_COVER = 0.6


def match_operator(a_start_time, a_end_time, b_start_time, b_end_time):
    pass


@with_connection
def re_build_tree(conn, cursor, start_parking_time):
    Tree = RBtree()  # Tree.left.start_time < Tree.start_time <= Tree.right.start_time
    cur = conn.cursor()
    del_list = []
    Tree.search_less_than(Tree.root, start_parking_time, del_list)
    for d in del_list:
        Tree.rb_delete(d)

    for row in cursor:
        tmpl = "select parking_id from t_publish where id = '{}'"
        cur.execute(tmpl.format(row[1]))
        parking_id = cur._rows[0][0]
        node = RBnode(row[0], parking_id, row[2], row[3])
        Tree.rb_insert(node)
    return Tree
    # Tree.inorder_traversal(Tree.root)


@with_connection
def data_prepare(conn, order_time):
    """
    TODO:自定义结尾，insert 重复数据时不插入
    :param conn:
    :param order_time:
    :return:
    """
    start_time = order_time + timedelta(minutes=30)
    last_one = llqueue.get_last()
    if last_one:
        start_time = last_one.start_time
    end_time = order_time + time_buffer
    cursor = conn.cursor()
    tmpl = "SELECT * FROM t_share WHERE '{}' > start_time and '{}' <= end_time"
    cursor.execute(tmpl.format(end_time, start_time))
    return re_build_tree(cursor=cursor, start_parking_time=order_time + timedelta(minutes=30))


@with_connection
def book(conn, Tree):
    cur = conn.cursor()
    start_time = datetime(2016, 5, 30, 20, 0, 0)
    tmpl = "SELECT * FROM t_order WHERE order_time > '{}' and order_time < '{}' order by order_time"
    cur.execute(tmpl.format(start_time, start_time + timedelta(hours=1)));
    now = datetime.now()
    cursor = conn.cursor()
    count = 0
    tmpl_1 = "select * from t_share WHERE start_time < '{}' and end_time > '{}' "
    while (cur.rowcount != 0):
        row = cur.fetchone()
        data_prepare(order_time=row[4])
        while row is not None:
            res = []
            Tree.search_all(Tree.root, row[2], row[3], res)
            count += 1
            print("count:{}; use_time:{}".format(count, datetime.now() -now))

            row = cur.fetchone()


            # cursor.execute(tmpl_1.format(row[2], row[3]))

        start_time += timedelta(hours=1)
        cur.execute(tmpl.format(start_time, start_time + timedelta(hours=1)));

    cur.close()


if __name__ == '__main__':
    # book()
    Tree = data_prepare(order_time=datetime(2016, 12, 1, 0, 8, 0))
    book(Tree=Tree)
    # Tree.inorder_traversal(Tree.root)
