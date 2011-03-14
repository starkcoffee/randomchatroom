import cgi
import os
import re
import datetime
import logging
import Cookie

from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

class Message(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  alias = db.StringProperty()


class MessageView:
  def __init__(self, message):
    self.message = message
    if message.alias:
      self.author = message.alias
    else:
      self.author = "A monkey"

    now = datetime.datetime.now()
    timedelta = now - message.date
    self.ago_minutes = timedelta.seconds / 60
    self.content = message.content


class MainPage(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

def getFilter():
    words = memcache.get("rudish_words")
    if words is not None:
        return words
    else:
        file = open("filter","r")
        words = file.readlines()
        file.close()
        memcache.add("rudish_words",words,600)
        return words

def filter(string):
    rudishWords = getFilter()
    for word in rudishWords:
        pattern = re.compile(word,re.IGNORECASE | re.VERBOSE)
        string = re.sub(pattern,'banana',string)
    return string
#BEWBS
class Messages(webapp.RequestHandler):
  def post(self):
    message = Message()
    
    alias = self.request.get('alias')
    if alias:        
        cookie = Cookie.SimpleCookie()
        cookie['alias'] = alias
        print cookie 
    elif self.request.cookies.get('alias'):
        alias = self.request.cookies.get('alias')

    content = self.request.get('content')

    message.alias = filter(alias)
    message.content = filter(self.request.get('content'))
    message.put()

    memcache.set("last_message_posted_at", datetime.datetime.utcnow())    

    self.redirect('/')

  def get(self):
    lastModifiedTime = memcache.get("last_message_posted_at") 

    # would be nice to initialize lastModifiedTime in memcache on app startup somehow so we dont need the None check
    if lastModifiedTime is None:
        lastModifiedTime = datetime.datetime.utcnow()
        memcache.set("last_message_posted_at", datetime.datetime.utcnow())    

    if self.request.headers.get('If-Modified-Since') == lastModifiedTime.strftime('%a, %d %b %Y %H:%M:%S GMT'): 
        return self.response.set_status(304) 
    

    messages_query = Message.all().order('-date')
    messages = messages_query.fetch(50)

    message_views = []
    for message in messages:
       message_views.append(MessageView(message))

    template_values = {
      'messages': message_views,
    }

    path = os.path.join(os.path.dirname(__file__), '_messages.html')
    self.response.out.write(template.render(path, template_values))
    self.response.headers['Cache-Control'] = 'must-revalidate'
    self.response.headers['Expires'] = ''
    self.response.headers['Last-Modified'] = lastModifiedTime.strftime('%a, %d %b %Y %H:%M:%S GMT')
  

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/messages', Messages)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
