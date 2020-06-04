# Cochintele Andreea
# Grupa 231
# Proiect 1 / Laboratorul 6
# PB_4-- Problema de cautare(un mesaj)

import math


class Node:
    def __init__(self, parent=None, position=None, name=None):
        self.parent = parent
        self.position = position
        self.name = name

        self.g = 0
        self.h = 0
        self.h1 = 0
        self.f = 0
        self.f1 = 0

    def __eq__(self, other):
        return self.position == other.position


def find_position(classroom, name):
    # search for start and end in classroom matrix
    nr1 = 0
    for i in classroom:
        nr2 = 0
        for j in i:
            poz = (nr1, nr2)
            if j == name:
                return poz
            nr2 = nr2 + 1
        nr1 = nr1 + 1
    return -1


def ok(sad, cnode, wnode):
    # search if cnode can comunicate with wnode
    n1 = (cnode, wnode)
    n2 = (wnode, cnode)
    for i in sad:
        if i == n1 or i == n2:
            return 0
    return 1


def scop(current_node):
    # the message arrived
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    return path  # Return reversed path


def generare(current_node, classroom, sad):
    children = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

        # Get node position
        node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        # Make sure within range
        if node_position[0] > (len(classroom) - 1) or node_position[0] < 0:
            continue
        if node_position[1] > (len(classroom[len(classroom) - 1]) - 1) or node_position[1] < 0:
            continue
        # Make sure we can cross between rounds
        if node_position[1] == 2:
            if node_position[0] < len(classroom) - 2 and current_node.position[0] < len(classroom) - 2:
                if current_node.position[1] == 1:
                    continue
        if node_position[1] == 4:
            if node_position[0] < len(classroom) - 2 and current_node.position[0] < len(classroom) - 2:
                if current_node.position[1] == 3:
                    continue
        if node_position[1] == 1:
            if node_position[0] < len(classroom) - 2 and current_node.position[0] < len(classroom) - 2:
                if current_node.position[1] == 2:
                    continue
        if node_position[1] == 3:
            if node_position[0] < len(classroom) - 2 and current_node.position[0] < len(classroom) - 2:
                if current_node.position[1] == 4:
                    continue

        node_name = classroom[node_position[0]][node_position[1]]
        # Skip empty seat
        if node_name == 'liber':
            continue

        if ok(sad, current_node.name, node_name) == 0:
            continue

        # Create new node
        new_node = Node(current_node, node_position, node_name)

        # Append
        children.append(new_node)
    return children


def astar(classroom, sad, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given classroom"""

    # Create start and end node
    start_node = Node(None, find_position(classroom, start), start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, find_position(classroom, end), end)
    end_node.g = end_node.h = end_node.f = 0

    # Check if there is start and end in the classroom
    if start_node.position == -1 or end_node.position == -1:
        return 0
    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node.name == end_node.name:
            return scop(current_node)

        # Generate children
        children = generare(current_node, classroom, sad)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # Euclidian distance
            child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2))
            child.f = child.g + child.h
            # Manhattan distance
            child.h1 = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f1 = child.g + child.h1

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def print_sol(classroom, path):
    # Print the path from start to end
    g = open('output_1.txt', 'w')
    xi = path[0][0]
    xj = path[0][1]
    g.write(classroom[xi][xj])
    for k in path:
        if k == path[0]:
            continue
        i = k[0]
        j = k[1]
        if (xj == 1 and j == 2) or (xj == 3 and j == 4):
            if xi >= len(classroom) - 2:
                g.write(' >> ')
        elif (xj == 2 and j == 1) or (xj == 4 and j == 3):
            if xi >= len(classroom) - 2:
                g.write(' << ')
        elif xi == i and xj + 1 == j:
            g.write(" > ")
        elif xi == i and xj - 1 == j:
            g.write(" < ")
        elif xi + 1 == i and xj == j:
            g.write(" v ")
        elif xi - 1 == i and xj == j:
            g.write(" ^ ")
        g.write(classroom[i][j])
        xi = i
        xj = j


def main():
    f = open('input_1.txt', 'r')
    # Reading from the input file
    number = int(f.readline())
    data = f.readlines()
    sad = []
    classroom = []
    nr = 0
    tr = 0
    date = "-"
    for line in data:
        if nr < number and tr == 0:
            words = line.split()
            classroom.append(words)
            nr = nr + 1
        elif nr == number and tr == 0:
            number = int(line)
            tr = 1
            nr = 0
        elif nr < number and tr == 1:
            words = line.split()
            sad.append(words)
            nr = nr + 1
        elif nr == number and tr == 1:
            date = line.split()
            tr = 2
    # nr = 7
    # classroom = [["ionel", "alina", "teo", "eliza", "carmen", "monica"],
    #       ["george", "diana", "bob", "liber", "nadia", "mihai"],
    #       ["liber", "costin", "anda", "bogdan", "dora", "marin"],
    #       ["luiza", "simona", "dana", "cristian", "tamara", "dragos"],
    #       ["mihnea", "razvan", "radu", "patricia", "gigel", "elena"],
    #       ["liber", "andrei", "oana", "victor", "liber", "dorel"],
    #       ["viorel", "alex", "ela", "nicoleta", "maria", "gabi"]]
    # nr = 7
    # sad = [("george", "ionel"),
    #      ("ela", "nicoleta"),
    #      ("victor", "oana"),
    #      ("teo", "eliza"),
    #      ("teo", "luiza"),
    #      ("elena", "dragos"),
    #      ("alina", "dragos")]
    # start = "ionel"
    # end = "dragos"

    path = astar(classroom, sad, date[0], date[1])
    if path != 0:
        print_sol(classroom, path)
    else:
        g = open("output_1.txt", "w")
        g.write("Nu exista solutii.")


if __name__ == "__main__":
    main()
