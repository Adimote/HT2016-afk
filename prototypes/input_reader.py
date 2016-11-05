import numpy as np

__all__ = ['InputReader']

class InputReader:

  def __init__(self, file_name):
    extension = file_name.split('.')[-1]
    data = None

    if extension == 'txt':
      # Parse the points
      with open(file_name, 'r') as f:
        x = []
        y = []
        z = []
        lines = f.readlines()

        for line in lines:
          x.append(float(line.split(' ')[0]))
          y.append(float(line.split(' ')[1]))
          z.append(float(line.split(' ')[2].split('\n')[0]))

        self.data = np.c_[x, y, z]
