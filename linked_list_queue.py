class Node:
    def __init__(self, share_id, start_time, end_time):
        self.publish_id = share_id
        self.start_time = start_time
        self.end_time = end_time
        self.next = None


class llQueue:
    def __init__(self):
        self.head = None
        self.last = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, node):
        if self.last is None:
            self.head = node
            self.last = self.head
        else:
            self.last.next = node
            self.last = self.last.next

    def get_first(self):
        return None if self.head == None else self.head

    def get_last(self):
        return None if self.last == None else self.last

    def dequeue(self):
        if self.head is None:
            return None
        else:
            to_return = self.head
            self.head = self.head.next
            return to_return


if __name__ == '__main__':

    a_queue = llQueue()

    while True:
        print('enqueue share_id start_time end_time')
        print('dequeue')
        print('get_first')
        print('get_last')
        print('quit')
        do = input('What would you like to do? ').split()

        operation = do[0].strip().lower()
        if operation == 'enqueue':
            a_queue.enqueue(Node(do[1], do[2], do[3]))
        elif operation == 'dequeue':
            dequeued = a_queue.dequeue()
            if dequeued is None:
                print('llQueue is empty.')
            else:
                print('dequeue element: share_id={}; start_time={}; end_time={}'.format(
                    dequeued.share_id, dequeued.start_time, dequeued.end_time))

        elif operation == 'get_first':
            first_one = a_queue.get_first()
            if first_one is None:
                print('llQueue is empty.')
            else:
                print('first_one: share_id={}; start_time={}; end_time={}'.format(
                    first_one.share_id, first_one.start_time, first_one.end_time))

        elif operation == 'get_last':
            last_one = a_queue.get_last()
            if last_one is None:
                print('llQueue is empty.')
            else:
                print('last_one: share_id={}; start_time={}; end_time={}'.format(
                    last_one.share_id, last_one.start_time, last_one.end_time))
        elif operation == 'quit':
            break

#     a_queue = llQueue()
#
#     a_queue.enqueue(Node(1, 11, 12))
#     a_queue.enqueue(Node(2, 12, 13))
#     a_queue.enqueue(Node(3, 13, 16))
#     dequeued = a_queue.dequeue()
#     first_one = a_queue.get_first()
#     if dequeued is None:
#         print('llQueue is empty.')
#     else:
#         print('dequeue element: share_id={}; start_time={}; end_time={}'.format(
#             first_one.share_id, first_one.start_time, first_one.end_time))
#
# elif operation == 'get_first':
#     first_one = a_queue.get_first()
#     if first_one is None:
#         print('llQueue is empty.')
#     else:
#         print('first_one: share_id={}; start_time={}; end_time={}'.format(
#             first_one.share_id, first_one.start_time, first_one.end_time))
#
# elif operation == 'get_last':
#     last_one = a_queue.get_last()
#     if last_one is None:
#         print('llQueue is empty.')
#     else:
#         print('last_one: share_id={}; start_time={}; end_time={}'.format(
#             first_one.share_id, first_one.start_time, first_one.end_time))
# elif operation == 'quit':
#     break
