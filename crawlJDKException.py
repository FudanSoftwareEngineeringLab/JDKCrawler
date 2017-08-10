import MySQLdb
import requests
from scrapy import Selector


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
                    method_name = each.xpath('li/h4/text()').extract()[0]
                    # print method_name
                    cur.execute(
                        "select method_id from jdk_method where full_declaration = '" + full_declaration + "' and name = '" + method_name + "' and class_id = " + str(
                            every[0]))
                    method_id = cur.fetchall()[0][0]
                    # print "method_id: " + str(method_id)
                    if each.xpath('li/dl/dt/span[@class="throwsLabel"]'):
                        if each.xpath('li/dl/dt/span[@class="throwsLabel"]/text()').extract()[0] == "Throws:":
                            exception_count = 0
                            exceptions = []
                            following_tags_dd = each.xpath('li/dl/dt/span[@class="throwsLabel"]/parent::*/following-sibling::dd')
                            if each.xpath('li/dl/dt/span[@class="throwsLabel"]/parent::*/following-sibling::dt'):
                                following_tags_dt = each.xpath('li/dl/dt/span[@class="throwsLabel"]/parent::*/following-sibling::dt')
                                next_dt = following_tags_dt[0]
                                preceding_tags_dd = next_dt.xpath('preceding-sibling::dd')
                                set_following_tags_dd = set(list(following_tags_dd.extract()))
                                set_preceding_tags_dd = set(list(preceding_tags_dd.extract()))

                                exceptions = list(set_following_tags_dd & set_preceding_tags_dd)
                                exception_count = len(exceptions)
                            else:
                                exception_count = len(following_tags_dd)
                                exceptions = following_tags_dd.extract()

                            print exception_count
                            print exceptions

                            for ex in exceptions:
                                temp_str = ex[:ex.find("</code>")]
                                temp_str = temp_str.replace("<dd>", "").replace("<code>", "").replace("</a>", "")
                                exception_class = temp_str[temp_str.find(">") + 1:]
                                print exception_class
                                description = ex[ex.find("</code>") + 9:].replace("</dd>", "").replace("\n", "").replace("  ", "").strip()
                                if description == "dd>":
                                    description = ''
                                print description
                                cur.execute("insert into jdk_exception(name, class_id, method_id, description) values(%s, %s, %s, %s)", (exception_class, every[0], method_id, description))
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
