# coding:utf-8
import MySQLdb
import requests
from scrapy import Selector


def download_old(version, library_id, param1, param2, param3, param4, param5):
    url = "http://docs.oracle.com/javase/" + version + "/docs/api/overview-summary.html"
    try:
        while 1 == 1:
            try:
                sel = Selector(requests.get(url, timeout=10))
            except Exception, e:
                print 'timeout'
                continue
            break
        totals = sel.xpath(param1)
        # print totals[122].xpath('td/text()').extract()
        for tr in totals:
            tds = tr.xpath('td')
            packageName = tds[0].xpath(param2).extract()[0]
            a = tds[0].xpath(param3)[0]
            website = 'http://docs.oracle.com/javase/' + version + '/docs/api/' + a.xpath('@href').extract()[0]
            description = ''
            if len(tds[1].xpath(param4).extract()):
                if len(tds[1].xpath(param4).extract()) > 1:
                    try:
                        child = tds[1].xpath(param5)
                        for i in range(0, len(tds[1].xpath(param4).extract())):
                            if len(child.extract()) - 1 >= i:
                                description += (tds[1].xpath(param4).extract()[i] + child.extract()[i])
                            else:
                                description += tds[1].xpath(param4).extract()[i]

                    except Exception, e:
                        print Exception, ":", e
                else:
                    description = tds[1].xpath(param4).extract()[0]

            description = description.replace("\r\n", " ").replace("\n", " ").replace("  ", " ")
            description = description.strip()
            print str(len(tds[1].xpath(param4).extract())) + " " + " " + packageName + " " + website + " " + description
            cur.execute("insert into jdk_package(name, description, doc_website, library_id) values (%s, %s, %s, %s)", (packageName, description, website, library_id))
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

if __name__ == '__main__':
    download_old("8", 1, '//div[@class="contentContainer"]/table/tbody/tr', 'a/text()', 'a', 'div/text()', 'div/child::*')
    download_old("7", 2, '//div[@class="contentContainer"]/table/tbody/tr', 'a/text()', 'a', 'div/text()', 'div/child::*')
    download_old("6", 3, '//body/table[@border="1"]/tr[@class="TableRowColor"]', 'b/a/text()', 'b/a', 'text()', 'child::*')
    download_old("1.5.0", 4, '//body/table[@border="1"]/tr[@class="TableRowColor"]', 'b/a/text()', 'b/a', 'text()', 'child::*')
