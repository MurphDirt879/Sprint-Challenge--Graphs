from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


stack = Stack()
visited = set()

graph = {}
#after you hit a dead end this will help you go the opposite direction
def reverse(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "w":
        return "e"
    elif direction == "e":
        return "w"

def BFS(graph, starting_room):
    queue = Queue()
    visited = set()  
    path = []
    queue.enqueue([starting_room])
    # Start your while loop
    while queue.size() > 0:
        path = queue.dequeue()
        # Grab the last vertex of the path (so you don't have to rewrite -1)
        currentRoom = path[-1]
        if currentRoom not in visited:
            visited.add(currentRoom)
            for room in graph[currentRoom]:
                if graph[currentRoom][room] == "?":
                    return path
            for exits in graph[currentRoom]:
                path.append(exits)
                next_room = graph[currentRoom][exits]
                tempPath = path.copy()
                tempPath.append(next_room)
                queue.enqueue(tempPath)


# until you reach the end of the rooms ...
while len(graph) < len(world.rooms):
    currentRoom = player.current_room
    if currentRoom not in graph:
        # Add room to graph without exits ... 
        graph[currentRoom] = {}
        for end in player.current_room.get_exits():
            # set to nil/?
            graph[currentRoom][end] = "?"
    for path in graph[currentRoom]:
        if path not in graph[currentRoom]:
            break
        if graph[currentRoom][path] == "?":
            tempPath = path
            if tempPath is not None:
                # add temp path to trav path, move player to room, set room to player.current
                traversal_path.append(tempPath)
                player.travel(tempPath)
                newRoom = player.current_room
                # same if it room isn't inn graph
                if newRoom not in graph:
                    graph[newRoom] = {}
                    for e in player.current_room.get_exits():
                        # update exits key and value 
                        graph[player.current_room][e] = "?"
            graph[currentRoom][tempPath] = newRoom
            graph[newRoom][reverse(tempPath)] = currentRoom
            currentRoom = newRoom
    # No exits left
    paths = BFS(graph, currentRoom)
    if paths != None:
        for roomID in paths:
            for room in graph[currentRoom]:
                if graph[currentRoom][room] == roomID:
                    traversal_path.append(room)
                    player.travel(room)
    currentRoom = player.current_room







# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
