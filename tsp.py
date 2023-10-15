import random
import math

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ant:
    def __init__(self, num_cities):
        self.visited = [random.randint(0, num_cities - 1)]

    def visit(self, city):
        self.visited.append(city)

class AntColony:
    def __init__(self, num_ants, num_cities, alpha, beta, rho, Q):
        self.num_ants = num_ants
        self.num_cities = num_cities
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.pheromone = [[1 / num_cities] * num_cities for _ in range(num_cities)]
        self.distances = [[0 if i == j else random.randint(10, 100) for j in range(num_cities)] for i in range(num_cities)]

    def select_next_city(self, ant, visited):
        current_city = ant.visited[-1]
        unvisited_cities = [i for i in range(self.num_cities) if i not in visited]
        probabilities = [((self.pheromone[current_city][city])**self.alpha) * ((1/self.distances[current_city][city])**self.beta) for city in unvisited_cities]
        probabilities_sum = sum(probabilities)
        probabilities = [prob / probabilities_sum for prob in probabilities]
        next_city = random.choices(unvisited_cities, probabilities)[0]
        return next_city

    def run(self, max_epochs):
        best_route = None
        best_distance = float('inf')
        for epoch in range(max_epochs):
            ants = [Ant(self.num_cities) for _ in range(self.num_ants)]
            for ant in ants:
                for _ in range(self.num_cities - 1):
                    next_city = self.select_next_city(ant, ant.visited)
                    ant.visit(next_city)

            for i in range(self.num_cities):
                for j in range(self.num_cities):
                    self.pheromone[i][j] *= (1 - self.rho)
            
            for ant in ants:
                distance = self.calculate_route_distance(ant.visited)
                if distance < best_distance:
                    best_distance = distance
                    best_route = ant.visited

                for i in range(len(ant.visited) - 1):
                    self.pheromone[ant.visited[i]][ant.visited[i+1]] += self.Q / distance

            print(f"Epoch {epoch + 1}: Best Distance = {best_distance:.2f}")

        return best_route

    def calculate_route_distance(self, route):
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distances[route[i]][route[i+1]]
        distance += self.distances[route[-1]][route[0]]
        return distance

# Function to generate random cities within a 200x200 plane
def generate_random_cities(num_cities):
    random.seed(42)  # Set random seed for reproducibility
    city_list = [City(random.randint(0, 200), random.randint(0, 200)) for _ in range(num_cities)]
    return city_list

# Main program
num_cities = 25
num_ants = 50
alpha = 1
beta = 2
rho = 0.1
Q = 1

city_list = generate_random_cities(num_cities)

aco = AntColony(num_ants, num_cities, alpha, beta, rho, Q)
best_route = aco.run(max_epochs=100)

print("Best route found:")
for city_index in best_route:
    city = city_list[city_index]
    print(f"City at ({city.x}, {city.y})")
