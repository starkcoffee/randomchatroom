import cgi
import os
import re
import datetime
import logging
import Cookie
import filter

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
  room = db.StringProperty()


class MessageView:
  def __init__(self, message, name):
    self.message = message
    if message.alias:
        self.author = message.alias
    else:
        self.author = "A monkey"

    now = datetime.datetime.now()
    timedelta = now - message.date
    self.ago_minutes = timedelta.seconds / 60
    if name == None: name = ""
    self.content = filter.twitter(message.content,name)

class MainPage(webapp.RequestHandler):
  def get(self):
    alias = self.request.cookies.get('alias')
    if not alias: alias = ""
    
    room = self.request.path
    logging.info("****** room is " + room)
	
    template_values = {'alias' : alias, 'room' : room}
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))


class Messages(webapp.RequestHandler):
  def post(self):
    message = Message()
    
    room = self.request.get('room').upper()
    message.room = room.upper()
    
    alias = self.request.get('alias')
    if alias:
      alias = alias.lstrip('"')
      alias = alias.rstrip('"')
      cookie = Cookie.SimpleCookie()
      cookie['alias'] = alias
      print cookie 
    elif self.request.cookies.get('alias'):
      alias = self.request.cookies.get('alias')
      alias = alias.lstrip('"')
      alias = alias.rstrip('"')
      
    content = self.request.get('content')

    message.alias = filter.all(alias)
    message.content = filter.all(self.request.get('content'),alias)
    if message.content:
      message.put()

      memcache.set("last_message_posted_at_"+room, datetime.datetime.utcnow())  
    
    self.redirect(room)

  def get(self):
    
    room = self.request.path.split("/messages")[1]
		
    lastModifiedTime = memcache.get("last_message_posted_at_"+room) 

    # would be nice to initialize lastModifiedTime in memcache on app startup somehow so we dont need the None check
    if lastModifiedTime is None:
        lastModifiedTime = datetime.datetime.utcnow()
        memcache.set("last_message_posted_at", datetime.datetime.utcnow())    

    if self.request.headers.get('If-Modified-Since') == lastModifiedTime.strftime('%a, %d %b %Y %H:%M:%S GMT'): 
        return self.response.set_status(304) 
    
    #messages_query = Message.all().order('-date')
    messages_query = db.GqlQuery("SELECT * FROM Message WHERE room = :1 ORDER BY date DESC",room)
    messages = messages_query.fetch(50)

    message_views = []
    alias = self.request.cookies.get('alias')
    for message in messages:
       message_views.append(MessageView(message,alias)) #Adapting for Twitter style.

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
                                      ('/messages.*', Messages),
                                      ('/.*', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
