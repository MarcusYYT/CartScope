import math
import random
import time
import route_generator
import tsp

rows = 40
columns = 21
cart_num = 5
items = {}

worker = ()
carts = []
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
    while True:
        id = eval(input())
        if id == -1:
            break
        print(items[id])
        pickupLoc = getMappedLoc(items[id])
        carts.append(pickupLoc)

def getCarts():
    printMap()
    # Choose algorithm
    print('Please choose the algorithm: ')
    print('1 - Items Order')
    print('2 - Brute Force')
    choice = eval(input())
    # The first choice of the algorithm
    route = []
    dis = 0
    # The duration of the running time of the algorithm
    duration = 0.0
    print(carts)
    if choice == 1:
        t = time.perf_counter()
        shortest_route, shortest_dis = tsp.tsp_order(worker, nodes, carts)
        duration = time.perf_counter() - t
        route += shortest_route
        dis += shortest_dis
    elif choice == 2:
        # Output the route information
        t = time.perf_counter()
        shortest_route, shortest_dis = tsp.tsp_permutation(worker, nodes, carts)
        duration = time.perf_counter() - t
        route += shortest_route
        dis += shortest_dis

    route.insert(0, worker)
    route.append(worker)
    for i in range(len(route)-1):
        dis, path = route_generator.dijkstra(nodes, route[i], route[i + 1])
        route_generator.print_path(path)
        print('Please pick up the item at', route[i+1])
    print(f'Duration: {duration:.8f}s')


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
    # print("The location of carts are generated randomly")
    # print("The default map size is 5 by 5")
    print("Please input the corresponding number to choose the next step.")
    print("1 - Input customer location manually")
    print("2 - Re-input items")
    # print("2 - Input cart location manually")
    # print("3 - Change map size")
    # print('4 - Set the maximum carts number')
    num = eval(input())
    global worker
    global carts
    global rows
    global columns
    global nodes
    global cart_num
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
        carts = []
        loadItems()
    # elif num == 2:
    #     print("The current number of carts in this system is ", cart_num)
    #     print("Input the location of", cart_num,  "carts as x,y. For example 1,2")
    #     for cart in carts:
    #         nodes[cart[0]][cart[1]] = 0
    #     carts = []
    #     for i in range(cart_num):
    #         content = input()
    #         arr = content.split(",")
    #         x, y = eval(arr[0]), eval(arr[1])
    #         nodes[x][y] = 2
    #         carts.append((x, y))
    # elif num == 3:
    #     print('The current map size is', rows, 'by', columns)
    #     print('Input the new size number')
    #     rows = eval(input())
    #     columns = eval(input())
    #     carts = []
    #     nodes = [[0 for i in range(rows)] for i in range(columns)]
    #     # Refresh the data
    #     generateRandomData()
    # elif num == 4:
    #     print('Input new maximum cart number')
    #     cart_num = eval(input())
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
        return (x-1, y)
    if y == columns:
        return (x, y-1)
    return (x, y-1)

def main():
    # Generate random data before running
    generateRandomData()
    loadFromFile()
    loadItems()

    while True:
        print("Welcome to Ants Carts Moving, please input the corresponding number to choose the next step.")
        print("1 - Get Items")
        print("2 - Settings")
        print("3 - Print Map")
        print("4 - Exit")
        # Get the input from user, perform the following steps according to the input
        num = eval(input())
        if num == 1:
            getCarts()
        elif num == 2:
            open_settings()
        elif num == 3:
            printMap()
        elif num == 4:
            break
        else:
            print("Invalid input! Please input again. ")
    print("Program exited")


def generateRandomData():
    global worker
    worker = (0, 0)
    nodes[0][0] = 1
    cnt = 0
    while cnt < cart_num:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if x == 0 and y == 0:
            continue
        if nodes[x][y] != 0:
            continue
        nodes[x][y] = 2
        # carts.append((x, y))
        cnt += 1



if __name__ == '__main__':
    main()
