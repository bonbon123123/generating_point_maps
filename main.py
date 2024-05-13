import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import math
class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def distance_from_other_point(self, other_point):
        return sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)

class Line:
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

class MapArea:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.points_generated = False
        self.points = []

    def generate_points(self, num_points, area_size,color):
        if not self.points_generated:
            for _ in range(num_points):
                point_x = np.random.randint(self.x*self.size  , (self.x+1)*self.size)
                point_y = np.random.randint(self.y*self.size  , (self.y+1)*self.size)
                self.points.append(Point(point_x, point_y, color))
            self.points_generated = True

            return self.points
        else:
            return []


def orientation(p, q, r):
    """Return positive if p-q-r are clockwise, neg if counterclockwise, zero if collinear."""
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    return 1 if val > 0 else -1


def jarvis_marszuje(points,mapEditor,land_to_grow=None):
    n = len(points)
    if n < 3:
        return points

    leftmost_index = 0
    for i in range(1, n):
        if points[i].x < points[leftmost_index].x:
            leftmost_index = i

    hull = []
    p = leftmost_index
    while True:
        hull.append(points[p])
        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[q], points[i]) == -1:
                q = i
        p = q
        if p == leftmost_index:
            break

    if land_to_grow==None:
        land = Land(hull)
        mapEditor.add_land(land)
    else:
        print("mamy land do rosnięcia")
        land_to_grow.grow_land(hull)
    # for point in hull:
    #     point.color="green"
    #     mapEditor.add_point(point)
    #
    # for i in range(len(hull)):
    #     mapEditor.add_line(hull[i], hull[(i + 1) % len(hull)])

class Land:
    def __init__(self, points):
        self.points = points
        self.lines = []
        for i in range(len(points)):
            self.lines.append(Line(points[i], points[(i + 1) % len(points)]))

    def add_line(self, line):
        self.lines.append(line)

    def add_point(self, point):
        self.points.append(point)

class Land:
    def __init__(self, points):
        self.points = points
        self.lines = []
        for i in range(len(points)):
            self.lines.append(Line(points[i], points[(i + 1) % len(points)]))

    def add_line(self, line):
        self.lines.append(line)

    def add_point(self, point):
        self.points.append(point)

    def grow_land(self, hull):
        common_points = [p for p in hull if p in self.points]
        for point in hull:
            for point1 in self.points:
                if(point.x==point1.x and point.y==point1.y ):
                    print(point.x,point.y)
        print("nie moje punkty:")
        for point1 in hull:
            print(point1.x,point1.y)
        print("moje punkty:")
        for point1 in self.points:
            print(point1.x,point1.y)
        if len(common_points) == 1 or len(common_points) == 2:

            for point in hull:
                print("point.x:")
                print(point.x)

                if point not in self.points:
                    index = self.points.index(common_points[-1]) + 1
                    self.points.insert(index, point)
        else:
            first_common = self.points.index(common_points[0])
            last_common = self.points.index(common_points[-1])

            new_points = []
            for point in hull:
                print("point.x:")
                print(point.x)
                if point not in self.points:
                    new_points.append(point)

            self.points = self.points[:first_common + 1] + new_points + self.points[last_common:]

        self.lines = []
        for i in range(len(self.points)):
            self.lines.append(Line(self.points[i], self.points[(i + 1) % len(self.points)]))



def update_land(self, map_editor):
        for line in self.lines:
            map_editor.add_line(line.p1, line.p2)

        for point in self.points:
            point.color = "green"
            map_editor.add_point(point)


# def convex_hull(points,mapEditor):
#     n = len(points)
#     if n < 3:
#         return "Za mało punktów"
#
#
#     points.sort(key=lambda point: point.x)
#
#     lower_hull = []
#     for point in points:
#         while len(lower_hull) >= 2 and orientation(lower_hull[-2], lower_hull[-1], point) != 2:
#             lower_hull.pop()
#         lower_hull.append(point)
#
#     upper_hull = []
#     for point in reversed(points):
#         while len(upper_hull) >= 2 and orientation(upper_hull[-2], upper_hull[-1], point) != 2:
#             upper_hull.pop()
#         upper_hull.append(point)
#
#     upper_hull.pop()
#
#     hull = lower_hull + upper_hull
#
#     for point in hull:
#         point.color="green"
#         mapEditor.add_point(point)
#
#     for i in range(len(hull)):
#         mapEditor.add_line(hull[i], hull[(i + 1) % len(hull)])


class MapEditor:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.points = []
        self.lines = []
        self.lands=[]
        self.plot_size = 1000
        self.search_range=100
        self.range_of_adding=1
        self.ax.set_xlim(0, self.plot_size)
        self.ax.set_ylim(0, self.plot_size)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.set_aspect('equal')
        self.rows=10
        self.last_clicked_x=None
        self.last_clicked_y=None
        self.map_coverage = []

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def add_line(self, p1, p2):
        self.lines.append(Line(p1, p2))

    def add_point(self, p):
        self.points.append(p)
    def add_land(self,land):
        self.lands.append(land)
    def create_map_area(self, x, y):
        area_size = self.plot_size / self.rows
        adjacent_areas = []

        found = False
        for area in self.map_coverage:
            if(area.x == x and area.y == y):
                found = True
        if(not found):
            self.map_coverage.append(MapArea(x, y, area_size))
            adjacent_areas.append(MapArea(x, y, area_size))

        return adjacent_areas

    def onclick(self, event):
        if event.inaxes == self.ax and event.button == 3:
            clicked_x, clicked_y = event.xdata, event.ydata
            half_plot_size = self.plot_size / 2
            if(self.last_clicked_x is None and self.last_clicked_y is None):
                if((abs(clicked_x) > half_plot_size or abs(clicked_y) > half_plot_size)):
                    self.last_clicked_x = clicked_x
                    self.last_clicked_y = clicked_y
            elif( abs(self.last_clicked_x - clicked_x) > half_plot_size or abs(self.last_clicked_y - clicked_y) > half_plot_size):
                self.last_clicked_x = clicked_x
                self.last_clicked_y = clicked_y


            for i in range(math.floor((clicked_x - self.search_range) / (self.plot_size / self.rows)), math.floor((clicked_x + self.search_range) / (self.plot_size / self.rows))+1):
                for j in range(math.floor((clicked_y - self.search_range) / (self.plot_size / self.rows)), math.floor((clicked_y + self.search_range) / (self.plot_size / self.rows))+1):
                    adjacent_areas = self.create_map_area(i, j)
                    for area in adjacent_areas:
                        new_points = area.generate_points(10, self.plot_size / self.rows, "red")
                        self.points.extend(new_points)


            new_point = Point(clicked_x, clicked_y, "blue")
            points_to_do=[]

            for point in self.points:
                distance = new_point.distance_from_other_point(point)
                if distance <= self.search_range:
                    points_to_do.append(point)

            has_land_point = False
            for land in self.lands:
                for point in land.points:
                    distance = new_point.distance_from_other_point(point)
                    if distance <= self.search_range:
                        print("znalezion")
                        jarvis_marszuje(points_to_do,self,land)
                        has_land_point = True
                        break

            if not has_land_point:
                self.lines=[]
                jarvis_marszuje(points_to_do,self)

            for point in points_to_do:
                if point in self.points:
                    self.points.remove(point)

            self.lines=[]
            jarvis_marszuje(points_to_do,self)

            self.update_map()

    def update_map(self):
        self.ax.clear()
        if self.last_clicked_x is not None and self.last_clicked_y is not None:
            half_plot_size = self.plot_size / 2
            self.ax.set_xlim(self.last_clicked_x - half_plot_size, self.last_clicked_x +half_plot_size)
            self.ax.set_ylim(self.last_clicked_y - half_plot_size, self.last_clicked_y + half_plot_size)

        else:
            self.ax.set_xlim(0, 1000)
            self.ax.set_ylim(0, 1000)
        for land in self.lands:
            for line in land.lines:
                plt.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], 'r-', marker='o')

            for point in land.points:
                self.ax.plot(point.x, point.y, 'o', color=point.color)
        # for line in self.lines:
        #     plt.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], 'r-', marker='o')
        #
        for point in self.points:
            self.ax.plot(point.x, point.y, 'o', color=point.color)

        self.ax.set_title('Mapa z dodanymi punktami i obszarami')
        self.ax.set_aspect('equal')
        self.fig.canvas.draw()

if __name__ == "__main__":
    map_editor = MapEditor()
    plt.show()
