"""Database-backed objects."""

import sys

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
  tags = db.StringListProperty()

  def notify_others(self, message, destinations):
    dest = [avatar.identity.address for avatar in destinations
            if avatar != self]
    if len(dest) == 0:
      return
    xmpp.send_message(dest, message)

  def summary(self):
    return '@' + self.handle

  commands = {
    'look': 1
  }

  def handle_input(self, message):
    words = message.arg.split()
    if words[0] == 'unmute':
      self.tags.append('listening')
      self.put()
      return
    if words[0] == 'mute':
      self.tags.remove('listening')
      self.put()
      xmpp.send_message([self.identity.address], 'Going catatonic. '
        'Type "unmute" to hear the world again.')
      return
    if 'listening' not in self.tags:
      xmpp.send_message([self.identity.address], 'You are muted! '
        'Type "unmute" to hear the world again.')
    if words[0] in self.commands:
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



