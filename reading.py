import json
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class Line:
    def __init__(self, point1, point2, color="red"):
        self.p1 = point1
        self.p2 = point2
        self.color = color

class Land:
    def __init__(self, points, color):
        self.color = color
        self.points = points
        self.lines = [Line(points[i], points[(i + 1) % len(points)], color) for i in range(len(points))]

def load_lands_from_file(filename):
    """
    Odczytuje landy z pliku tekstowego i zwraca listę obiektów land.
    """
    lands = []
    with open(filename, 'r') as file:
        land_data = json.load(file)
        for land_dict in land_data:
            color = land_dict["color"]
            points = [Point(x, y, color) for x, y in land_dict["points"]]
            land = Land(points, color)
            lands.append(land)
    return lands

def display_lands(lands):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    for land in lands:
        for line in land.lines:
            ax.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], color=line.color)
        for point in land.points:
            ax.plot(point.x, point.y, 'o', color=point.color)
    ax.set_title('Mapa z wczytanymi landami')
    ax.set_aspect('equal')
    plt.show()

if __name__ == "__main__":
    filename = "lands_data.txt"
    loaded_lands = load_lands_from_file(filename)
    display_lands(loaded_lands)
