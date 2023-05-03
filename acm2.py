import itertools
import random


class TravelingCartSystem:
    def __init__(self, map_width=5, map_height=5, num_carts=3):
        self.map_width = map_width
        self.map_height = map_height
        self.num_carts = num_carts
        self.grid_size = 3
        self.cart_positions = []
        self.cart_rects = []
        self.generate_map()
        self.generate_carts()

    def generate_map(self):
        # create the map
        self.map = []
        for i in range(self.map_height):
            row = []
            for j in range(self.map_width):
                row.append(".")
            self.map.append(row)

    def generate_carts(self):
        # generate random positions for the carts and user
        self.user_x, self.user_y = self.get_random_position()
        for i in range(self.num_carts):
            cart_x, cart_y = self.get_random_position()
            while (cart_x, cart_y) == (self.user_x, self.user_y) or (cart_x, cart_y) in self.cart_positions:
                cart_x, cart_y = self.get_random_position()
            self.cart_positions.append((cart_x, cart_y))

    def run_system(self):
        while True:
            # display the menu and get user input
            print("Traveling Shopping Cart Worker System")
            print("1. Go get carts")
            print("2. Settings")
            print("3. Exit")
            choice = input("Enter your choice: ")
            print()

            # process the user's choice
            if choice == "1":
                self.get_carts()
            elif choice == "2":
                self.settings()
            elif choice == "3":
                break
            else:
                print("Invalid choice")

    def get_carts(self):
        self.display_map()
        self.choose_algorithm()

    def display_map(self):
        # display the user and cart positions on the map
        self.map[self.user_y // self.grid_size][self.user_x // self.grid_size] = "U"
        for cart_x, cart_y in self.cart_positions:
            self.map[cart_y // self.grid_size][cart_x // self.grid_size] = "C"

        # print the map
        for row in self.map:
            for cell in row:
                print(cell.center(self.grid_size), end="")
            print()

        # reset the map
        self.map[self.user_y // self.grid_size][self.user_x // self.grid_size] = "."
        for cart_x, cart_y in self.cart_positions:
            self.map[cart_y // self.grid_size][cart_x // self.grid_size] = "."

    def choose_algorithm(self):
        print("Choose a method to conduct the route calculation:")
        print("1. random cart order")
        print("2. brute force for a shortest route")
        choice = input("Enter your choice: ")
        print()
        cart_order = None
        if choice == "1":
            cart_order = self.random_cart_order()
            self.update_directions(cart_order)
        elif choice == "2":
            cart_order = self.brute_force_order()
            self.update_directions(cart_order)


    def brute_force_order(self):
        # Generate all possible cart orderings
        cart_orderings = itertools.permutations(range(self.num_carts))

        # Find shortest path
        shortest_path = None
        shortest_distance = None
        for order in cart_orderings:
            distance = self.get_distance(order)
            if shortest_distance is None or distance < shortest_distance:
                shortest_path = order
                shortest_distance = distance
        return shortest_path

    def get_distance(self, order):
        total_distance = 0
        prev_pos = (self.user_x, self.user_y)
        for i, cart_idx in enumerate(order):
            curr_pos = self.cart_positions[cart_idx]
            total_distance += self.manhattan_distance(curr_pos, prev_pos)
            prev_pos = curr_pos
        return total_distance

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def update_directions(self, cart_order):
        directions = f"You are at ({self.user_x // self.grid_size}, {self.user_y // self.grid_size}). Here are the directions to get your carts:\n"
        for i in range(len(cart_order)):
            start_pos = (self.user_x, self.user_y) if i == 0 else self.cart_positions[cart_order[i - 1]]
            end_pos = self.cart_positions[cart_order[i]]
            directions += self.generate_directions(start_pos, end_pos)
        directions += "Now you have all the carts."
        directions += "\n\n"
        print(directions)

    def random_cart_order(self):
        # generate a random order for visiting the carts
        cart_order = list(range(self.num_carts))
        random.shuffle(cart_order)
        return cart_order

    def get_random_position(self):
        x = random.randint(0, self.map_width * self.grid_size - self.grid_size)
        y = random.randint(0, self.map_height * self.grid_size - self.grid_size)
        return x, y

    def generate_directions(self, start_pos, end_pos):
        directions = f"From ({start_pos[0] // self.grid_size}, {start_pos[1] // self.grid_size}) "
        if start_pos[0] == end_pos[0]:
            if start_pos[1] < end_pos[1]:
                directions += f"go down to ({end_pos[0] // self.grid_size}, {end_pos[1] // self.grid_size})"
            else:
                directions += f"go up to ({end_pos[0] // self.grid_size}, {end_pos[1] // self.grid_size})"
        elif start_pos[1] == end_pos[1]:
            if start_pos[0] < end_pos[0]:
                directions += f"go right to ({end_pos[0] // self.grid_size}, {end_pos[1] // self.grid_size})"
            else:
                directions += f"go left to ({end_pos[0] // self.grid_size}, {end_pos[1] // self.grid_size})"
        else:
            if start_pos[0] < end_pos[0]:
                if start_pos[1] < end_pos[1]:
                    directions += f"go right and down to ({end_pos[0] // self.grid_size}, {end_pos[1] // self.grid_size})"
                else:
                    directions += f"go right and up to ({end_pos[0] // self.grid_size}, {end_pos[1] // self.grid_size})"
            else:
                if start_pos[1] < end_pos[1]:
                    directions += f"go left and down to ({end_pos[0] // self.grid_size}, {end_pos[1] // self.grid_size})"
                else:
                    directions += f"go left and up to ({end_pos[0] // self.grid_size}, {end_pos[1] // self.grid_size})"
        directions += ";\nPick up your cart.\n"
        return directions

    def settings(self):
        # get the new settings from the user
        print("Current settings:")
        print(f"Map size: {self.map_width}x{self.map_height}")
        print(f"Number of carts: {self.num_carts}")
        print(f"Grid size: {self.grid_size}")
        print()
        new_map_width = int(input("Enter new map width: "))
        new_map_height = int(input("Enter new map height: "))
        new_num_carts = int(input("Enter new number of carts: "))
        new_grid_size = int(input("Enter new grid size: "))

        # update the settings and regenerate the map and cart positions
        self.map_width = new_map_width
        self.map_height = new_map_height
        self.num_carts = new_num_carts
        self.grid_size = new_grid_size
        self.generate_map()
        self.cart_positions = []
        self.generate_carts()


if __name__ == "__main__":
    system = TravelingCartSystem()
    system.run_system()
