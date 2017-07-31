import MySQLdb
import requests
from scrapy import Selector


def download():
    try:
        # cur.execute("select class_id, doc_website from jdk_class where class_id > 0 and class_id < 100")
        cur.execute("select class_id, doc_website from jdk_class where class_id = 99")
        lists = cur.fetchall()
        for list in lists:
            print list[0]
            while 1 == 1:
                try:
                    sel = Selector(requests.get(list[1], timeout=10))
                except Exception, e:
                    print 'timeout'
                    continue
                break

            version = ''
            print sel.xpath('//div[@class="description"]/ul/li/dl/dd/text()').extract()
            if sel.xpath('//div[@class="description"]/ul/li/dl/dd/text()').extract():
                print sel.xpath('//div[@class="description"]/ul/li/dl/dd/text()').extract()[0]
                version = sel.xpath('//div[@class="description"]/ul/li/dl/dd/text()').extract()[0]
                if version.find('j') != -1 or version.find('J') != -1:
                    version = version[3:]
                version = version.replace("\n", "")
                version = version.strip()
                print str(version) + " " + "1.0"
                if len(version) != 3:
                    version = ''
                    print str(version) + " " + "2.0"
                elif version[0] != '1':
                    version = ''
                    print str(version) + " " + "3.0"
                print str(version) + " " + "finally"

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
