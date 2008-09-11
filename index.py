import urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

def download_sitemap():
  page = urllib2.urlopen('http://www.yellowpages.com/sitemap_index.xml')
  site_map_xml = page.read()

  soup = BeautifulStoneSoup(site_map_xml)
  links = soup.findAll('loc')
  for link in links:
    name = link.string.split('/')[-1]
    a = file(name, 'w+')
    page = urllib2.urlopen(link.string)
    a.write(page.read())
    a.close()
    print 'File %s is done' %  name


import os

path='./sitemap'
site_maps = []
categories = []

def unwind():
  def walker(arg, dirr, filess):
    for f in filess:
      if '.xml' == os.path.splitext(f)[1]:
        site_maps.append(f)

  os.path.walk(path, walker, 0)

  a = file(path+'/' + site_maps[0], 'r')

  soup = BeautifulStoneSoup(a.read(1024))
  links = soup.findAll('loc')
  for link in links:
    categories.extend(link)


unwind()


def spider():
  page = urllib2.urlopen(categories[0]).read()

  print page
  return
  soup = BeautifulSoup(page)
  links = soup.findAll('loc')
  for link in links:
    name = link.string.split('/')[-1]


spider()