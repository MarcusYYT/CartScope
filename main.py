import math
import random
import time
import route_generator
import tsp
import running_time_history_logger
import copy
from memory_profiler import memory_usage
import tracemalloc


# Row and column of the map
rows = 40
columns = 21

# List of items loaded from file
itemlists = []
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
# 2-d list to store the temp navigation map. 0 for none, 1 for worker, 2 for shelves, 3 for direction routes
directed_map = [[0 for i in range(columns)] for i in range(rows)]

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

# add directions on a Map
def addDirections(path):
    global directed_map
    # Display of location information
    for i in range(len(path)-1):
        if path[i][0] == path[i+1][0]:
            if path[i][1] < path[i+1][1]:
                for j in range(path[i+1][1]-path[i][1]+1):
                     directed_map[path[i][0]][path[i][1]+j] = 3
            else:
                for j in range(path[i][1]-path[i+1][1]+1):
                     directed_map[path[i+1][0]][path[i+1][1]+j] = 4
        else:
            if path[i][0] < path[i+1][0]:
                for j in range(path[i+1][0]-path[i][0]+1):
                    directed_map[path[i][0]+j][path[i][1]] = 6
            else:
                for j in range(path[i][0]-path[i+1][0]+1):
                    directed_map[path[i+1][0]+j][path[i+1][1]] = 5

# Print direction map
def printDirections():
    global directed_map
    for i in range(columns):
        row_str = '{0:<3s}'.format(str(columns - 1 - i))
        for j in range(rows):
            row_str = row_str + '{0:<3s}'.format(toSymbol(directed_map[j][columns - 1 - i]))
        print(row_str)
    col_str = "{0:3s}".format('')
    for i in range(rows):
        col_str = col_str + "{0:<3s}".format(str(i))
    print(col_str)

# Direction map initialization
def init_directions():
    global directed_map
    directed_map = copy.deepcopy(nodes)

# Get Items from user input
def mamuallyInputItems():
    print('Please input the item ids you are purchasing: ')
    print('input -1 to stop: ')
    global pickuploc_list
    while True:
        try:
            id = eval(input())
            if id == -1:
                break
            print(items[id])
            # Merge items at same shelves
            pickupLoc = items[id]
            if pickupLoc not in item_ids:
                item_ids[pickupLoc] = [id]
            else:
                item_ids[pickupLoc].append(id)
            pickuploc_list.append(pickupLoc)
        except SyntaxError:
            print("Invalid input! Please input again. ")
        except KeyError:
            print("No such item. Input again.")

    new_list = list(set(pickuploc_list))
    pickuploc_list = []
    pickuploc_list += new_list


def loadListFromFile():
    global itemlists

    f = open('qvBox-warehouse-orders-list-part01.txt', 'r')
    lines = f.readlines()
    for line in lines:
        itemids = line.strip().split(", ")
        itemlists.append(list(map(int, itemids)))
    # print(itemlist)

def selectOneListFromLoadedData():
    global pickuploc_list
    print("Now please select one list from the item lists we loaded from file.")
    print("Here are the lists:")
    for i in range(len(itemlists)):
        print(f"{i}. {itemlists[i]}")
    try:
        choice = eval(input("Please select by input the index:"))
        itemids = itemlists[choice]
        for j in range(len(itemids)):
            pickupLoc = items[itemids[j]]
            if pickupLoc not in item_ids:
                item_ids[pickupLoc] = [id]
            else:
                item_ids[pickupLoc].append(id)
            pickuploc_list.append(pickupLoc)
    except SyntaxError:
        print("Invalid input! Please input again. ")

# Function 1. Get Items
def getItems():
    printMap()
    # Choose algorithm
    print('Please choose the algorithm: ')
    # print('1 - Items Order')
    # print('2 - Brute Force')
    print('1 - Branch and Bound')
    print('2 - Greedy')
    running_time_history_logger.calculateRunningTime(len(pickuploc_list))
    try:
        choice = eval(input())
        # The first choice of the algorithm
        route = []
        dis = 0
        # The duration of the running time of the algorithm
        duration = 0.0
        # print(pickuploc_list)
        if choice == 1:
            tracemalloc.start()
            t = time.perf_counter()
            shortest_route, shortest_dis = tsp.multi_branch_tsp(worker, nodes, pickuploc_list)
            duration = time.perf_counter() - t
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            route += shortest_route
            dis += shortest_dis
        elif choice == 2:
            tracemalloc.start()
            t = time.perf_counter()
            shortest_route, shortest_dis = tsp.greedy_tsp(worker, nodes, pickuploc_list)
            duration = time.perf_counter() - t
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            route += shortest_route
            dis += shortest_dis
        print(f"Route order generated by the algorithm: {shortest_route}, Cost: {shortest_dis}")
        input("Press Enter to start your route navigation step by step")
        print()
        route.insert(0, worker)
        route.append(worker)
        init_directions()
        for i in range(len(route) - 1):
            dis, path = route_generator.dijkstra(nodes, route[i], route[i + 1])
            route_generator.print_path(path)
            addDirections(path)
            if i != len(route) - 2:
                # print('Please pick up the items of id', item_ids[route[i + 1]])
                printDirections()
                input('Please press enter to go to next item')
                print()
                init_directions()
                continue
            printDirections()
            init_directions()
        print(f'Running Time Consumpption: {duration:.8f}s')
        print(f"Peak memory usage was {peak / 10 ** 6}MB")
        running_time_history_logger.log(choice, len(pickuploc_list), duration)
    except SyntaxError:
        print("Invalid input! Please input again. ")



# Convert the number expression to String  1 - user; 2 - shelf
def toSymbol(num):
    if num == 0:
        return '.'
    elif num == 1:
        return 'P'
    elif num == 2:
        return 'S'
    elif num == 3:
        return '^'
    elif num == 4:
        return 'v'
    elif num == 5:
        return '<'
    elif num == 6:
        return '>'

# The function to handle all setting operations
def open_settings():
    print("The location of customer is at [0, 0] as default")
    print("Please input the corresponding number to choose the next step.")
    print("1 - Input worker location manually")
    print("2 - Re-input items")
    try:
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
            mamuallyInputItems()
        else:
            print("Invalid input! ")
    except SyntaxError:
        print("Invalid input! ")
        print()


# Load data file into list
def loadDataFromFile():
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
    loadDataFromFile()
    loadListFromFile()
    selectOneListFromLoadedData()

    print("Welcome to Ants Carts Moving, please input the corresponding number to choose the next step.")
    print("1 - Get Items")
    print("2 - Settings")
    print("3 - Print Map")
    print("4 - Exit")
    # Get the input from user, perform the following steps according to the input
    while True:
        try:
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
                continue
        except SyntaxError:
            print("Invalid input! Please input again. ")
            continue
        print("Welcome to Ants Carts Moving, please input the corresponding number to choose the next step.")
        print("1 - Get Items")
        print("2 - Settings")
        print("3 - Print Map")
        print("4 - Exit")

    print("Program exited")


def write_array_to_file(array, file_name):
    with open(file_name, 'w') as file:
        for row in array:
            file.write(' '.join(str(x) for x in row) + '\n')

if __name__ == '__main__':
    main()
