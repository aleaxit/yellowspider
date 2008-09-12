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

def download_categories():
  def walker(arg, dirr, filess):
    for f in filess:
      if '.xml' == os.path.splitext(f)[1]:
        site_maps.append(f)

  os.path.walk(path, walker, 0)

  a = file(path+'/' + site_maps[0], 'r')

  soup = BeautifulStoneSoup(a.read())
  links = soup.findAll('loc')
  for link in links:
    categories.extend(link)


#download_categories()

def scan_categorie(cat):
  f = file('./categories/'+cat.split('yellowpages.com/')[1].replace('/', '_')+'.html', 'w+')
  page = urllib2.urlopen(cat).read()

  f.write(page)


#for c in categories:
#  scan_categorie(c)
#  print 'Loading ' + c
import re
def scrape(filename):
  companies = []  
  f = file(filename, 'r')
  soup = BeautifulSoup(f.read())
  ads = soup.findAll('li', attrs={"class" : re.compile("^listing")})
  for a in ads:
    comp = {}
    comp['company'] = a.h2.a.contents[0]
    comp['address'] = a.p.contents[0]
    comp['phone'] = a.li.contents[0]
    e = a.findAll('a', attrs={'class':'email'})
    for ee in e:
     comp['email'] = ee['href'].split('mailto:')[1]

    w = a.findAll('a', attrs={'class':'web'})
    for ww in w:
     comp['web'] = ww['href']

    companies.append(comp)
    print comp
  return companies


f1 = file('sample.txt', 'w+')
lines = ['company, address, phone, email, web']
for c in scrape('./categories/Adak-AK_Accounting-Services.html'):
  lines.append(','.join([str(c) for c in c.values()]))  

f1.writelines(lines)
f1.close()
