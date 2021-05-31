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
from IShape import IShape
from PoseHelper import prepare_points_from_list, calculate_yaw, distance
from PlotHelper import points_with_yaw_plot

class Line(IShape):
    def __init__(self, points, is_periodic=False):
        self.points = prepare_points_from_list(points, is_periodic)
        self.sample_step = 0.5
        self.max_samples = 1000
        self.min_samples = 100
        self.is_points_valid = False
        self.validate_points()
        self.offset_dist = 0.0

    def validate_points(self):
        for i in range(1,len(self.points)):
            if np.linalg.norm(self.points[i-1] - self.points[i]) < 0.01:
                self.is_points_valid = False
            else:
                self.is_points_valid = True

    def offset_point(self, point, dx, dy, distRatio):
        return ([point[ 0 ] - dy * distRatio,
                point[ 1 ] + dx * distRatio])

    def sample_points(self):
        if self.is_points_valid is False:
            print "Error : Please check the points..."
            return None, None

        totalDist = 0
        ctrlPtDists = [0]
        ptOffsetRatios = []

        for pt in range(len(self.points) - 1):
            dist = distance( self.points[ pt ], self.points[ pt + 1 ] )
            totalDist += dist;
            ptOffsetRatios.append( self.offset_dist / dist )
            ctrlPtDists.append(totalDist)

        step_size, total_steps = self.sample_rate()

        samples = []
        # Starting point
        samples.append(self.offset_point(
            self.points[ 0 ],
            self.points[ 1 ][ 0 ] - self.points[ 0 ][ 0 ],
            self.points[ 1 ][ 1 ] - self.points[ 0 ][ 1 ],
            ptOffsetRatios[ 0 ]
            ))

        prevCtrlPtInd = 0
        currDist = 0
        currPoint = self.points[0]
        nextDist = step_size

        for pt in range((int(total_steps) - 1)):
            while( nextDist > ctrlPtDists[ prevCtrlPtInd + 1 ] ):
                prevCtrlPtInd = (prevCtrlPtInd + 1)
                currDist = ctrlPtDists[ prevCtrlPtInd ]
                currPoint = self.points[ prevCtrlPtInd ]

            remainingDist = (nextDist - currDist)
            ctrlPtsDeltaX = self.points[ prevCtrlPtInd + 1 ][ 0 ] - self.points[ prevCtrlPtInd ][ 0 ]
            ctrlPtsDeltaY = self.points[ prevCtrlPtInd + 1 ][ 1 ] - self.points[ prevCtrlPtInd ][ 1 ]
            ctrlPtsDist = ctrlPtDists[ prevCtrlPtInd + 1 ] - ctrlPtDists[ prevCtrlPtInd ]
            distRatio = remainingDist / ctrlPtsDist

            if not np.isclose(remainingDist, step_size):
                residue = [
                    currPoint[ 0 ],
                    currPoint[ 1 ]
                    ]
                samples.append( self.offset_point(
                    residue, ctrlPtsDeltaX, ctrlPtsDeltaY, ptOffsetRatios[ prevCtrlPtInd ])
                )
            else:
                currPoint = [
                    currPoint[ 0 ] + ctrlPtsDeltaX * distRatio,
                    currPoint[ 1 ] + ctrlPtsDeltaY * distRatio
                    ]
                samples.append( self.offset_point(
                    currPoint, ctrlPtsDeltaX, ctrlPtsDeltaY, ptOffsetRatios[ prevCtrlPtInd ])
                )

            currDist = nextDist
            nextDist += step_size

        samples.append( self.offset_point(
            self.points[ len(self.points) - 1 ],
            self.points[ len(self.points) - 1 ][ 0 ] -
            self.points[ len(self.points) - 2 ][ 0 ],
            self.points[ len(self.points) - 1 ][ 1 ] -
            self.points[ len(self.points) - 2 ][ 1 ],
            ptOffsetRatios[ len(ptOffsetRatios) - 1 ]
            ))
        samples = np.asarray(samples)
        return samples, calculate_yaw(samples)

if __name__ == '__main__':
    bz = Line([[1,2],[10.5, 4.5],[5,6],[23.5,15.5],[20,2],[30.5,5.5]], True)
    samples, yaw_samples = bz.sample_points()
    #print samples, yaw_samples
    points_with_yaw_plot(bz.name, bz.points, samples, yaw_samples)
