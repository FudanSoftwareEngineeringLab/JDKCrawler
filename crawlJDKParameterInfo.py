import MySQLdb
import requests
from scrapy import Selector


def download():
    try:
        # jdk version 7 and 8, class_id <= 8264 4240
        cur.execute("select class_id, doc_website from jdk_class where class_id >= 406 and class_id <= 1000")
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
                for each in details:
                    full_declaration = each.xpath('li/pre').extract()[0]
                    method_name = each.xpath('li/h4/text()').extract()[0]
                    # print full_declaration
                    cur.execute("select method_id from jdk_method where full_declaration = '" + full_declaration + "' and name = '" + method_name +"' and class_id = '" + str(list[0]) + "'")
                    method_id = cur.fetchall()[0][0]
                    last_bracket = find_last(full_declaration, "(")
                    if full_declaration.find("throws") != -1:
                        full_declaration = full_declaration[last_bracket: full_declaration.find("throws")]
                    else:
                        full_declaration = full_declaration[last_bracket:]

                    #print full_declaration
                    if full_declaration.find("&lt;") != -1:
                        full_declaration = full_declaration.replace(full_declaration[full_declaration.find("&lt;"):(full_declaration.find("&gt;") + 4)], '')
                    param_count = full_declaration.count(",") + 1
                    # print method_id
                    full_declaration = full_declaration.replace('\n', "").replace("    ", "").strip()
                    # print each.xpath('li/dl/dt/span[@class="paramLabel"]')
                    if each.xpath('li/dl/dt/span[@class="paramLabel"]'):
                        if each.xpath('li/dl/dt/span[@class="paramLabel"]/text()').extract()[0] == "Parameters:":
                            print full_declaration
                            print param_count
                            params = each.xpath(
                                'li/dl/dt/span[@class="paramLabel"]/parent::*/following-sibling::dd[position()<=' + str(
                                    param_count) + ']')
                            # print params
                            for param in params:
                                name_des = param.extract()
                                # print name_des
                                name = name_des[10:(name_des.index("</code>"))]
                                # name = param.xpath('code/text()').extract()[0]
                                print name
                                description = name_des[(name_des.index("</code>") + 10): -5].replace("  ", "").replace(
                                    "\n", "").strip()
                                # print description
                                index = -1
                                ss = ''

                                while True:
                                    index = full_declaration.index(name)
                                    tmp = full_declaration.index(name) + len(name)
                                    tmp_str = full_declaration[tmp]
                                    if tmp_str == ")" or tmp_str == ",":
                                        strs = full_declaration[:index]
                                        # print strs

                                        begin_index = -1
                                        if find_last(strs, "(") > find_last(strs, ","):
                                            begin_index = find_last(strs, "(")
                                        else:
                                            begin_index = find_last(strs, ",")

                                        ss = strs[(begin_index + 1):]

                                        ss = ss.replace("   ", "")
                                        ss = ss.strip()

                                        # print ss
                                        break
                                    full_declaration = full_declaration[tmp:]

                                type_string = ''
                                if ss.find("<a href") != -1:
                                    end_index = ss.find("</a>")
                                    ss = ss.replace("</a>", "")
                                    tmp_index = ss.find(">") + 1
                                    type_string = ss[tmp_index: end_index]
                                    print type_string
                                    # version 8 (1, 217); version 7 (218, 426)
                                    cur.execute(
                                        "select class_id from jdk_class where class_name = '" + type_string + "' and package_id < 218")
                                    type_classes = cur.fetchall()
                                    if type_classes:
                                        type_class = type_classes[0][0]
                                    else:
                                        type_class = 0

                                else:
                                    type_string = ss
                                    type_class = 0

                                print type_string
                                print "type_class: " + str(type_class)

                                cur.execute("insert into jdk_parameter(name, class_id, method_id, type_class, type_string, description) values (%s, %s, %s, %s, %s, %s)", (name, list[0], method_id, type_class, type_string, description))
                                conn.commit()


    except Exception, e:
        print Exception, ":", e

conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='jdk_data',
    charset='utf8'
)
cur = conn.cursor()


def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position

if __name__ == "__main__":
    download()