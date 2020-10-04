# 
# This file is part of the GNU General Public License v3.0 distribution 
# https://github.com/balamuruganky/path_planning
# Copyright (c) 2020 Balamurugan Kandan
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
from scipy import interpolate
from IShape import IShape
from PoseHelper import prepare_points_from_list, calculate_yaw
from PlotHelper import points_with_yaw_plot

class CubicSpline(IShape):
    def __init__(self, points, is_periodic=False):
        self.points = prepare_points_from_list(points, is_periodic)
        self.sample_step = 0.1
        self.max_samples = 1000
        self.min_samples = 100
        self.is_points_valid = False
        self.validate_points()
        self.is_periodic = is_periodic

    def validate_points(self):
        for i in range(1,len(self.points)):
            if np.linalg.norm(self.points[i-1] - self.points[i]) < 0.01:
                self.is_points_valid = False
            else:
                self.is_points_valid = True

    def sample_points(self):
        if self.is_points_valid is False:
            print "Error : Please check the points..."
            return None, None

        nPoints = len(self.points)
        xPoints = np.array([point[0] for point in self.points])
        yPoints = np.array([point[1] for point in self.points])

        step_size, total_steps = self.sample_rate()

        x=self.points[:,0]
        y=self.points[:,1]

        tck,u = interpolate.splprep([x,y],k=3,s=0)
        u=np.linspace(0,1,total_steps,step_size)
        out = interpolate.splev(u,tck)

        samples = np.array((out[0], out[1])).T
        yaw_samples = calculate_yaw(samples)
        return (samples, yaw_samples)

if __name__ == '__main__':
    bz = CubicSpline([[1,2],[10.5, 4.5],[5,6],[23.5,15.5],[20,2],[30.5,5.5]], True)
    samples, yaw_samples = bz.sample_points()
    points_with_yaw_plot(bz.name, bz.points, samples, yaw_samples)