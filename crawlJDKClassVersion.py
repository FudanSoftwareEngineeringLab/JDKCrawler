import MySQLdb
import requests
from scrapy import Selector


def download():
    try:
        # cur.execute("select class_id, doc_website from jdk_class where class_id > 0 and class_id < 100")
        cur.execute("select class_id, doc_website, package_id from jdk_class")
        lists = cur.fetchall()
        # print lists
        for list in lists:
            print list[0]
            while 1 == 1:
                try:
                    sel = Selector(requests.get(list[1], timeout=10))
                except Exception, e:
                    print 'timeout'
                    continue
                break

            library_id = 0
            try:
                cur.execute("select library_id from jdk_package where package_id = " + str(list[2]))
                library_id = cur.fetchall()[0][0]
            except Exception, e:
                print Exception, ":", e

            print library_id
            version = ''
            if library_id != 0:
                if library_id <= 2:
                    if sel.xpath('//div[@class="description"]/ul/li/dl/dt/span[contains(text(), "Since:")]'):
                        version_tag = sel.xpath('//div[@class="description"]/ul/li/dl/dt/span[contains(text(), "Since")]/parent::*/following-sibling::dd/text()').extract()
                        print version_tag
                        version = version_tag[0]
                else:
                    if sel.xpath('//dl/dt/b[contains(text(), "Since:")]'):
                        version_tag = sel.xpath('//dl/dt/b[contains(text(), "Since:")]/parent::*/following-sibling::dd')
                        print version_tag
                        for each in version_tag:
                            if each.xpath('text()') and each.xpath('text()').extract() != [u', \n']:
                                # print each.xpath('text()').extract()
                                # print each.xpath('parent::*').extract()
                                # print each.xpath('parent::*/preceding-sibling::table')
                                # print len(each.xpath('parent::*/preceding-sibling::table'))
                                if len(each.xpath('parent::*/preceding-sibling::table')) > 0:
                                    version = each.xpath('text()').extract()[0]
                                    break

                if version.find("J") != -1 or version.find("j") != -1:
                    version = version[3:]
                version = version.replace("\n", "")
                version = version.strip()
                print version

                cur.execute("update jdk_class set first_version = %s where class_id = %s", (version, list[0]))
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
