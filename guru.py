import datetime
import logging
import os
import re
import wsgiref.handlers

from google.appengine.api import xmpp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.ext import webapp
from google.appengine.ext.ereporter import report_generator
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import xmpp_handlers

from mudryn.lib import get_class
from mudryn.db import Mobile, Avatar
from mudryn.room import Room

import config

class InputHandler(object):
  @staticmethod
  def handle_input(message):
    words = message.arg.split()
    if words[0] == 'create':
      # TODO(dichro): sanitize input
      xmpp.send_message([message.sender], 'Creating!')
      Avatar(identity=db.IM("xmpp", message.sender), 
             location=config.default_room, handle=words[1], 
             tags=['listening']).put()
      xmpp.send_message([message.sender], 'Done')
    else:
      InputHandler.defaultHelp(message)

  @staticmethod
  def defaultHelp(message):
    xmpp.send_message([message.sender], 'This is Mudryn. Type "create <name>" to join, eg "create zarathustra".')


class XmppHandler(xmpp_handlers.CommandHandler):
  """Handler class for all XMPP activity."""

  def text_message(self, message=None):
    sender = db.IM("xmpp", message.sender)
    q_avatar = Avatar.all();
    q_avatar.filter("identity =", sender);
    avatar = q_avatar.get();
    if avatar is None:
      InputHandler.handle_input(message)
    else:
      avatar.handle_input(message)
    

def main():
  app = webapp.WSGIApplication([
      ('/_ah/xmpp/message/chat/', XmppHandler),
      ], debug=True)
  wsgiref.handlers.CGIHandler().run(app)


if __name__ == '__main__':
  main()

