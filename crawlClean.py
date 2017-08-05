import MySQLdb


def download():
    try:
        # jdk version 7 and 8, class_id <= 8264
        cur.execute("update jdk_method set full_declaration = null, return_string = null, description = null, first_version = null, override = null, specified_by = null where class_id <= 1000" )
        conn.commit()


    except Exception, e:
        print Exception, ":", e

conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='jdk_data',
    charset='utf8'
)
cur = conn.cursor()

if __name__ == "__main__":
    download()