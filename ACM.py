import itertools
import math
import random
import time

rows = 40
columns = 21
cart_num = 5


# Brute force implementation of tsp
def tsp(cities):
    # Generate all possible permutations of the cities
    permutations = itertools.permutations(cities)

    # Initialize variables for the shortest distance and route
    shortest_distance = float('inf')
    shortest_route = None

    # Iterate over each permutation and calculate its distance
    for route in permutations:
        route_distance = 0
        for i in range(len(route) - 1):
            route_distance += distance(route[i], route[i + 1])
        # Add the distance from the last city back to the first city
        route_distance += distance(worker, route[0])
        route_distance += distance(worker, route[len(route)-1])

        # Update the shortest distance and route if necessary
        if route_distance < shortest_distance:
            shortest_distance = route_distance
            shortest_route = route

    return shortest_route, shortest_distance


# Calculate the distance between two cities
def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.fabs(x1 - x2) + math.fabs(y1 - y2)

worker = []
carts = []
nodes = [[0 for i in range(rows)] for i in range(columns)]

def printMap():
    # Basic information
    print('Legend: ')
    print('P - You')
    print('_ - No items')
    print('C - Cart')
    print('Coordinates are (Row, Col)')
    print()
    # Display of location information
    col_str = "{0:3s}".format('')
    for i in range(rows):
        col_str = col_str + "{0:<3s}".format(str(i))
    print(col_str)
    for i in range(rows):
        row_str = '{0:<3s}'.format(str(i))
        for j in range(columns):
            row_str = row_str + '{0:<3s}'.format(toSymbol(nodes[i][j]))
        print(row_str)


def getCarts():
    printMap()
    # Choose algorithm
    print('Please choose the algorithm: ')
    print('1 - Carts Order')
    print('2 - Brute Force')
    choice = eval(input())
    # The first choice of the algorithm
    route = []
    dis = 0
    # The duration of the running time of the algorithm
    duration = 0.0
    if choice == 1:
        t = time.perf_counter()
        route += carts
        dis += distance(worker, carts[0])
        for i in range(len(carts)-1):
            dis += distance(carts[i], carts[i+1])
        dis += distance(worker, carts[len(carts)-1])
        duration = time.perf_counter() - t
    elif choice == 2:
        # Output the route information
        t = time.perf_counter()
        shortest_route, shortest_dis = tsp(carts)
        duration = time.perf_counter() - t
        route += (shortest_route)
        dis += shortest_dis

    print("Route:")
    print('Move from', worker, "to", route[0])
    for i in range(len(route) - 1):
        print("Move from", route[i], "to", route[i + 1])
    print('Move from', route[len(route) - 1], "to", worker)
    print(f'Duration: {duration:.8f}s')
    print()


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
    print("The location of worker is at [0, 0] as default")
    print("The location of carts are generated randomly")
    print("The default map size is 5 by 5")
    print("Please input the corresponding number to choose the next step.")
    print("1 - Input worker location manually")
    print("2 - Input cart location manually")
    print("3 - Change map size")
    print('4 - Set the maximum carts number')
    num = eval(input())
    global worker
    global carts
    global rows
    global nodes
    global cart_num
    if num == 1:
        nodes[worker[0]][worker[1]] = 0
        print("Input the location of worker as x,y. For example 0,0")
        content = input()
        arr = content.split(",")
        x, y = eval(arr[0]), eval(arr[1])
        nodes[x][y] = 1
        worker = [x, y]
    elif num == 2:
        print("The current number of carts in this system is ", cart_num)
        print("Input the location of", cart_num,  "carts as x,y. For example 1,2")
        for cart in carts:
            nodes[cart[0]][cart[1]] = 0
        carts = []
        for i in range(cart_num):
            content = input()
            arr = content.split(",")
            x, y = eval(arr[0]), eval(arr[1])
            nodes[x][y] = 2
            carts.append([x, y])
    elif num == 3:
        print('The current map size is', rows, 'by', columns)
        print('Input the new size number')
        rows = eval(input())
        columns = eval(input())
        carts = []
        nodes = [[0 for i in range(rows)] for i in range(columns)]
        # Refresh the data
        generateRandomData()
    elif num == 4:
        print('Input new maximum cart number')
        cart_num = eval(input())
    else:
        print("Invalid input! Please input again. ")

def main():
    # Generate random data before running
    generateRandomData()

    while True:
        print("Welcome to Ants Carts Moving, please input the corresponding number to choose the next step.")
        print("1 - Get Carts")
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
    worker = [0, 0]
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
        carts.append([x, y])
        cnt += 1

def loadFromFile():
    global worker
    worker = [0, 0]
    nodes[0][0] = 1
    f = open('data.txt', 'r')
    text = f.readlines()

    node_x = []
    node_y = []

    for i in range(len(text) - 1):
        line = text[i + 1]
        strs = line.split()
        x = math.floor(eval(strs[1]))
        y = math.floor(eval(strs[2]))
        node_x.append(x)
        node_y.append(y)

    max_x = 0
    max_y = 0
    for i in range(len(node_x)):
        if node_x[i] > max_x:
            max_x = node_x[i]
    for i in range(len(node_y)):
        if node_y[i] > max_y:
            max_y = node_y[i]
    rows = max_x
    columns = max_y
    global nodes
    nodes = [[0 for i in range(rows)] for i in range(columns)]
    for i in range(len(node_x)):
        nodes[node_x][node_y] = 2


if __name__ == '__main__':
    main()
