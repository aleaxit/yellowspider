from time import time

from wsgiref import handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

class MainHandler(webapp.RequestHandler):
  def get(self):
    page = urlfetch.fetch('http://www.yellowpages.com/sitemap_index.xml')
    self.response.out.write(page.content)


def main():
  application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
  handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
