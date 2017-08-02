import MySQLdb
import requests
from scrapy import Selector


def download():
    try:
        # jdk version 7 and 8, class_id <= 8264
        cur.execute("select class_id, doc_website from jdk_class where class_id < 10")
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

            block_list = sel.xpath('//div[@class="details"]/ul/li/ul')
            for block in block_list:
                details = block.xpath('li/ul')
                print len(details)
                for each in details:
                    full_declaration = ''
                    return_string = ''
                    description = ''
                    print each.xpath('li/h4/text()').extract()[0]
                    name = each.xpath('li/h4/text()').extract()[0]
                    full_declaration_texts = each.xpath('li/pre/text()').extract()
                    full_declaration_children = each.xpath('li/pre/child::a/text()').extract()
                    # cur.execute("select class_id, doc_website from jdk_class where name = '" + name + "' and class_id = '" + list[0] + "' and full_declaration is null limit 1")
                    if len(full_declaration_children) == len(full_declaration_texts):
                        if full_declaration_texts[0].find("void") != -1:
                            for i in range(0, len(full_declaration_children)):
                                full_declaration += (full_declaration_texts[i] + full_declaration_children[i])
                        else:
                            for i in range(0, len(full_declaration_children)):
                                full_declaration += (full_declaration_children[i] + full_declaration_texts[i])
                    elif len(full_declaration_children) <len(full_declaration_texts):
                        for i in range(0, len(full_declaration_children)):
                            full_declaration += (full_declaration_texts[i] + full_declaration_children[i])
                        for i in range(len(full_declaration_children), len(full_declaration_texts)):
                            full_declaration += full_declaration_texts[i]
                    else:
                        break
                    # print full_declaration
                    if each.xpath('li/dl/dt/span[@class="returnLabel"]'):
                        # print each.xpath('li/dl/dt/span[@class="returnLabel"]/parent::*/following-sibling::dd[position()=1]').extract()[0]
                        return_string = each.xpath('li/dl/dt/span[@class="returnLabel"]/parent::*/following-sibling::dd[position()=1]').extract()[0]
                    if each.xpath('li/div[@class="block"]'):
                        description = each.xpath('li/div[@class="block"]').extract()[0]
                        print description



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