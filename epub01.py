import os
from pickletools import unicodestring1
from zipfile import ZipFile
from bs4 import BeautifulSoup


def prepbook():
    # book1 = epub.read_epub("book1.epub")
    # pg = book1.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    # a = list(pg)

    bookdir = 'templates/ebooks/2/'
    zipfilename = bookdir + os.listdir(bookdir)[0]
    print(f"fil1 -> {zipfilename}")
    with ZipFile(zipfilename, 'r') as zip:
        b = zip.namelist()
        soup = BeautifulSoup(
            zip.read('META-INF/container.xml'), features='xml')
        opf = dict(soup.find('rootfile').attrs)['full-path']

        basedir = os.path.dirname(opf)
        if basedir:
            basedir = '{0}/'.format(basedir)

        c = zip.read(opf)
        soup = BeautifulSoup(c, features='xml')
        print(soup.find('dc:title').text)
        x, ncx = {}, None
        for item in soup.find('manifest').findAll('item'):
            d = dict(item.attrs)
            x[d['id']] = '{0}{1}'.format(basedir, d['href'])
            if d['media-type'] == 'application/x-dtbncx+xml':
                ncx = '{0}{1}'.format(basedir, d['href'])
        # for a in b:
        #     print(a)
        # print(zip.read(b[3]))
        print(f"ncx  {ncx}")
        z = {}
        pp = []
        if ncx:
            # get titles from the toc
            #n = zip.read('OEBPS/html/toc.ncx')
            n = zip.read(ncx)
            soup = BeautifulSoup(n, 'lxml')
            for navpoint in soup('navpoint'):
                k = navpoint.content.get('src', None)
                # strip off any anchor text
                # k = root + basedir + k.split('#')[0]
                k = bookdir + basedir + k
                if k:
                    z[k] = navpoint.navlabel.text
                    pp.append([z[k], k])

    dumpdir = bookdir+'/dump/'
    if os.path.exists(dumpdir) and False:
        for root, dirs, files in os.walk(dumpdir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        with ZipFile(zipfilename, 'r') as zip:
            zip.extractall(dumpdir)
    elif not os.path.exists(dumpdir):
        os.mkdir(dumpdir)
        with ZipFile(zipfilename, 'r') as zip:
            zip.extractall(dumpdir)
    else:
        pass
    return b


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
