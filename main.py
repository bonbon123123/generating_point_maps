import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import math
import copy
class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.failed_connections=0

    def distance_from_other_point(self, other_point):
        return sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)


    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Line:
    def __init__(self, point1, point2,color="red"):
        self.p1 = point1
        self.p2 = point2
        self.color=color
    def __repr__(self):
        return f"Points({self.p1}, {self.p2})"
    def intersects(self, other):
        # Check if two line segments intersect
        # Implement the line intersection logic
        def orientation(p, q, r):
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        def on_segment(p, q, r):
            if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
                    q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
                return True
            return False

        o1 = orientation(self.p1, self.p2, other.p1)
        o2 = orientation(self.p1, self.p2, other.p2)
        o3 = orientation(other.p1, other.p2, self.p1)
        o4 = orientation(other.p1, other.p2, self.p2)

        if self.p1==other.p1:
            return False
        if self.p1==other.p2:
            return False
        if self.p2==other.p1:
            return False
        if self.p2==other.p2:
            return False

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and on_segment(self.p1, other.p1, self.p2):
            return True

        if o2 == 0 and on_segment(self.p1, other.p2, self.p2):
            return True

        if o3 == 0 and on_segment(other.p1, self.p1, other.p2):
            return True

        if o4 == 0 and on_segment(other.p1, self.p2, other.p2):
            return True

        return False

    def intersection_point(self, other):
        # Find the intersection point of two line segments
        # Implement the logic to find the intersection point
        def line_intersection(p1, p2, p3, p4):
            A1 = p2.y - p1.y
            B1 = p1.x - p2.x
            C1 = A1 * p1.x + B1 * p1.y
            A2 = p4.y - p3.y
            B2 = p3.x - p4.x
            C2 = A2 * p3.x + B2 * p3.y
            det = A1 * B2 - A2 * B1
            if det == 0:
                return None  # Lines are parallel
            else:
                x = (B2 * C1 - B1 * C2) / det
                y = (A1 * C2 - A2 * C1) / det
                return Point(x, y,"yellow")

        return line_intersection(self.p1, self.p2, other.p1, other.p2)

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






class Land:
    def __init__(self, points,color):
        self.color=color
        self.points = points
        for point in self.points:
            point.color=self.color
        self.lines = []
        for i in range(len(points)):
            self.lines.append(Line(points[i], points[(i + 1) % len(points)],self.color))


    def add_line(self, line):
        self.lines.append(line)


    def update_lines(self):
        self.lines = []
        for i in range(len(self.points)):
            self.lines.append(Line(self.points[i], self.points[(i + 1) % len(self.points)],self.color))


    def delete_point(self,point):
        print("deleting")
        self.points.remove(point)
        self.points = sort_points(self.points)
        self.update_lines()

    def my_points(self,points):
        return  [point for point in self.points if point in points]

    def mini_grow(self, hull, points):
        mutual_points = set(points) & set(hull)
        combined_points = list(set(self.points.copy() + list(mutual_points)))
        self.points = sort_points(combined_points)
        for point in self.points:
            point.color = self.color
        self.update_lines()


    def grow_land(self, hull, points_insie):
        combined_points = list(set(self.points.copy() + hull.copy()))
        mutual_points = set(self.points) & set(hull)
        unique_points =  [point for point in combined_points if point not in mutual_points]
        uniquer_points =  [point for point in unique_points if point not in points_insie]
        self.points = sort_points(uniquer_points)
        for point in self.points:
            point.color=self.color
        self.update_lines()

def merge_lands(land1, land2):
    hull_points = sort_points(list(set(land1.points + land2.points)))
    merged_land = Land(hull_points, land1.color)
    return merged_land


def sort_points(points):
    banned_lines=[]
    banned_points=[]
    if not points:
        return []

    def next_point(current_point, points, used_points):
        min_distance = float('inf')
        next_p = None
        for p in points:
            if (p != current_point) and (p not in used_points) and (p not in banned_points):
                dist = current_point.distance_from_other_point(p)
                if dist < min_distance:
                    valid = True
                    if len(banned_lines) > 0:
                        for line in banned_lines:
                            if (next_p is not None) and ((line.p1 == p and line.p2 == next_p) or (line.p2 == p and line.p1 == next_p)):
                                valid = False
                                break
                    if valid:
                        min_distance = dist
                        next_p = p
        return next_p


    start_point = points[0]
    i=0
    thereIsIntersection=True
    while thereIsIntersection:
        used_points = set()
        used_lines=[]
        current_point = start_point
        sorted_points = []
        banned_points=[]


        while len(sorted_points) < len(points) - len(banned_points):
            sorted_points.append(current_point)
            used_points.add(current_point)
            next_p = next_point(current_point, points, used_points)
            if next_p is None:
                print("None")
                current_point.failed_connections+=1
                if(current_point).failed_connections==100:
                    banned_points.append(banned_points)
                    points.remove(current_point)
                i+=1
                if(i>len(points)):
                    i=0
                start_point = points[i]
                break

            used_lines.append(Line(current_point, next_p))
            current_point = next_p
        thereIsIntersection=False
        used_lines.append(Line(sorted_points[0],sorted_points[-1]))
        for line in used_lines:
            for line2 in used_lines:
                if line.intersects(line2):
                    thereIsIntersection=True
                    banned_lines.append(line)
                    banned_lines.append(line2)
                    break
        # total_length = sum(line.p1.distance_from_other_point(line.p2) for line in used_lines)
        # sus_lines=[]
        # average_length = total_length / len(used_lines)
        # for line in used_lines:
        #     if line.p1.distance_from_other_point(line.p2) > average_length*2:
        #         print("sus_lines1")
        #         sus_lines.append(line)
        # if len(sus_lines)>=2:
        #     thereIsIntersection=True
        #     if(sus_lines[0].p2==sus_lines[1].p1):
        #         points.remove(sus_lines[0].p2)
        #     else:
        #         index = sorted_points.index(sus_lines[0].p2)
        #         index2 = sorted_points.index(sus_lines[-1].p1)
        #         points_to_remove = sorted_points[:index +1] + sorted_points[index2-1:]
        #         if len(points_to_remove) <4:
        #             for point in points_to_remove:
        #                 points.remove(point)
    return sorted_points










def jarvis_marszuje(points,mapEditor,land_to_grow=None,points_inside=None):
    print("aktywowany")
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
        land = Land(hull,mapEditor.color)
        mapEditor.add_land(land)
    else:
        for land in land_to_grow:
            print(land.color)
            print(land.points)
        if(len(land_to_grow)==1):
            if land_to_grow[0].color == mapEditor.color:
                print(len(land_to_grow))
                land_to_grow[0].grow_land(hull,points_inside)
            else:
                land = Land(hull,mapEditor.color)
                land.mini_grow(land_to_grow[0].points.copy(),points_inside)
                mapEditor.add_land(land)

        else:
            print("len(land_to_grow)")
            print(len(land_to_grow))
            new_land = Land(hull,mapEditor.color)
            for land in land_to_grow:
                if land.color == mapEditor.color:
                    new_land.grow_land(land.points.copy(),points_inside)
                    mapEditor.remove_lands([land])
                else:
                    new_land.mini_grow(land.points.copy(),points_inside)

            mapEditor.add_land(new_land)





class MapEditor:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.points = []
        self.mode="write"
        self.color="red"
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
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def on_key_press(self, event):
        if event.key == '1':
            self.color="red"
            print("red")
        if event.key == '2':
            self.color="blue"
            print("blue")
        if event.key == '3':
            self.color="green"
            print("green")
        if event.key == '4':
            self.color="yellow"
            print("yellow")
        if event.key == 'd':
            print("deletion mode")
            self.mode="delete"
        if event.key == 'w':
            print("write mode")
            self.mode="write"


    def add_point(self, p):
        self.points.append(p)

    def remove_lands(self, lands_to_remove):
        self.lands = [land for land in self.lands if land not in lands_to_remove]

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
        if self.mode == "delete":
            if event.inaxes == self.ax and event.button == 3:
                clicked_x, clicked_y = event.xdata, event.ydata
                new_point = Point(clicked_x, clicked_y, "blue")
                for land in self.lands:
                    for point in land.points:
                        distance = new_point.distance_from_other_point(point)
                        if distance <= self.search_range/10:
                            land.delete_point(point)
            self.update_map()
        if self.mode == "write":
            if event.inaxes == self.ax and event.button == 3:
                clicked_x, clicked_y = event.xdata, event.ydata
                half_plot_size = self.plot_size / 3
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
                            new_points = area.generate_points(10, self.plot_size / self.rows, "black")
                            self.points.extend(new_points)


                new_point = Point(clicked_x, clicked_y, self.color)
                points_to_do=[]

                for point in self.points:
                    distance = new_point.distance_from_other_point(point)
                    if distance <= self.search_range:
                        points_to_do.append(point)

                has_land_point = False
                land_found=[]
                points_inside=[]
                for land in self.lands:

                    for point in land.points:
                        distance = new_point.distance_from_other_point(point)
                        if distance <= self.search_range:
                            points_inside.append(point)
                            point.color="black"
                            points_to_do.append(point)
                            has_land_point = True
                            if land in land_found:
                                continue
                            land_found.append(land)



                if not has_land_point:
                    jarvis_marszuje(points_to_do,self)
                else:
                    jarvis_marszuje(points_to_do,self,land_found,points_inside)

                for point in points_to_do:
                    if point in self.points:
                        self.points.remove(point)
                # print("first print")
                # for land in self.lands:
                #     print(land.points)
                # for land in land_found:
                #     if land in self.lands:
                #         print(land.points)
                        # self.lands.remove(land)
                # print("printed")
                # for land in self.lands:
                #     print(land.points)

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

                plt.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], color=line.color)

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
