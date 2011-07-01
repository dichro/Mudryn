from mudryn.room import macro

room = macro(__name__)

foo = room(
    desc='This is a test room.',
    exits={
      'north': 'bar',
    },
)

bar = room(
    desc='This is also a test room.',
    exits={
      'south': 'foo',
    },
)
