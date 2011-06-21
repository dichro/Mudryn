from mudryn.lib import get_class

from mudryn import db

"""Rooms are the units of environment. An object is in one room
at a time, and can generally interact with other objects in the
same room."""

class Room(object):
  """A simple room."""
  aliases = {
    'n': 'north',
    's': 'south',
    'e': 'east',
    'w': 'west',
  }
  exits = {}
  desc = ''

  def __init__(self, location):
    pass

  def get_location(self):
    return '.'.join([self.__class__.__module__, self.__class__.__name__])

  def description(self, viewer):
    ret = self.desc
    contents = db.Mobile.all().filter("location =", self.get_location())
    item_names = [item.summary() for item in contents if item != viewer]
    if item_names:
      ret += ' You see: '
      if len(item_names) > 1:
        ret += ', '.join(x for x in item_names[:-1]) + ' and '
      ret += item_names[-1] + '.'
    if self.exits:
      ret += ' You can go: '
      exit_names = self.exits.keys()
      if len(exit_names) > 1:
        ret += ', '.join(x for x in exit_names[:-1]) + ' and '
      ret += exit_names[-1] + '.'
    return ret

  def handle_input(self, actor, message):
    words = message.arg.split()
    cmd = words[0]
    if cmd in self.aliases:
      cmd = self.aliases[cmd]
    if cmd in self.exits:
      destination = self.exits[cmd]
      # TODO(dichro): test dest is valid?
      actor.location = destination
      actor.put()
      return 'You go ' + cmd + '. ' + get_class(destination)(destination).description(actor)


