import math
import random
import time
import route_generator
import tsp
import adjacent_matrix

rows = 40
columns = 21
item_num = 5
items = {}

item_ids = {}
worker = ()
carts_list = []
nodes = [[0 for i in range(columns)] for i in range(rows)]


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


def loadItems():
    print('Please input the item ids you are purchasing: ')
    print('input -1 to stop: ')
    global carts_list
    while True:
        id = eval(input())
        if id == -1:
            break
        print(items[id])

        pickupLoc = getMappedLoc(items[id])
        if pickupLoc not in item_ids:
            item_ids[pickupLoc] = [id]
        else:
            item_ids[pickupLoc].append(id)
        carts_list.append(pickupLoc)

    new_list = list(set(carts_list))
    carts_list = []
    carts_list += new_list


def getItems():
    printMap()
    # Choose algorithm
    print('Please choose the algorithm: ')
    print('1 - Items Order')
    print('2 - Brute Force')
    calculateRunningTime(len(carts_list))
    choice = eval(input())
    # The first choice of the algorithm
    route = []
    dis = 0
    # The duration of the running time of the algorithm
    duration = 0.0
    print(carts_list)
    if choice == 1:
        t = time.perf_counter()
        shortest_route, shortest_dis = tsp.tsp_order(worker, nodes, carts_list)
        duration = time.perf_counter() - t
        route += shortest_route
        dis += shortest_dis
    elif choice == 2:
        # Output the route information
        t = time.perf_counter()
        shortest_route, shortest_dis = tsp.tsp_permutation(worker, nodes, carts_list)
        duration = time.perf_counter() - t
        route += shortest_route
        dis += shortest_dis

    route.insert(0, worker)
    route.append(worker)
    print(route)
    for i in range(len(route) - 1):
        dis, path = route_generator.dijkstra(nodes, route[i], route[i + 1])
        route_generator.print_path(path)
        if i != len(route) - 2:
            print('Please pick up the items of id', item_ids[route[i + 1]])
    print(f'Duration: {duration:.8f}s')
    with open('running_time_history.txt', 'a') as file:
        # file.write(choice + ',' + len(carts_list) + ',' + duration + '\n')
        file.write(f'{choice},{len(carts_list)},{duration}\n')



def calculateRunningTime(itemNum):
    f = open('running_time_history.txt', 'r')
    logs = f.readlines()
    coCount = 0
    coTime = 0
    bfCount = 0
    bfTime = 0
    for log in logs:
        log_str = log.split(',')
        if log_str[0] == '1' and log_str[1] == str(itemNum):
            coCount += 1
            coTime += float(log_str[2])
        if log_str[0] == '2' and log_str[1] == str(itemNum):
            bfCount += 1
            bfTime += float(log_str[2])
    if bfCount == 0 or coCount == 0:
        return

    print(f'Duration time estimation: \nIn this loop of {itemNum} locations to drop by, estimated running time will be \n{(coTime/coCount)}s using Carts Order algorithm, \n{bfTime/bfCount}s using Brute Froce Algorithm.')

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
    print("1 - Input customer location manually")
    print("2 - Re-input items")

    num = eval(input())
    global worker
    global carts_list
    global rows
    global columns
    global nodes
    global item_num
    if num == 1:
        nodes[worker[0]][worker[1]] = 0
        print("Input the location of customer as x,y. For example 0,0")
        content = input()
        arr = content.split(",")
        x, y = eval(arr[0]), eval(arr[1])
        if nodes[x][y] == 2:
            print("You cannot locate on shelves.")
            return
        nodes[x][y] = 1
        worker = (x, y)
        print("Customer location changed.")
    elif num == 2:
        carts_list = []
        loadItems()
    else:
        print("Invalid input! Please input again. ")


def loadFromFile():
    global worker
    worker = (0, 0)
    global nodes
    nodes[0][0] = 1
    f = open('data.txt', 'r')
    text = f.readlines()

    node_x = []
    node_y = []

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

    nodes = [[0 for i in range(columns)] for i in range(rows)]
    for i in range(len(node_x)):
        # print(node_x[i], node_y[i])
        nodes[node_x[i]][node_y[i]] = 2


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
    generateRandomData()
    loadFromFile()
    loadItems()
    matrix = adjacent_matrix.adjacency_matrix(nodes)

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


def generateRandomData():
    global worker
    worker = (0, 0)
    nodes[0][0] = 1
    cnt = 0
    while cnt < item_num:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if x == 0 and y == 0:
            continue
        if nodes[x][y] != 0:
            continue
        nodes[x][y] = 2
        cnt += 1


if __name__ == '__main__':
    main()
