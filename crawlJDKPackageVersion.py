# coding:utf-8

import requests
import time
import MySQLdb
from scrapy.selector import Selector


def download():
    try:
        cur.execute("select package_id,doc_website from jdk_package")
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
            # print sel.xpath('//dl/dd/text()').extract()[0]
            version = ''
            if sel.xpath('//dl/dd/text()').extract() != []:
                version = sel.xpath('//dl/dd/text()').extract()[-1]
                if version.find('j') != -1 or version.find('J') != -1:
                    version = version[3:]
                version = version.replace("\n", "")
                version = version.strip()
                if len(version) != 3:
                    version = ''
            print version
            cur.execute("update jdk_package set first_version = %s where package_id = %s", (version, list[0]))
            conn.commit()
    except Exception, e:
        print Exception, ":", e
        # return -1


conn = MySQLdb.connect(
    host='10.131.252.156',
    port=3306,
    user='root',
    passwd='root',
    db='fdroid',
    charset='utf8'
)
cur = conn.cursor()

if __name__ == '__main__':
    download()
