import urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import os
import gzip
import re

class YellowSpider():
  def __init__(self, base):
    self.base = base
    

  def download_sitemap_xml_gz_files(self, outdir):
    page = urllib2.urlopen('http://www.yellowpages.com/sitemap_index.xml')
    site_map_xml = page.read()

    soup = BeautifulStoneSoup(site_map_xml)
    links = soup.findAll('loc')
    for link in links:
      name = link.string.split('/')[-1]
      a = file(outdir+name, 'w+')
      page = urllib2.urlopen(link.string)
      a.write(page.read())
      a.close()
      print 'File %s is done' %  name

  def unzip_files(self, path, outdir=None):
    outdir = outdir or path
    for i in [f for f in os.listdir(path) if f.split('.')[-1] == 'gz']:
      zfile = gzip.GzipFile(path+i)
      content = zfile.read()
      zfile.close()
      thefile = outdir + i.split('.gz')[0]
      file(thefile, 'w+').write(content)
      print 'Unzipping ',  thefile
      
  def extract_categories(self, path, outdir=None):
    outdir = outdir or path
    self.categories = []
 
    for f in [f for f in os.listdir(path) if f.split('.')[-1] == 'xml']:
      print f
      for link in BeautifulStoneSoup(file(outdir+f, 'r').read()).findAll('loc'):
        self.categories.extend(link)
        print len(self.categories), link
    
  def scan_categorie(self):
    f = file('./categories/'+cat.split('yellowpages.com/')[1].replace('/', '_')+'.html', 'w+')
    page = urllib2.urlopen(cat).read()

    f.write(page)


  def scrape(self, filename):
    companies = []  
    f = file(filename, 'r')
    soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.XML_ENTITIES)
    ads = soup(attrs={"class" : re.compile("^listing advertiser")})
    
    for a in ads:
        item = dict(name='', address='', phone='', email='', web='')
      
        item['name'] = a.h2.a.contents[0]
        try:
          item['address'] = ', '.join(a.p(text=True)[:2])
        except TypeError:
          print '!!!>>>>', a(text=True)

        print item['name'], '>>>    ', item['address']
        
        for i in a(attrs={'class':'number'}):
          item['phone'] = i.contents[0]

        for i in a('a', attrs={'class':'email'}):
         item['email'] = i['href'].split('mailto:')[1]

        for i in a('a', attrs={'class':'web'}):
         item['web']=i['href']
      
        item = '"'+'","'.join((item['name'], item['address'],item['phone'],item['email'],item['web']))+'"'
        companies.append(item)
   
    return companies

  def scrape_dir(self, path):
    companies = []
    for f in [f for f in os.listdir(path) if f.split('.')[-1] == 'html']:
      print '!!!Processing %s' % f
      companies.append(self.scrape(path+f))


  def save_companies(self, inpath, filename):

    f1 = file(filename, 'a+')
    
    for f in [f for f in os.listdir(inpath) if f.split('.')[-1] == 'html']:
      print '!!!Processing %s' % f
      f1.writelines([line+'\n' for line in self.scrape(inpath+f)])
      f1.flush()
      lines = []

    f1.close()

y = YellowSpider('/home/aivo/dev/yellowspider/')

#for a in  y.scrape('./pages/Anchorage-AK_Accounting-Services.html'):print a

y.save_companies('/home/aivo/dev/yellowspider/pages/', 'companies.txt')
#y.download_sitemap_xml_gz_files('/home/aivo/dev/yellowspider/categories/')
#y.extract_categories('/home/aivo/dev/yellowspider/sitemap/')






