from mudryn import room

import time

class Room(room.Room):
  desc = 'The road runs past a small pond. There is a toad with swirling eyes here.'
  exits = {
    'east': 'realms.village.rooms.graveroad1',
  }
  __blocked = {}
  
  def __init__(self, *args):
    super(Room, self).__init__(*args)

  def toad_reply(self):
    return 'ALL GLORY TO THE HYPNOTOAD'

  def cmd_look(self, actor, argv0, args):
    if 'toad' in args:
      self.__blocked[actor.identity.address] = time.time() + 20
      return self.toad_reply()
    return super(Room, self).cmd_look(actor, argv0, args)

  def handle_input(self, actor, message):
    """Block user input for a while if the user has looked at the toad."""
    try:
      expiry = self.__blocked[actor.identity.address]
      if expiry > time.time():
        return self.toad_reply()
      del self.__blocked[actor.identity]
    except KeyError, e:
      pass
    return super(Room, self).handle_input(actor, message)

