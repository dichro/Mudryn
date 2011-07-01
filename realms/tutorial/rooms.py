from mudryn.room import macro

room = macro(__name__)

start = room(
    desc = 'Welcome to Mudryn! You are in an empty room. You should try typing '
           '"north" to leave.',
    exits = {
        'north': 'next',
    },
)

next = room(
    desc = "Well done! You're in... another unremarkable room now. Each room "
           "lists the directions you can go from it. Just type the direction "
           "to leave, like you did before.",
    exits = {
        'south': 'start',
        'east': 'mazeintro',
    },
)

mazeintro = room(
    desc = 'This room is the entrance to a (tiny) maze. Find your way to the '
           'other side.',
    exits = {
        'west': 'next',
        'north': 'upstart',
        'east': 'downstart',
    }
)

upstart = room(
    desc = 'You are in a maze of twisty little passages, all alike.',
    exits = {
        'south': 'mazeintro',
        'east': 'mazestep',
    }
)

downstart = room(
    desc = 'You are in a maze of twisty little cabbages, all alike.',
    exits = {
        'west': 'mazeintro',
        'north': 'mazestep',
    }
)

mazestep = room(
    desc = 'Still in the maze. You can abbreviate compass directions to just '
           'their first letter. Try using "n" instead of "north".',
    exits = {
        'south': 'downstart',
        'west': 'upstart',
        'north': 'passage',
    }
)

passage = room(
    desc = 'This is a narrow stone corridor, cold and dank.',
    exits = {
        'south': 'mazestep',
    }
)
