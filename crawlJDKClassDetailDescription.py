import MySQLdb
import requests
from scrapy import Selector


def download():
    try:
        cur.execute("select class_id, doc_website from jdk_class where package_id <= 426")
        lists = cur.fetchall()
        for each_list in lists:
            print each_list[0]
            while 1 == 1:
                try:
                    sel = Selector(requests.get(each_list[1], timeout=10))
                except Exception, e:
                    print 'timeout'
                    continue
                break
            # print sel.xpath('//div[@class="description"]/ul/li/div[@class="block"]')
            if sel.xpath('//div[@class="description"]/ul/li/div[@class="block"]'):
                description = sel.xpath('//div[@class="description"]/ul/li/div[@class="block"]').extract()[0]
                print description
                cur.execute("update jdk_class set detail_description = %s where class_id = %s",
                            (description, each_list[0]))
                conn.commit()

    except Exception, e:
        print Exception, ":", e

conn = MySQLdb.connect(
    host='10.131.252.156',
    port=3306,
    user='root',
    passwd='root',
    db='fdroid',
    charset='utf8'
)
cur = conn.cursor()

if __name__ == "__main__":
    download()
