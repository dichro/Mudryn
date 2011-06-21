from mudryn.room import Room

def room(d, e):
  def maybe_prepend_package(p):
    if '.' in p:
      return p
    return '.'.join([__name__, p])
  class new_room(Room):
    desc = d
    exits = dict((x, maybe_prepend_package(y)) for x, y in e.iteritems())
  return new_room

start = room('You are in a day care center.', {
  'out': 'square',
})

square = room('You are in a square. East is the day care center; '
  'west the town hall.', {
  'east': 'start',
  'west': 'townhall',
  'north': 'northroad1',
})

northroad1 = room('You are on a road climbing a gentle slope to '
  'the north.', {
  'north': 'northroad2',
  'south': 'square',
})

northroad2 = room('You are on a road climbing a gentle slope to '
  'the north. A large building sits atop the hill. An overgrown '
  'track diverges towards the west.', {
  'north': 'northroad3',
  'south': 'northroad1',
  'west': 'graveroad1',
})

northroad3 = room('You stand just below a castle to the north.', {
  'north': 'castlegate',
  'south': 'northroad2',
})

castlegate = room('You are at the gates to a castle.', {
  'south': 'northroad3',
})

graveroad1 = room('This narrow and somewhat unkempt road leads west.', {
  'east': 'northroad2',
})

townhall = room('You are in a town hall.', {
  'out': 'square',
})
