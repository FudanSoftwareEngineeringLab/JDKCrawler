import MySQLdb
import requests
from scrapy import Selector


def generate_href(doc_website, href):
    href = href.replace('../', '')
    prefix = doc_website[:41]
    result = prefix + href
    return result

def download():
    try:
        cur.execute("select class_id, doc_website from jdk_class where class_id <= 4240")
        lists = cur.fetchall()
        for every in lists:
            print every[0]
            while 1 == 1:
                try:
                    sel = Selector(requests.get(every[1], timeout=10))
                except Exception, e:
                    print 'timeout'
                    continue
                break

            block_list = sel.xpath('//div[@class="details"]/ul/li/ul')
            for block in block_list:
                details = block.xpath('li/ul')
                for each in details:
                    full_declaration = each.xpath('li/pre').extract()[0]
                    cur.execute(
                        "select method_id from jdk_method where full_declaration = '" + full_declaration + "' and class_id = " + str(every[0]))
                    method_id = cur.fetchall()[0][0]
                    #print each.xpath('li/dl/dt/span[@class="seeLabel"]')
                    if each.xpath('li/dl/dt/span[@class="seeLabel"]'):
                        #print each.xpath('li/dl/dt/span[@class="seeLabel"]/text()').extract()[0]
                        if each.xpath('li/dl/dt/span[@class="seeLabel"]/text()').extract()[0] == "See Also:":
                            following_tags_dd = each.xpath(
                                'li/dl/dt/span[@class="seeLabel"]/parent::*/following-sibling::dd/a')
                            for each_tag in following_tags_dd:
                                href = each_tag.xpath('@href').extract()[0]
                                if each_tag.xpath('child::*'):
                                    content_title = each_tag.xpath('child::*').extract()[0]
                                else:
                                    content_title = each_tag.xpath('text()').extract()[0]
                                print content_title
                                final_href = generate_href(every[1], href)
                                print final_href
                                cur.execute("insert into jdk_method_see_also (see_also_title, see_also_website, class_id, method_id) values (%s, %s, %s, %s)", (content_title, final_href, every[0], method_id))
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