"""Database-backed objects."""

from google.appengine.api import xmpp
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from mudryn.lib import get_class

import config


class Mobile(polymodel.PolyModel):
  """An object that moves between physical locations."""

  location = db.StringProperty(required=True)

  def summary(self):
    return 'thing'


class Avatar(Mobile):
  handle = db.TextProperty(required=True)
  tags = db.StringListProperty()
  char_aliases = {
    "'": 'say',
    ':': 'emote',
  }

  def notify_others(self, message, destinations):
    dest = [avatar.key().name() for avatar in destinations
            if avatar != self]
    if len(dest) == 0:
      return
    xmpp.send_message(dest, message)

  def summary(self):
    return '@' + self.handle

  def handle_input(self, message):
    line = message.arg
    words = line.split()
    if words[0] == 'unmute':
      self.tags.append('listening')
      self.put()
      return
    if words[0] == 'mute':
      self.tags.remove('listening')
      self.put()
      xmpp.send_message([self.key().name()], 'Going catatonic. '
        'Type "unmute" to hear the world again.')
      return
    if 'listening' not in self.tags:
      xmpp.send_message([self.key().name()], 'You are muted! '
        'Type "unmute" to hear the world again.')
    try:
      line = self.char_aliases[line[0]] + ' ' + line[1:]
    except KeyError, e:
      pass
    try:
      room = get_class(self.location)(self.location)
    except:
      xmpp.send_message([self.key().name()],
                        'Failed to load your last location. Sending you back '
                        'to the start.')
      room = get_class(config.default_room)(config.default_room)
      self.location = config.default_room
      self.put()
    ret = room.handle_input(self, line)
    if ret is not None:
      xmpp.send_message([self.key().name()], ret)
    else:
      xmpp.send_message([self.key().name()], "I don't recognize that command")

  def __eq__(self, other):
    return self.key() == other.key()

  def __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
    return self.key().__hash__()



