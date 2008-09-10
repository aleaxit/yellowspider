import urllib2

page = urllib2.urlopen('http://www.yellowpages.com/sitemap_index.xml')
print page.read()