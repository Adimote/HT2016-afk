import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from input_reader import *

class PlaneFitter:

  data = None
  X = None
  Y = None
  XX = None
  YY = None

  def __init__(self, data):
    self.data = data

  def fit(self):
    self.init_meshgrid()
    self.get_linear_plane()

  def init_meshgrid(self):
    # regular grid covering the domain of the data
    mn = np.min(self.data, axis=0)
    mx = np.max(self.data, axis=0)
    self.X, self.Y = np.meshgrid(np.linspace(mn[0], mx[0], 20), np.linspace(mn[1], mx[1], 20))
    self.XX = self.X.flatten()
    self.YY = self.Y.flatten()

  def get_linear_plane(self):
    # best-fit linear plane
    A = np.c_[self.data[:,0], self.data[:,1], np.ones(self.data.shape[0])]
    C,_,_,_ = np.linalg.lstsq(A, data[:,2])    # coefficients

    # evaluate it on grid
    self.Z = C[0]*self.X + C[1]*self.Y + C[2]

  def visualise(self):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(self.X, self.Y, self.Z, rstride=1, cstride=1, alpha=0.2)
    ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
    plt.xlabel('X')
    plt.ylabel('Y')
    ax.set_zlabel('Z')
    ax.axis('equal')
    ax.axis('tight')
    plt.show()

if __name__ == '__main__':
  filename = raw_input('txt point cloud data:')
  reader = InputReader(filename)
  data = reader.data
  print data

  fitter = PlaneFitter(data)
  fitter.fit()
  fitter.visualise()
