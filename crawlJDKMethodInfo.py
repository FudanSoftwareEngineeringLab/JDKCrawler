import MySQLdb
import requests
from scrapy import Selector


def download():
    type = ''
    name = ''
    return_type = ''
    is_static = 0
    try:
        # jdk version 7 and 8, class_id <= 8264 4240
        cur.execute("select class_id, doc_website from jdk_class where class_id > 4240 and class_id <= 8264")
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
            # print len(sel.xpath('//div[@class="summary"]/ul/li/ul').extract())
            # print sel.xpath('//div[@class="summary"]/ul/li/ul').extract()
            # print len(sel.xpath('//div[@class="summary"]/ul/li/ul'))
            block_list = sel.xpath('//div[@class="summary"]/ul/li/ul')
            for block in block_list:
                # print block.xpath('li/h3/text()').extract()[0]
                type = block.xpath('li/h3/text()').extract()[0].split()[0]
                # print block.xpath('li/table').extract()
                table = block.xpath('li/table')
                if table:
                    temp1 = table.xpath('tr/td[@class="colOne"]')
                    # print temp1
                    print len(temp1)
                    if temp1:
                        return_type = ''
                        for each in temp1:
                            # print temp1.xpath('code/span/a/text()').extract()[0]
                            # name = each.xpath('code/span/a/text()').extract()[0]
                            name = each.xpath('code/strong/a/text()').extract()[0]
                            print return_type + " " + name
                            cur.execute(
                                "insert into jdk_method(type,name,return_type,is_static,class_id) values(%s,%s,%s,%s,%s)",
                                (type, name, return_type, is_static, list[0]))
                            conn.commit()
                    else:
                        temp2 = table.xpath('tr/td')
                        print temp2.extract()
                        for each in temp2:
                            # print temp2.index(each) % 2
                            if (temp2.index(each) % 2) == 0:
                                return_type = ''
                                # print each.xpath('code/child::*/text()').extract()
                                # print each.xpath('code/text()').extract()
                                children = each.xpath('code/child::*/text()').extract()
                                texts = each.xpath('code/text()').extract()
                                if children != [] and texts != []:
                                    if texts[0].strip() == 'static':
                                        texts.remove(texts[0])
                                        is_static = 1
                                    else:
                                        is_static = 0
                                    length = min(len(texts), len(children))
                                    # print length
                                    for i in range(0, length):
                                        return_type += (children[i] + texts[i])
                                    if len(texts) > length:
                                        # print 1
                                        for j in range(length, len(texts)):
                                            return_type += texts[j]
                                    if len(children) > length:
                                        # print 2
                                        for j in range(length, len(children)):
                                            return_type += children[j]

                                elif children != [] and texts == []:
                                    for child in children:
                                        return_type += (children[children.index(child)] + " ")
                                elif children == [] and texts != []:
                                    if texts[0].find('static') != -1:
                                        texts[0] = texts[0].replace('static', '').strip()
                                        is_static = 1
                                    else:
                                        is_static = 0
                                    for text in texts:
                                        return_type += (texts[texts.index(text)] + " ")
                                else:
                                    return_type = ''

                            else:
                                # name = each.xpath('code/span/a/text()').extract()[0]
                                name = each.xpath('code/strong/a/text()').extract()[0]
                                print return_type + " " + name
                                cur.execute(
                                    "insert into jdk_method(type,name,return_type,is_static,class_id) values(%s,%s,%s,%s,%s)",
                                    (type, name, return_type, is_static, list[0]))
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