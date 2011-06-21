import datetime
import logging
import os
import re
import wsgiref.handlers
import sys

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


class Start(Room):
  desc = 'Start room description.'
  exits = {
    'north': '__main__.Next',
    'south': '__main__.test2',
    'east': 'realms.village.rooms.start',
  }


class Next(Start):
  desc = 'Next room description'
  exits = {
    'south': '__main__.Start',
    'north': '__main__.test',
  }


def roomx(name, d, e):
  class new_room(Room):
    desc = d
    exits = e
  return new_room


test = roomx('test', 'Test room description',
  { 'south': '__main__.Next',
    'north': '__main__.test2', })

test2 = roomx('test', 'Test2 room description',
  { 'south': '__main__.test',
    'north': '__main__.Start' })


class InputHandler(object):
  @staticmethod
  def handle_input(message):
    words = message.arg.split()
    if words[0] == 'create':
      # TODO(dichro): sanitize input
      xmpp.send_message([message.sender], 'Creating!')
      Avatar(identity=db.IM("xmpp", message.sender), location='__main__.Start', handle=words[1]).put()
      xmpp.send_message([message.sender], 'Done')
    else:
      InputHandler.defaultHelp(message)

  @staticmethod
  def defaultHelp(message):
    xmpp.send_message([message.sender], 'This is Mudryn. Type "create" to join.')


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

