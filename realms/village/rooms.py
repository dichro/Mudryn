from mudryn.room import Room

def room(d, e):
  class new_room(Room):
    desc = d
    exits = e
  return new_room

start = room('You are in a day care center.', {
  'out': 'square',
})
