from mudryn.room import Room

def macro(package):
  def room(**kwargs):
    def maybe_prepend_package(p):
      if '.' in p:
        return p
      return '.'.join([__name__, p])
    class new_room(Room):
      desc = kwargs.get('desc')
      exits = dict((x, maybe_prepend_package(y)) for x, y in kwargs.get('exits').iteritems())
    return new_room
  return room

room = macro(__name__)

foo = room(desc='This is a test room.', exits={
  'north': 'bar',
})

bar = room(desc='This is also a test room.', exits={
  'south': 'foo',
})
