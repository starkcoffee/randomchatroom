import cgi
import os
import re
import datetime
from django.utils import simplejson

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Message(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  Alias = db.StringProperty()


class MessageView:
  def __init__(self, message):
    self.message = message
    if message.Alias:
      self.author = message.Alias
    else:
      self.author = "A monkey"

    now = datetime.datetime.now()
    timedelta = now - message.date
    self.ago_minutes = timedelta.seconds / 60
    self.content = message.content


class MainPage(webapp.RequestHandler):
  def get(self):
    messages_query = Message.all().order('-date')
    messages = messages_query.fetch(50)

    #if users.get_current_user():
    #  url = users.create_logout_url(self.request.uri)
    #  url_linktext = 'Logout'
    #else:
    #  url = users.create_login_url(self.request.uri)
    #  url_linktext = 'Login if you want'

    message_views = []
    for message in messages:
       message_views.append(MessageView(message))

    template_values = {
      'messages': message_views,
    #  'url': url,
    #  'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))
    
def Filter(string):
    file = open("filter","r")
    rudish_words = file.readlines()
    file.close()
    for word in rudish_words:
        pattern = re.compile(word,re.IGNORECASE | re.VERBOSE)
        string = re.sub(pattern,'Banana',string)
    return string

class Messages(webapp.RequestHandler):
  def post(self):
    message = Message()


    message.Alias = Filter(self.request.get('Alias'))

    content = Filter(self.request.get('content'))

    message.content = content
    message.put()
    self.redirect('/')

  def get(self):
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
  

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/messages', Messages)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
