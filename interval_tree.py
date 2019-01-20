from datetime import datetime

BLACK = "BLACK"
RED = "RED"


class RBnode(object):
    def __init__(self, ID=None, parking_id=None, start_time=datetime(2000, 1, 1, 0, 0, 0),
                 end_time=datetime(2000, 1, 1, 0, 0, 0), color=BLACK):
        super(RBnode, self).__init__()
        self.id = ID
        self.parking_id = parking_id
        self.start_time = start_time
        self.end_time = end_time
        self.max = end_time
        self.left = None
        self.right = None
        self.parent = None
        self.color = color


class RBtree(object):
    def __init__(self):
        self.nil = RBnode()
        self.root = self.nil

    def left_rotate(self, x):
        y = x.right
        if y is not self.nil:  # 右节点不为空
            x.right = y.left
            if y.left is not self.nil:
                y.left.parent = x
            y.parent = x.parent
            if x.parent is self.nil:  # x原来是根
                self.root = y
            elif x is x.parent.left:  # x是左孩子
                x.parent.left = y
            else:
                x.parent.right = y
            y.left = x
            x.parent = y
            # update max
            y.max = x.max
            x.max = max(x.end_time, x.left.max, x.right.max)

    def right_rotate(self, y):
        '''右旋'''
        x = y.left
        if x is not self.nil:  # y的左节点不为空
            y.left = x.right
            if x.right is not self.nil:
                x.right.parent = y
            x.parent = y.parent
            if y.parent is self.nil:  # y原来是根节点
                self.root = x
            elif y is y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
            y.parent = x
            x.right = y
            # update max
            x.max = y.max
            y.max = max(y.end_time, y.left.max, y.right.max)

    def rb_insert(self, z):
        '''插入z节点'''
        if z is self.nil:
            return
        y = self.nil
        x = self.root
        while x is not self.nil:
            x.max = max(x.max, z.max)  # 插入z时更新max值
            y = x
            x = (x.left if x.start_time > z.start_time else x.right)
        z.parent = y
        if y is self.nil:
            self.root = z
        elif y.start_time > z.start_time:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = RED
        self.rb_insert_fixup(z)

    def rb_insert_fixup(self, z):
        '''保持插入后红黑树性质'''
        while z.parent.color is RED:  # z的父节点是红色
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color is RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color is RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)
        self.root.color = BLACK

    def rb_transplant(self, u, v):
        '''删除u节点 以v节点代替'''
        if u.parent is self.nil:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def rb_delete_fixup(self, x):
        '''保持删除节点后红黑树性质'''
        while (x is not self.root) and (x.color is BLACK):
            if x is x.parent.left:
                w = x.parent.right
                if w.color is RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color is BLACK and w.right.color is BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color is BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color is RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color is BLACK and w.left.color is BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color is BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def rb_delete(self, z):  # 这里跟书上有删改
        '''删除节点z'''
        if z is self.nil:
            exit("ATTENTION !!! Don't delete Tree.nil !!!")
        y_origimal_color = z.color
        if z.left is self.nil:
            x = z.right
            self.rb_transplant(z, z.right)
            p = x.parent
            while p.max == z.max:
                p.max = max(p.left.max, p.right.max, p.end_time)
                p = p.parent
        elif z.right is self.nil:
            x = z.left
            self.rb_transplant(z, z.left)
            p = x.parent
            while p.max == z.max:
                p.max = max(p.left.max, p.right.max, p.end_time)
                p = p.parent
        else:
            y = self.minimum(z.right)
            y_origimal_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            if y.parent is not z:
                self.rb_transplant(y, x)
                y.right = z.right
                y.right.parent = y

                y.parent = self.nil
                p = x.parent
                while p.max == y.max:
                    p.max = max(p.left.max, p.right.max, p.end_time)
                    p = p.parent
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

            y.max = max(y.left.max, y.right.max, y.end_time)
            p = y.parent
            while p.max == z.max:
                p.max = max(p.left.max, p.right.max, p.end_time)
                p = p.parent

        if y_origimal_color is BLACK:
            self.rb_delete_fixup(x)

    def minimum(self, x=False):
        '''
        找到以 x 节点为根节点的树的最小值节点 并返回
        return: 最小值节点
        '''
        while x.left is not self.nil:
            x = x.left
        return x

    def maximum(self, x=False):
        '''
        找到以 x 节点为根节点的树的最大值节点 并返回
        return: 最大值节点
        '''
        if x is False:
            x = self.root
        while x.right is not self.nil:
            x = x.right
        return x

    def inorder_traversal(self, x):
        '''中序遍历输出'''
        if x is not self.nil:
            self.inorder_traversal(x=x.left)
            print("id:{} parking_id:{:<14} start_time:{} end_time:{} max:{} color:{:<5}".format(
                x.id, x.parking_id, x.start_time, x.end_time, x.max, x.color))
            self.inorder_traversal(x=x.right)

    def preorder_traversal(self, x):
        '''先序遍历输出'''
        if x is not self.nil:
            print("id:{} parking_id:{:<14} start_time:{} end_time:{} max:{} color:{:<5}".format(
                x.id, x.parking_id, x.start_time, x.end_time, x.max, x.color))
            self.inorder_traversal(x=x.left)
            self.inorder_traversal(x=x.right)

    def is_overlap(self, x, start_time, end_time):
        '''if x 交叉 [start_time,end_time] return True else False'''

        s = max(start_time, x.start_time)
        e = min(end_time, x.end_time)
        return e > s and ((e - s) / (max(end_time, x.end_time) - min(start_time, x.start_time))) > 0.6  # 覆盖率低于0.6的直接舍去

    def interval_search(self, start_time, end_time):
        '''查询[start_time,end_time]区间内一个的课程'''
        x = self.root
        while (x is not self.nil) and (not self.is_overlap(x, start_time, end_time)):
            if (x.left is not self.nil) and (x.left.max >= start_time):
                x = x.left
            else:
                x = x.right
        return x

    def minstart_time(self, x):
        if x is self.nil:
            return x.start_time
        while x is not self.nil:
            y = x
            x = x.left
        return y.start_time

    def search(self, x, start_time, end_time, all=[]):
        '''search all 利用区间树性质'''
        if self.is_overlap(x, start_time, end_time):
            all.append(x)
        if x is not self.nil and start_time <= x.left.max and end_time >= self.minstart_time(x):
            # 深度不深时可以放弃end_time>self.minstart_time(x)的比较
            self.search(x.left, start_time, end_time, all)
        if x is not self.nil and end_time >= x.start_time and start_time <= x.right.max:
            self.search(x.right, start_time, end_time, all)

    def search_all(self, x, start_time, end_time, delete=[]):
        '''查询与[start_time,end_time]有交集的所有课程 利用中序遍历'''
        if x is not self.nil:
            self.search_all(x.left, start_time, end_time, delete)
            if self.is_overlap(x, start_time, end_time):
                print("id:{} parking_id:{:<14} start_time:{} end_time:{} color:{:<5}".format(
                    x.id, x.parking_id, x.start_time, x.end_time, x.color))
                delete.append(x)
            self.search_all(x.right, start_time, end_time, delete)

    def search_less_than(self, x, time_less_than, lt_list=[]):
        if x is self.nil:
            return
        if self.minstart_time(x) > time_less_than:
            return
        if x.start_time >= time_less_than:
            self.search_less_than(x.left, time_less_than, lt_list)
        else:
            if x.end_time <= time_less_than:
                lt_list.append(x)
            self.search_less_than(x.left, time_less_than, lt_list)
            self.search_less_than(x.right, time_less_than, lt_list)


def search_id(self, x, id, delete):
    '''利用中序遍历删除固定的id课程'''
    if x is not self.nil:
        self.search_id(x.left, id, delete)
        if x.id == id:
            delete.append(x)
        self.search_id(x.right, id, delete)


def command(Tree):
    '''
     insert id name start_time end_time
     delete id
     del start_time end_time
     search all start_time end_time
     search one start_time end_time
     exit
     '''

    while True:
        print(
            "\n\nyou can do :\n insert id parking_id start_time end_time \n delete id \n del start_time end_time\n search all start_time end_time\n search lt lt_time\n search one start_time end_time\n exit")
        command = list(input().split())
        if command[0] == "insert":
            x = RBnode(command[1], command[2],
                       command[3], command[4])
            Tree.rb_insert(x)
            print("after insert :")
            Tree.inorder_traversal(Tree.root)
            print("\n")
        elif command[0] == "delete":
            delete = []
            Tree.search_id(Tree.root, command[1], delete)
            if len(delete) < 1:
                print("delete error\n")
            else:
                Tree.rb_delete(delete[0])
                print("after delete :")
                Tree.inorder_traversal(Tree.root)
                print("\n")

        elif command[0] == "del":
            delete = []
            Tree.search(Tree.root,
                        command[1], command[2], delete)
            if len(delete) < 1:
                print("delete error\n")
            else:
                while len(delete) != 0:
                    Tree.rb_delete(delete[-1])
                    delete.pop(-1)
                print("after del:")
                Tree.inorder_traversal(Tree.root)
        elif command[0] == "search":
            if command[1] == "all":
                all = []
                Tree.search(Tree.root, command[2], command[3], all)
                if len(all) == 0:
                    print("There is no class at this time")
                else:
                    while len(all) != 0:
                        x = all.pop(-1)
                        print("id:{} parking_id:{:<14} start_time:{} end_time:{} color:{:<5}".format(
                            x.id, x.parking_id, x.start_time, x.end_time, x.color))
            if command[1] == "lt":
                lt_list = []
                Tree.search_less_than(Tree.root, command[2], lt_list)
                if len(lt_list) == 0:
                    print("There is no class at this time")
                else:
                    while len(lt_list) != 0:
                        x = lt_list.pop(-1)
                        print("id:{} parking_id:{:<14} start_time:{} end_time:{} color:{:<5}".format(
                            x.id, x.parking_id, x.start_time, x.end_time, x.color))
            if command[1] == "one":
                x = Tree.interval_search(start_time=
                                         command[2], end_time=command[3])
                if x is not Tree.nil:
                    print("id:{} parking_id:{:<14} start_time:{} end_time:{} color:{:<5}".format(
                        x.id, x.parking_id, x.start_time, x.end_time, x.color))
                else:
                    print("There is no class at this time")

        elif command[0] == "exit":
            exit("Good bye!\n")
        else:
            print("Re-enter,please")


def main():
    course = {
        "1": ("one", datetime(2000, 1, 1, 0, 16, 0), datetime(2000, 1, 1, 0, 21, 0)),
        "2": ("two", datetime(2000, 1, 1, 0, 8, 0), datetime(2000, 1, 1, 0, 9, 0)),
        "3": ("three", datetime(2000, 1, 1, 0, 25, 0), datetime(2000, 1, 1, 0, 30, 0)),
        "4": ("four", datetime(2000, 1, 1, 0, 5, 0), datetime(2000, 1, 1, 0, 8, 0)),
        "5": ("five", datetime(2000, 1, 1, 0, 15, 0), datetime(2000, 1, 1, 0, 23, 0)),
        "6": ("six", datetime(2000, 1, 1, 0, 17, 0), datetime(2000, 1, 1, 0, 19, 0)),
        "7": ("seven", datetime(2000, 1, 1, 0, 26, 0), datetime(2000, 1, 1, 0, 27, 0)),
        "8": ("eight", datetime(2000, 1, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 3, 0)),
        "9": ("nine", datetime(2000, 1, 1, 0, 6, 0), datetime(2000, 1, 1, 0, 10, 0)),
        "10": ("ten", datetime(2000, 1, 1, 0, 19, 0), datetime(2000, 1, 1, 0, 20, 0))}

    Tree = RBtree()  # Tree.left.start_time < Tree.start_time <= Tree.right.start_time
    for i in course.keys():
        node = RBnode(i, *course[i])
        Tree.rb_insert(node)
    print("\n\n初始树为：")
    Tree.preorder_traversal(Tree.root)
    #
    # x = RBnode(11, "eleven", datetime(2000, 1, 1, 0, 8, 0), datetime(2000, 1, 1, 0, 20, 0))
    # Tree.rb_insert(x)
    # print("after insert :")
    all = []
    Tree.search_less_than(Tree.root, datetime(2000, 1, 1, 0, 8, 0), all)
    print("\n\n删除前：")

    if len(all) == 0:
        print("There is no class at this time")
    else:
        delete = []
        delete += all
        while len(all) != 0:
            x = all.pop(-1)
            print("id:{} parking_id:{:<14} start_time:{} end_time:{} color:{:<5}".format(
                x.id, x.parking_id, x.start_time, x.end_time, x.color))
    if len(delete) < 1:
        print("delete error\n")
    else:
        while len(delete) != 0:
            Tree.rb_delete(delete[-1])
            delete.pop(-1)
        print("after del:")
        Tree.inorder_traversal(Tree.root)
    # command(Tree)


if __name__ == '__main__':
    main()
