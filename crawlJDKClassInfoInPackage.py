# coding:utf-8

import requests
import MySQLdb
from scrapy.selector import Selector


def download(library_id, version, param1, param2, param3, param4, param5, param6, param7):
    try:
    #    sql = "select package_id,doc_website,name from jdk_package where library_id = " + str(library_id) + " and package_id = 792"
        sql = "select package_id,doc_website,name from jdk_package where library_id = " + str(library_id)
        cur.execute(sql)
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
            totals = sel.xpath(param1)
            for li in totals:
                type = li.xpath(param2).extract()[0]
                if library_id == 3 or library_id == 4:
                    temp = type.split()
                    type = temp[0]
                # print type
                classes = li.xpath(param3)
                # print len(classes)
                for each in classes:
                    tds = each.xpath('td')
                    class_name = tds[0].xpath(param4).extract()[0]
                    print class_name
                    name = list[2] + "." + class_name
                    # print name
                    a = tds[0].xpath(param5)[0]
                    count = list[2].count(".")
                    website = 'http://docs.oracle.com/javase/' + version + '/docs/api/' + a.xpath('@href').extract()[0][(3*(count + 1)):]
                    # print website
                    description = ''
                    if tds[1].xpath(param6).extract():
                        if len(tds[1].xpath(param6).extract()) > 1:
                            try:
                                child = tds[1].xpath(param7)
                                for i in range(0, len(tds[1].xpath(param6).extract())):
                                    if len(child.extract()) - 1 >= i:
                                        description += (tds[1].xpath(param6).extract()[i] + child.extract()[i])
                                    else:
                                        description += tds[1].xpath(param6).extract()[i]

                            except Exception, e:
                                print Exception, ":", e, "here cause exception1"
                        else:
                            description = tds[1].xpath(param6).extract()[0]

                        description = description.replace("\r\n", " ").replace("\n", " ").replace("  ", " ")
                        description = description.strip()
                    # print description

                    cur.execute(
                        "insert into jdk_class(name,class_name,description,type,doc_website,package_id) values(%s,%s,%s,%s,%s,%s)",
                        (name, class_name, description, type, website, list[0]))
                    conn.commit()
    except Exception, e:
        print Exception, ":", e, "here cause exception2"
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
    download(1, "8", '//div[@class="contentContainer"]/ul/li/table', 'tr/th/text()', 'tbody/tr', 'a/text()', 'a', 'div/text()', 'div/child::*')
    download(2, "7", '//div[@class="contentContainer"]/ul/li/table', 'tr/th/text()', 'tbody/tr', 'a/text()', 'a', 'div/text()', 'div/child::*')
    download(3, "6",'//table[@border="1"]', 'tr[@class="TableHeadingColor"]/th/font/b/text()', 'tr[@class="TableRowColor"]', 'b/a/text()', 'b/a', 'text()', 'child::*')
    download(4, "1.5.0", '//table[@border="1"][@cellpadding="3"][@summary]', 'tr[@class="TableHeadingColor"]/th/font/b/text()', 'tr[@class="TableRowColor"]', 'b/a/text()', 'b/a', 'text()', 'child::*')
