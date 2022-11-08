from ast import walk
from codecs import utf_16_be_encode, utf_16_decode, utf_16_encode
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
        if tag == 'h1':
            self.flag = True
        else:
            self.flag = False

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.flag = False

    def handle_data(self, data):
        if self.flag:
            self.data1 = data


def prepbook(resetbook):
    book1 = epub.read_epub("book1.epub")
    pg = book1.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    a = list(pg)
    b = []
    parser1 = MyHTMLParser()
    for a0 in a:
        parser1.feed(a0.get_content().decode())
        b.append([a0.get_name(), parser1.data1])
    print("****")
    for b0 in b:
        print(b0)
        indx = b.index(b0)
    print("****")
    zipfilename = "book1.epub"
    dir1 = 'epubbook'
    if os.path.exists(dir1) and resetbook:
        for root, dirs, files in os.walk(dir1, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        with ZipFile(zipfilename, 'r') as zip:
            zip.extractall(dir1)
    elif not os.path.exists(dir1):
        os.mkdir(dir1)
        with ZipFile(zipfilename, 'r') as zip:
            zip.extractall(dir1)
    else:
        pass


if __name__ == "__main__":
    prepbook(True)
    print("\nFinished")

# f = open('./'+dir1+'/OEBPS/'+b[5][0], 'r', encoding='utf8')
# # for i in f.readline():
# #     print(i.encode())
# print(f.read())
