"""Database-backed objects."""

from google.appengine.api import xmpp

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from mudryn.lib import get_class


class Mobile(polymodel.PolyModel):
  """An object that moves between physical locations."""

  location = db.StringProperty(required=True)

  def summary(self):
    return 'thing'


class Avatar(Mobile):
  identity = db.IMProperty(required=True)
  handle = db.TextProperty(required=True)

  def summary(self):
    return '@' + self.handle

  commands = {
    'look': 1
  }

  def handle_input(self, message):
    words = message.arg.split()
    if words[0] in self.commands:
      xmpp.send_message([self.identity.address], 'I recognize that command')
      # look
      room = get_class(self.location)(self.location)
      xmpp.send_message([self.identity.address], room.description(self))
    else:
      room = get_class(self.location)(self.location)
      ret = room.handle_input(self, message)
      if ret is not None:
        xmpp.send_message([self.identity.address], ret)
      else:
        xmpp.send_message([self.identity.address], "I don't recognize that command")

  def __eq__(self, other):
    return hasattr(other, 'identity') and other.identity == self.identity

  def __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
    return self.identity.__hash__()



