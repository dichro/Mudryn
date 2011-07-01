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
  throng_cutoff = 100

  def __init__(self, location):
    self.location = location
    self.commands = dict((x, self.cmd_go) for x in self.exits)
    self.commands['look'] = self.cmd_look
    self.commands['say'] = self.cmd_say
    # TODO(dichro): commands exist if self.cmd_<verb> exists?
    self.commands['emote'] = self.cmd_emote
    self.commands['debug'] = self.cmd_debug

  def broadcast(self, actor, message):
    """Broadcast message unless thronging."""
    notify = db.Avatar.all().filter("location =", self.get_location()).filter("tags =", "listening").fetch(self.throng_cutoff)
    if len(notify) == self.throng_cutoff:
      return False
    actor.notify_others(message, notify)
    return True
    
  def cmd_debug(self, actor, cmd, args):
    """Dump some debugging information."""
    return 'exits: ' + '; '.join('%s: %s' % (x, y) for x, y in self.exits.iteritems())

  def cmd_emote(self, actor, cmd, args):
    """Emote to the room's listeners."""
    msg = actor.summary() + ' ' + ' '.join(args)
    if not self.broadcast(actor, msg):
      return "Too many hipsters in this room."
    return 'Everyone saw: ' + msg
    
  def cmd_say(self, actor, cmd, args):
    """Speak to the listening users in this room."""
    # TODO(dichro): want the original string here instead. Change
    #   cmd api to be kwargs with everything inc kitchen sink
    if not self.broadcast(actor, actor.summary() + ' says: ' + ' '.join(args)):
      return "You can't make yourself heard over the throng."
    return 'You say: ' + ' '.join(args)

  def cmd_go(self, actor, cmd, args):
    """Move to a connected room."""
    destination = self.exits[cmd]
    dest_room = get_class(destination)(destination)
    response = dest_room.receive_mobile(actor)
    self.broadcast(actor, actor.summary() + ' leaves ' + cmd + '.')
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
        ret += ', '.join(x for x in exit_names[:-1]) + ' or '
      ret += exit_names[-1] + '.'
    return ret

  def handle_input(self, actor, command):
    words = command.split()
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
    results = notify.fetch(self.throng_cutoff)
    if len(results) == self.throng_cutoff:
      # TODO(dichro): throng mode!
      # TODO(dichro): we're retrieving a superset of this data in description()
      #  immediately hereafter. There Must Be A Better Way.
      pass
    else:
      if len(results) > 0:
        actor.notify_others(actor.summary() + ' arrives.', results)
    return self.description(actor)


def macro(package):
  """Returns a function for easily creating rooms in package."""
  def room(**kwargs):
    def maybe_prepend_package(p):
      if '.' in p:
        return p
      return '.'.join([package, p])
    class new_room(Room):
      desc = kwargs.get('desc')
      exits = dict((x, maybe_prepend_package(y)) for x, y in kwargs.get('exits').iteritems())
    return new_room
  return room


