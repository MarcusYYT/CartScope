import math
import random
import time
import route_generator
import tsp
import running_time_history_logger

# Row and column of the map
rows = 40
columns = 21

# Dictionary to lookup all the item locations on shelves by id, in format { id, (x, y) }. x, y are integers
items = {}
# Dictionary to lookup ids by item pickup locations, in format { (x, y), id }
item_ids = {}
# Position of worker (x, y)
worker = ()
# List to store pickup locations
pickuploc_list = []
# 2-d list to store the map of warehouse. 0 for none, 1 for worker, 2 for shelves
nodes = [[0 for i in range(columns)] for i in range(rows)]

# Print map function
def printMap():
    # Basic information
    print('Legend: ')
    print('P - You')
    print('_ - No items')
    print('S - Shelf')
    print('Coordinates are (Row, Col)')
    print()
    # Display of location information

    for i in range(columns):
        row_str = '{0:<3s}'.format(str(columns - 1 - i))
        for j in range(rows):
            row_str = row_str + '{0:<3s}'.format(toSymbol(nodes[j][columns - 1 - i]))
        print(row_str)
    col_str = "{0:3s}".format('')
    for i in range(rows):
        col_str = col_str + "{0:<3s}".format(str(i))
    print(col_str)

# Get Items from user input
def inputItems():
    print('Please input the item ids you are purchasing: ')
    print('input -1 to stop: ')
    global pickuploc_list
    while True:
        id = eval(input())
        if id == -1:
            break
        print(items[id])
        # Merge items at same shelves
        pickupLoc = getMappedLoc(items[id])
        if pickupLoc not in item_ids:
            item_ids[pickupLoc] = [id]
        else:
            item_ids[pickupLoc].append(id)
        pickuploc_list.append(pickupLoc)

    new_list = list(set(pickuploc_list))
    pickuploc_list = []
    pickuploc_list += new_list

# Function 1. Get Items
def getItems():
    printMap()
    # Choose algorithm
    print('Please choose the algorithm: ')
    print('1 - Items Order')
    print('2 - Brute Force')
    running_time_history_logger.calculateRunningTime(len(pickuploc_list))
    choice = eval(input())
    # The first choice of the algorithm
    route = []
    dis = 0
    # The duration of the running time of the algorithm
    duration = 0.0
    print(pickuploc_list)
    if choice == 1:
        # Start logging the duration of the running time of the algorithm
        t = time.perf_counter()
        shortest_route, shortest_dis = tsp.tsp_order(worker, nodes, pickuploc_list)
        # End logging the duration of the running time of the algorithm
        duration = time.perf_counter() - t
        route += shortest_route
        dis += shortest_dis
    elif choice == 2:
        # Start logging the duration of the running time of the algorithm
        t = time.perf_counter()
        shortest_route, shortest_dis = tsp.tsp_permutation(worker, nodes, pickuploc_list)
        # End logging the duration of the running time of the algorithm
        duration = time.perf_counter() - t
        route += shortest_route
        dis += shortest_dis

    route.insert(0, worker)
    route.append(worker)
    for i in range(len(route) - 1):
        dis, path = route_generator.dijkstra(nodes, route[i], route[i + 1])
        route_generator.print_path(path)
        if i != len(route) - 2:
            print('Please pick up the items of id', item_ids[route[i + 1]])
    print(f'Duration: {duration:.8f}s')
    running_time_history_logger.log(choice, len(pickuploc_list), duration)




# Convert the number expression to String  1 - user; 2 - shelf
def toSymbol(num):
    if num == 0:
        return '_'
    elif num == 1:
        return 'P'
    elif num == 2:
        return 'S'


# The function to handle all setting operations
def open_settings():
    print("The location of customer is at [0, 0] as default")
    print("Please input the corresponding number to choose the next step.")
    print("1 - Input worker location manually")
    print("2 - Re-input items")

    num = eval(input())
    global worker
    global pickuploc_list
    global rows
    global columns
    global nodes

    if num == 1:
        nodes[worker[0]][worker[1]] = 0
        print("Input the location of worker as x,y. For example 0,0")
        content = input()
        arr = content.split(",")
        x, y = eval(arr[0]), eval(arr[1])
        # Prevent locations of shelves
        if nodes[x][y] == 2:
            print("You cannot locate on shelves.")
            return
        nodes[x][y] = 1
        worker = (x, y)
        print("Worker location changed.")
    elif num == 2:
        pickuploc_list = []
        inputItems()
    else:
        print("Invalid input! Please input again. ")


# Load data file into list
def loadFromFile():
    global worker

    global nodes

    f = open('data.txt', 'r')
    text = f.readlines()

    node_x = []
    node_y = []
    nodes = [[0 for i in range(columns)] for i in range(rows)]

    global items
    for i in range(len(text) - 1):
        line = text[i + 1]
        strs = line.split()
        x = eval(strs[1])
        y = eval(strs[2])
        items[eval(strs[0])] = (x, y)
        # print(items[eval(strs[0])])
        node_x.append(math.floor(x))
        node_y.append(math.floor(y))

    for i in range(len(node_x)):
        # print(node_x[i], node_y[i])
        nodes[node_x[i]][node_y[i]] = 2

    # Initialize worker position to (0,0)
    worker = (0, 0)
    nodes[0][0] = 1

# Map the item location to a accessible lane position
def getMappedLoc(location):
    x = math.floor(location[0])
    y = math.floor(location[1])
    if x == 0:
        return (1, y)
    if y == 0:
        return (x, 1)
    if x == rows:
        return (x - 1, y)
    if y == columns:
        return (x, y - 1)
    return (x, y - 1)


def main():
    # Generate random data before running
    # generateRandomData()
    loadFromFile()
    inputItems()

    while True:
        print("Welcome to Ants Carts Moving, please input the corresponding number to choose the next step.")
        print("1 - Get Items")
        print("2 - Settings")
        print("3 - Print Map")
        print("4 - Exit")
        # Get the input from user, perform the following steps according to the input
        num = eval(input())
        if num == 1:
            getItems()
        elif num == 2:
            open_settings()
        elif num == 3:
            printMap()
        elif num == 4:
            break
        else:
            print("Invalid input! Please input again. ")
    print("Program exited")


def write_array_to_file(array, file_name):
    with open(file_name, 'w') as file:
        for row in array:
            file.write(' '.join(str(x) for x in row) + '\n')

if __name__ == '__main__':
    main()
