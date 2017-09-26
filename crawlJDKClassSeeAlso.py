import MySQLdb
import requests
from scrapy import Selector


def generate_href(doc_website, href):
    if href.find("#") != -1:
        index = href.find("#")
        href = href[:index]
    href = href.replace('../', '')
    prefix = doc_website[:41]
    result = prefix + href
    return result


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
            if sel.xpath('//div[@class="description"]/ul/li/dl/dt/span[@class="seeLabel"]/text()'):
                see_also_title = sel.xpath('//div[@class="description"]/ul/li/dl/dt/span[@class="seeLabel"]/text()').extract()[0]
                print see_also_title
                if see_also_title == "See Also:":
                    see_also_objects = sel.xpath('//div[@class="description"]/ul/li/dl/dt/span[@class="seeLabel"]/parent::*/following-sibling::dd/a')
                    print see_also_objects
                    for each in see_also_objects:
                        print each.extract()
                        href = each.xpath('@href').extract()[0]
                        print href
                        final_href = generate_href(each_list[1], href)
                        print final_href
                        print each.xpath('child::*')
                        if each.xpath('child::*'):
                            content_title = each.xpath('child::*').extract()[0]
                        else:
                            content_title = each.xpath('text()').extract()[0]
                        print content_title
                        cur.execute("insert into jdk_class_see_also (see_also_title, see_also_website, class_id) values (%s, %s, %s)", (content_title, final_href, each_list[0]))
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
