import os
import shutil
from pickletools import unicodestring1
from zipfile import ZipFile
from bs4 import BeautifulSoup


def get_toc(bookdir='templates/ebooks/2/'):
    bookdir = bookdir
    # bookdir = 'templates/ebooks/2/'
    ff = os.scandir(bookdir)
    for i in ff:
        if i.is_file():
            zipfilename = bookdir + i.name
    print(f"fil1 zipname : {zipfilename}")
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

        soup = BeautifulSoup(
            zip.read('META-INF/container.xml'), features='xml')
        opf = dict(soup.find('rootfile').attrs)['full-path']

        basedir = os.path.dirname(opf)
        if basedir:
            basedir = '{0}/'.format(basedir)

        c = zip.read(opf)
        soup = BeautifulSoup(c, features='xml')
        print(" Title of the book : ", soup.find('dc:title').text)
        x, ncx = {}, None
        for item in soup.find('manifest').findAll('item'):
            d = dict(item.attrs)
            x[d['id']] = '{0}{1}'.format(basedir, d['href'])
            if len(x) <= 5:
                print(x, '\n')
            if d['media-type'] == 'application/x-dtbncx+xml':
                ncx = '{0}{1}'.format(basedir, d['href'])
            elif d['id'] == 'ncxtoc':
                ncx = '{0}{1}'.format(basedir, d['href'])
        # for a in b:
        #     print(a)
        # print(zip.read(b[3]))
        print(f"ncx is  :  {ncx}")
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
                if k:
                    k = bookdir + basedir + k
                    z[k] = navpoint.navlabel.text
                    pp.append([z[k], k])
            if len(pp) <= 1:
                for li in soup.find('ol').findAll('li'):
                    pp.append([bookdir + basedir +
                               li.find('a')['href'], li.text])

    return pp

# @application.route('/set_books')


def set_books(basedir='templates/ebooks/'):
    # check dir if new book here and unpuck it
    listdirs = os.scandir(basedir)
    numlist = [0]
    flist = []
    for i in listdirs:
        if i.is_dir():
            # print(i)
            # print(os.path.basename(i))
            numlist.append(int(os.path.basename(i)))
        if i.is_file():
            flist.append(i)
    print(numlist)
    maxnum = max(numlist)
    print(maxnum, " next value -> ", maxnum+1)
    print(basedir + str(maxnum + 1) + '/')
    for f in flist:
        maxnum += 1
        os.makedirs(basedir+str(maxnum)+'/')
        shutil.move(f, basedir+str(maxnum)+'/')
        print("File moved!")
        ff = os.scandir(basedir+str(maxnum)+'/')
        for i in ff:
            if i.is_file():
                with ZipFile(i, 'r') as zip:
                    zip.extractall(basedir+str(maxnum)+'/book/')


if __name__ == "__main__":
    basedir = 'templates/ebooks/'
    set_books()
    b = get_toc('templates/ebooks/2/')
    print("\nFinished")
    print("Returned data: ")
    for i in b:
        # print((i[0]).strip(), " -> ", i[1])
        print(i)
    print("****")


# f = open('./'+dir1+'/OEBPS/'+b[5][0], 'r', encoding='utf8')
# # for i in f.readline():
# #     print(i.encode())
# print(f.read())
