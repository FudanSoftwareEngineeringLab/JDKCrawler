import MySQLdb
import requests

from scrapy import Selector


def download_libraries():
    try:
        cur.execute("select doc_website from jdk_library")
        lists = cur.fetchall()
        for each in lists:
            print each[0]
            url = each[0] + "overview-summary.html"
            while 1 == 1:
                try:
                    sel = Selector(requests.get(url, timeout=10))
                except Exception, e:
                    print 'timeout'
                    continue
                break
            body = sel.xpath('//body').extract()[0]
            #print body
            cur.execute("insert into javadoc_body(doc_website, html_body) values(%s, %s)", (each[0], body))
            conn.commit()

    except Exception, e:
        print Exception, ":", e


def download_packages():
    try:
        cur.execute("select doc_website from jdk_package")
        lists = cur.fetchall()
        for each in lists:
            print each[0]
            while 1 == 1:
                try:
                    sel = Selector(requests.get(each[0], timeout=10))
                except Exception, e:
                    print 'timeout'
                    continue
                break
            body = sel.xpath('//body').extract()[0]
            #print body
            cur.execute("insert into javadoc_body(doc_website, html_body) values(%s, %s)", (each[0], body))
            conn.commit()

    except Exception, e:
        print Exception, ":", e


def download_classes():
    try:
        cur.execute("select doc_website from jdk_class")
        lists = cur.fetchall()
        for each in lists:
            print each[0]
            while 1 == 1:
                try:
                    sel = Selector(requests.get(each[0], timeout=10))
                except Exception, e:
                    print 'timeout'
                    continue
                break
            body = sel.xpath('//body').extract()[0]
            #print body
            cur.execute("insert into javadoc_body(doc_website, html_body) values(%s, %s)", (each[0], body))
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
    download_libraries()
    download_packages()
    download_classes()