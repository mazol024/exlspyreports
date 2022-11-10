from ast import walk
import os
from pickletools import unicodestring1
import ebooklib
import codecs
from ebooklib import epub
from html.parser import HTMLParser
from zipfile import ZipFile


class MyHTMLParser(HTMLParser):
    flag = False
    data1 = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            self.flag = True
        else:
            self.flag = False

    def handle_endtag(self, tag):
        if tag == 'span':
            self.flag = False

    def handle_data(self, data):
        if self.flag:
            self.data1 = data


def prepbook():
    book1 = epub.read_epub("book1.epub")
    pg = book1.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    a = list(pg)

    zipfilename = "book1.epub"
    dir1 = 'epubbook'
    # if os.path.exists(dir1):
    #     for root, dirs, files in os.walk(dir1, topdown=False):
    #         for name in files:
    #             os.remove(os.path.join(root, name))
    #         for name in dirs:
    #             os.rmdir(os.path.join(root, name))
    #     with ZipFile(zipfilename, 'r') as zip:
    #         zip.extractall(dir1)
    # elif not os.path.exists(dir1):
    #     os.mkdir(dir1)
    #     with ZipFile(zipfilename, 'r') as zip:
    #         zip.extractall(dir1)
    # else:
    #     pass
    with ZipFile(zipfilename, 'r') as zip:
        # print(zip.read())
        b = zip.namelist()
        print(type(b))
        for a in b:
            print(a)
        print(zip.read(b[3]))
    return a


# @application.route('/readbook')
def readbook():
    b = prepbook()
    # return render_template('contents.html', chapters=b)
    return b


if __name__ == "__main__":
    b = prepbook()
    print("\nFinished")
    print("****")

    print("****")


# f = open('./'+dir1+'/OEBPS/'+b[5][0], 'r', encoding='utf8')
# # for i in f.readline():
# #     print(i.encode())
# print(f.read())
