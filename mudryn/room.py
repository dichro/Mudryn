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
    self.location = location
    self.commands = dict((x, self.cmd_go) for x in self.exits)
    self.commands['look'] = self.cmd_look

  def cmd_go(self, actor, cmd, args):
    """Move to a connected room."""
    destination = self.exits[cmd]
    dest_room = get_class(destination)(destination)
    response = dest_room.receive_mobile(actor)
    notify = db.Avatar.all().filter("location =", self.get_location()).filter("tags =", "listening").fetch(100)
    if len(notify) == 100:
      # TODO(dichro): throng mode!
      pass
    else:
      if len(notify) > 0:
        actor.notify_others(actor.summary() + ' leaves ' + cmd + '.', notify)
    return 'You went ' + cmd + '. ' + response
    
  def cmd_look(self, actor, argv0, args):
    """View this room from the inside."""
    return self.description(actor)
    
  def get_location(self):
    return self.location

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
    if cmd in self.commands:
      return self.commands[cmd](actor, cmd, words[1:])

  def receive_mobile(self, actor):
    actor.location = self.get_location()
    actor.put()
    notify = db.Avatar.all()
    notify.filter("location =", self.get_location())
    notify.filter("tags =", "listening")
    results = notify.fetch(100)
    if len(results) == 100:
      # TODO(dichro): throng mode!
      # TODO(dichro): we're retrieving a superset of this data in description()
      #  immediately hereafter. There Must Be A Better Way.
      pass
    else:
      if len(results) > 0:
        actor.notify_others(actor.summary() + ' arrives.', results)
    return self.description(actor)
