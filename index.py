from time import time
import hashlib

from wsgiref import handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
  """Class for handling the root URL.
  """

  def get(self):
    ts = str(int(time()))
    appid = "2bDHbf3IkY2bp01sBtFL9nO_0_Bkcl0-"
    secret = "a34f389cbd135de4618eed5e23409d34450"

    sig = hashlib.md5("/WSLogin/V1/wslogin?appid=" + appid + "&ts=" + ts + secret).hexdigest()

    self.response.out.write(template.render('hello.html', {'ts': ts, 'sig': sig, 'appid': appid }))

def main():
  application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
  handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
