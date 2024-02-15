'''
Author: CSuperlei
Date: 2024-02-15 16:37:13
LastEditTime: 2024-02-15 17:00:37
Description: 
'''
import numpy as np
import random
import os
import time
from mayavi import mlab
from scipy.spatial import Delaunay
from tvtk.api import tvtk
from io import StringIO


def point_cloud(HIFT_res):
    '''
    show the ocean rendered point cloud of the data
    x, y, z: the coordinate of the point cloud of HIFT
    '''
    for idx, data in enumerate(HIFT_res):
        mlab.clf()

        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]

        mlab.points3d(x, y, z, color=(0.47, 0.62, 0.74), mode='sphere', colormap='jet', scale_factor=0.7)
        mlab.show()


def surface_cloud(HIFT_res):
    '''
    show the ocean rendered surface of the data
    x, y, z: the coordinate of the point cloud of HIFT
    '''
    for idx, data in enumerate(HIFT_res):
        mlab.clf()

        tri = Delaunay(data[:, :2])  
        triangles = tri.simplices

        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        colors = z

        mlab.triangular_mesh(x, y, z, triangles, scalars=colors, colormap='Blues')
