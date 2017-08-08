import MySQLdb
import requests
from scrapy import Selector


def download():
    try:
        # jdk version 7 and 8, class_id <= 8264
        cur.execute("select class_id, doc_website from jdk_class where class_id <= 4240")
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
                # print len(details)
                for each in details:
                    full_declaration = ''
                    return_string = ''
                    description = ''
                    first_version = ''
                    override = ''
                    specified_by = ''
                    print each.xpath('li/h4/text()').extract()[0]
                    name = each.xpath('li/h4/text()').extract()[0]
                    full_declaration = each.xpath('li/pre').extract()[0]
                    # print full_declaration
                    if each.xpath('li/div[@class="block"]'):
                        description = each.xpath('li/div[@class="block"]').extract()[0]
                        # print description
                    # javadoc 8
                    if each.xpath('li/dl/dt/span[@class="returnLabel"]'):
                        # print each.xpath('li/dl/dt/span[@class="returnLabel"]/parent::*/following-sibling::dd[position()=1]').extract()[0]
                        return_string = each.xpath('li/dl/dt/span[@class="returnLabel"]/parent::*/following-sibling::dd[position()=1]').extract()[0]

                    if each.xpath('li/dl/dt/span[@class="simpleTagLabel"]'):
                        if each.xpath('li/dl/dt/span[@class="simpleTagLabel"]/text()').extract()[0].find("Since") != -1:
                            # print each.xpath('li/dl/dt/span[@class="simpleTagLabel"]/parent::*/following-sibling::dd[position()=1]/text()').extract()[0]
                            first_version = each.xpath(
                                'li/dl/dt/span[@class="simpleTagLabel"]/parent::*/following-sibling::dd[position()=1]/text()').extract()[0]
                            if first_version.find("J") != -1 or first_version.find("j") != -1:
                                first_version = first_version[3:]
                            first_version = first_version.replace("\n", "")
                            first_version = first_version.strip()
                            # print first_version
                    if each.xpath('li/dl/dt/span[@class="overrideSpecifyLabel"]'):
                        temps = each.xpath('li/dl/dt/span[@class="overrideSpecifyLabel"]')
                        for temp in temps:
                            title = temp.xpath('text()').extract()[0]
                            # print title
                            # print each.xpath('li/dl/dt/span[@class="overrideSpecifyLabel"]/parent::*/following-sibling::dd[position()=1]').extract()
                            temps_children = temp.xpath('parent::*/following-sibling::dd[position()=1]/child::*/a/text()').extract()
                            temps_texts = temp.xpath('parent::*/following-sibling::dd[position()=1]/text()').extract()
                            # print temps_children
                            # print temps_texts
                            result = ''
                            for i in range(0, len(temps_texts)):
                                result += (temps_children[i] + temps_texts[i])
                            for i in range(len(temps_texts), len(temps_children)):
                                result += temps_children[i]
                            if title.find("Overrides") != -1:
                                # print title + " " + result
                                override = result
                            else:
                                # print title + " " + result
                                specified_by = result

                        cur.execute(
                            "update jdk_method set full_declaration = %s, return_string = %s, description = %s, first_version = %s, override = %s, specified_by = %s where name = %s and class_id = %s and full_declaration is null limit %s",
                            (full_declaration, return_string, description, first_version, override, specified_by, name, list[0], 1))
                        conn.commit()
                    else:
                        cur.execute(
                            "update jdk_method set full_declaration = %s, return_string = %s, description = %s, first_version = %s where name = %s and class_id = %s and full_declaration is null limit 1",
                            (full_declaration, return_string, description, first_version, name, list[0]))
                        conn.commit()

                    # javadoc 7
                    '''if each.xpath('li/dl/dt/span[@class="strong"]'):
                        temps = each.xpath('li/dl/dt/span[@class="strong"]')
                        for temp in temps:
                            brother = temp.xpath('parent::*/following-sibling::dd[position()=1]')
                            title = temp.xpath('text()').extract()[0]
                            # print title + " " + brother
                            if title.find("Returns") != -1:
                                return_string = brother.extract()[0]
                            if title.find("Since") != -1:
                                first_version = brother.xpath('text()').extract()[0]
                                if first_version.find("J") != -1 or first_version.find("j") != -1:
                                    first_version = first_version[3:]
                                first_version = first_version.replace("\n", "")
                                first_version = first_version.strip()

                    if each.xpath('li/dl/dt/strong/text()'):
                        temps = each.xpath('li/dl/dt/strong')
                        for temp in temps:
                            title = temp.xpath('text()').extract()[0]
                            brother = temp.xpath('parent::*/following-sibling::dd[position()=1]')
                            if title.find("Overrides") != -1:
                                override = brother.extract()[0]
                            if title.find("Specified") != -1:
                                specified_by = brother.extract()[0]
                    #print "full_declaration: " + full_declaration
                    #print "description: " + description
                    #print "return_string: " + return_string
                    #print "first_version: " + first_version
                    print "override: " + override
                    print "specified_by: " + specified_by
                    cur.execute(
                        "update jdk_method set full_declaration = %s, return_string = %s, description = %s, first_version = %s, override = %s, specified_by = %s where name = %s and class_id = %s and full_declaration is null limit 1",
                        (full_declaration, return_string, description, first_version, override, specified_by, name, list[0]))
                    conn.commit()'''

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