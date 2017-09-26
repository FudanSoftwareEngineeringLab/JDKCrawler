import MySQLdb
import requests
from scrapy import Selector


def download():
    try:
        cur.execute("select package_id, doc_website, name from jdk_package where package_id <= 426")
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

            title = "Package " + each_list[2] + " Description"
            if sel.xpath('//h2[@title="' + title + '"]/following-sibling::div'):
                detail_description_block = sel.xpath('//h2[@title="' + title + '"]/following-sibling::div').extract()[0]
                print detail_description_block
                cur.execute("update jdk_package set detail_description = %s where package_id = %s",
                            (detail_description_block, each_list[0]))
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
