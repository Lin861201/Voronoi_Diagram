from scipy.spatial import ConvexHull, convex_hull_plot_2d
import numpy as np
import matplotlib.pyplot as plt
import cv2
rng = np.random.default_rng()
points = rng.random((6, 2))   # 30 random points in 2-D
print(points)
hull = ConvexHull(points)

# def f(points):
#     if points.shape[0] > 6:
#         m = points.shape[0] // 2
#         f(points[:m])
#         f(points[m:])
#     else:
#         hull = ConvexHull(points)
#         for simplex in hull.simplices:
#             print(simplex)
#             plt.plot(points[simplex, 0], points[simplex, 1], 'k-.')

# f(points)
print(hull.vertices)

import matplotlib.pyplot as plt
plt.plot(points[:,0], points[:,1], 'o')
for simplex in hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], 'k-.')
print(hull.simplices)

# plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
# plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
plt.show()
