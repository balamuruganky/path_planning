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
import matplotlib.pyplot as plt
import math
import uuid

def points_with_yaw_plot(name, points, samples, yaw_samples = None, save_only=False):
    unique_filename = str(uuid.uuid4())
    name = name + '_' + unique_filename
    plt.figure(name)

    np_pts = np.split(points,2,axis=1) 
    plt.plot(np_pts[0],np_pts[1],"o")
    for i in range(0,len(np_pts[0])):
        plt.text( np_pts[0][i],np_pts[1][i] , str(i) )
    plt.plot(samples[0][0],samples[0][1],"go",markersize=15)    
    plt.plot(samples[-1][0],samples[-1][1],"ro",markersize=15)

    np_s = np.split(samples,2,axis=1)
    plt.plot(np_s[0],np_s[1],"yo")

    if yaw_samples is not None:
        for j in range(0, len(yaw_samples)):
            new_y = math.sin(yaw_samples[j])
            new_x = math.cos(yaw_samples[j])
            plt.quiver(samples[j][0], samples[j][1], new_x, new_y, width=0.001)

    plt.axis("equal")
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    if save_only is False:
        plt.show()
    else:
        plt.savefig(name)
