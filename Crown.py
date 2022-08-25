from math import floor
from typing import List, Tuple
import pygame as pg
import numpy as np
class Crown:
    """
    Class for only visual effect on map.
    makes pseudo progress bar for complited tasks
    """
    def genereate_points(self,n,procent)->Tuple[List[Tuple[float,float]],List[Tuple[float,float]]]:
        """
        generate complited and incomplited marks around unit circle (max 16)
        (precomputed values)

        args :
            n : int - number of tasks
            procent : float - % of completed tasks
        return
            good : List[Tuple[float,float]] - complited tasks marks
            bad : List[Tuple[float,float]] - incomplited tasks marks
        """
        alpha = np.pi/2
        dalpha = -2*np.pi/16
        pr = floor(procent*n)
        tab = [(np.cos(alpha+i*dalpha),np.sin(alpha+i*dalpha)) for i in range(n)]
        if pr == 0:
            good = []
            bad = tab
        elif pr == n:
            good = tab
            bad = []
        else:
            good = tab[:pr]
            bad = tab[pr:]
        return good,bad

    def __init__(self,lst,n):
        """
        Initialization of Crown (progress bar)

        args :
            lst : Lst[int] - list of indexes of complited tasks
            n : int - number of all tasks
        """
        self.len_lst = len(lst)
        self.n = n
        self.max_len_lst = 16
        if self.len_lst != 0:
            self.procent = float(self.len_lst)/float(self.n)
        else:
            self.procent = 0
        if self.n == 0:
            self.good,self.bad = [],[]
        else:
            self.good,self.bad = self.genereate_points(min(self.n,self.max_len_lst),self.procent)
        pass

    def update(self,lst,n):
        """
        Update progress bar

        args:
            lst : Lst[int] - list of indexes of complited tasks
            n : int - number of all tasks
        """
        self.len_lst = len(lst)
        self.n = n
        self.max_len_lst = 16
        self.procent = float(self.n)/float(self.len_lst)
        if self.len_lst != 0:
            self.procent = float(self.len_lst)/float(self.n)
        else:
            self.procent = 0
        if self.len_lst == 0:
            self.good,self.bad = [],[]
        else:
            self.good,self.bad = self.genereate_points(min(self.n,self.max_len_lst),self.procent)
        pass

    def draw(self,win,color,v,weight):
        """
        Draw Crown

        args :
            win - window to draw
            color : Tuple[int,int,int] - color of element
            v : Tuple[int,int] - (x,y) middle of Node
        """
        w = weight+10
        for i in self.good:
            pg.draw.line(win,color,v,(i[0]*w+v[0] ,i[1]*w+v[1]))
            pg.draw.circle(win,color,(i[0]*w+v[0] ,i[1]*w+v[1]),4)
            pg.draw.circle(win,(0,255,0),(i[0]*w+v[0] ,i[1]*w+v[1]),3)
        for i in self.bad:
            pg.draw.line(win,color,v,(i[0]*w+v[0] ,i[1]*w+v[1]))
            pg.draw.circle(win,color,(i[0]*w+v[0] ,i[1]*w+v[1]),4)
            pg.draw.circle(win,(255,0,0),(i[0]*w+v[0] ,i[1]*w+v[1]),3)
        pass