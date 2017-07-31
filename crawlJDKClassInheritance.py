import MySQLdb
import requests
from scrapy import Selector


def download():
    try:
        cur.execute("select class_id, doc_website, type, package_id from jdk_class where class_id > 8800 and class_id < 8900")
        #cur.execute(
        #    "select class_id, doc_website, type, package_id from jdk_class where class_id = 8835")
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

            cur.execute("select library_id from jdk_package where package_id = '" + str(list[3]) + "'")
            library_ids = cur.fetchall()
            # print library_ids
            library_id = library_ids[0][0]
            # type includes: class, interface, enum, exception, annotation type, error
            print list[2]
            if list[2] == "Class" or list[2] == "Error" or list[2] == "Exception":
                extend_class = ''
                num = ''
                website = ''
                href = ''
                if library_id <= 2:
                    # print sel.xpath('//ul[@class="inheritance"]/li/a/text()').extract()[-1]
                    href = sel.xpath('//ul[@class="inheritance"]/li/a/@href').extract()[-1]
                    href = href.replace("../", "")
                    print href
                else:
                    strs = sel.xpath('//pre/a/text()').extract()
                    # print strs
                    for each in strs:
                        if each.find('.') == -1:
                            num = strs.index(each) - 1
                            extend_class = strs[strs.index(each) - 1]
                            break
                    if extend_class == '':
                        num = len(strs) - 1
                        extend_class = strs[-1]

                    print num

                    hrefs = sel.xpath('//pre/a/@href').extract()
                    hrefs[num] = hrefs[num].replace('../', '')
                    href = hrefs[num]
                    print hrefs[num]

                index = list[1].find('docs/api')
                prefix = list[1][:index]
                website = prefix + 'docs/api/' + href
                print website

                sql = "select class_id from jdk_class where doc_website = '" + website + "'"
                # print sql
                cur.execute(sql)
                class_ids = cur.fetchall()
                print class_ids

                class_id = class_ids[0][0]
                print class_id

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