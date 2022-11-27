from bs4 import BeautifulSoup
import os


def tocarray(ff):
    root = ff + "/"
    fl = open(root+'META-INF/container.xml').read()
    soup = BeautifulSoup(fl, 'xml')
    opf = dict(soup.find('rootfile').attrs)['full-path']
    basedir = os.path.dirname(opf)
    if basedir:
        basedir = '{0}/'.format(basedir)
    ff2 = open(ff+'/'+opf)
    soup = BeautifulSoup(ff2, features="lxml")

    # # title
    booktitle = soup.find('dc:title').text
    # print(f"booktitle is : {booktitle} ")
    # all files, not in order
    x, ncx = {}, None
    for item in soup.find('manifest').findAll('item'):
        d = dict(item.attrs)
        x[d['id']] = '{0}{1}'.format(basedir, d['href'])
        if d['media-type'] == 'application/x-dtbncx+xml':
            ncx = '{0}{1}'.format(basedir, d['href'])

    y = []
    for item in soup.find('spine').findAll('itemref'):
        y.append(x[dict(item.attrs)['idref']])
    z = {}
    pp = []
    if ncx:
        # get titles from the toc
        fncx = open(root + ncx)
        soup = BeautifulSoup(fncx, 'lxml')

        for navpoint in soup('navpoint'):
            k = navpoint.content.get('src', None)
            # strip off any anchor text
            # k = root + basedir + k.split('#')[0]
            k = root + basedir + k
            if k:
                z[k] = navpoint.navlabel.text
                pp.append([z[k], k])
                # print(k, z[k])
    return (booktitle, pp)


if __name__ == '__main__':
    # tt('epubbook')
    pp = tocarray('epubbook')
    print(pp[0])
    print(pp[1])
    # one()
    print("Done")
