import random
import matplotlib.pyplot as plt
import numpy as np

'''
Generate random points on a plane. rangeX and rangeY set plane's width and length.
'''
def generate(quantity, rangeX=int, rangeY=int):
    points = []
    for i in range(quantity):
        x = random.randrange(0, rangeX)
        y = random.randrange(0, rangeY)
        points.append((x,y))
    return np.array(points)

'''
Matrix of distance between every single generated point
'''
def get_distance_matrix(generated):
    return np.array([[np.linalg.norm(i - j) for j in generated] for i in generated])


'''
Shows plane with points, they're annotated by indexes and connected with lines reflecting the best path.
'''
def show_map(coordinates_list, best_path):
    x,y = (zip(*coordinates_list))
    plt.scatter(*zip(*coordinates_list))
    for i, txt in enumerate (list(range(len(coordinates_list)))):
        plt.annotate(txt,(x[i],y[i]))
    for edge in range(len(best_path)):
        try:
            plt.plot([x[best_path[edge]],x[best_path[edge+1]]],[y[best_path[edge]],y[best_path[edge+1]]],'k-')
        except IndexError:
            pass
    plt.show()