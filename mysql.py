import pymysql


def with_connection(f):
    def with_connection_(*args, **kwargs):
        # or use a pool, or a factory function...
        conn = pymysql.connect(
            host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='123345', db='shared_parking')
        try:
            rv = f(conn=conn, *args, **kwargs)
        except Exception as e:
            conn.rollback()
            print(e)
            raise
        else:
            conn.commit()  # or maybe not
        finally:
            conn.close()

        return rv

    return with_connection_
