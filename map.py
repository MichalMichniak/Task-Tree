from enum import Enum
from platform import node
from typing import List
import pygame as pg
import numpy as np
from Node import Node
import threading

WIDTH = 1200
HEIGH = 600

class Screen_Mode(Enum):
    """
    avaliable screen modes of map
    """
    default = 1
    edit = 2
    organizing = 3

def map_window_func(node_lst : List[Node],node_lst_lock : threading.Lock,pipe_to_main):
    """
    Initialize and menage pygame window

    args :
        node_lst : List[Node] - list of actual nodes in program
        node_lst_lock : multiprocessing.Lock - lock for using list of nodes
        pipe_to_main : Pipe - simplex pipe to request new tasks to mainloop
    """
    pg.display.set_caption("game")
    font = pg.font.SysFont(None, 24)
    win = pg.display.set_mode((WIDTH, HEIGH))
    edit_txt = font.render('Edit Mode', True, (0,255,0))
    organizing_txt = font.render('Organizing Mode', True, (0,255,0))
    run = True
    ref_x = -WIDTH/2
    ref_y = -HEIGH/2
    screen_mode = Screen_Mode.default
    screen_follow = False
    obj_follow = False
    prev_mouse_pos = (0,0)
    dragged_obj_nr = None
    Force_x2 = 6000000
    Force_x = 1
    arrow_m = 3
    default_mouse_left = False
    while run:
        node_lst_lock.acquire()
        win.fill((0,0,0))
        ##### event section #####
        ##### 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_e:
                    if screen_mode == Screen_Mode.edit:
                        screen_mode = Screen_Mode.default
                        obj_follow = False
                        dragged_obj_nr = None
                    elif screen_mode == Screen_Mode.default:
                        screen_mode = Screen_Mode.edit
                if event.key == pg.K_o:
                    if screen_mode == Screen_Mode.organizing:
                        screen_mode = Screen_Mode.default
                    elif screen_mode == Screen_Mode.default:
                        screen_mode = Screen_Mode.organizing
                        pass
                if event.key == pg.K_c:
                    pipe_to_main.send([None])
                    mouse = pg.mouse.get_pos()
                    pipe_to_main.send([(mouse[0] + ref_x,mouse[1] + ref_y),"create_window"])


            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 2:
                    screen_follow = True
                    prev_mouse_pos = pg.mouse.get_pos()
                #### edit mode events ####
                if screen_mode == Screen_Mode.edit:
                    if event.button == 1:
                        obj_follow = True
                        prev_mouse_pos = pg.mouse.get_pos()
                        for i in range(len(node_lst)):
                            if node_lst[i].get_radius() >= np.sqrt((prev_mouse_pos[0]+ref_x - node_lst[i].x_)**2+(prev_mouse_pos[1]+ref_y - node_lst[i].y_)**2):
                                dragged_obj_nr = i
                                break
                if screen_mode == Screen_Mode.default or screen_mode == Screen_Mode.organizing:
                    if event.button == 1:
                        default_mouse_left = True
                            
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 2:
                    screen_follow = False
                if screen_mode == Screen_Mode.edit:
                    if event.button == 1:
                        obj_follow = False
                        dragged_obj_nr = None
        ###### computing section #####
        mouse_pos = pg.mouse.get_pos()
        if screen_follow:
            temp = mouse_pos
            ref_x += prev_mouse_pos[0] - temp[0]
            ref_y += prev_mouse_pos[1] - temp[1]
            prev_mouse_pos = temp
        if obj_follow:
            if dragged_obj_nr != None:
                node_lst[dragged_obj_nr].move(mouse_pos[0]-prev_mouse_pos[0],mouse_pos[1]-prev_mouse_pos[1])
                prev_mouse_pos = mouse_pos
        if screen_mode == Screen_Mode.organizing:
            for n, i in enumerate(node_lst):
                Dx = 0
                Dy = 0

                dx = i.x_-node_lst[0].x_
                dy = i.y_-node_lst[0].y_
                z = np.sqrt(dy**2 + dx**2)
                if z>0:
                    Dx -= (t*(np.sign(dx)*abs(dx+10)/z) if (t:=np.log(z))>1 else 0) * len(node_lst)
                    Dy -= (t*(np.sign(dy)*abs(dy+10)/z) if (t:=np.log(z))>1 else 0) * len(node_lst)


                for j in node_lst:
                    dx = i.x_-j.x_
                    dy = i.y_-j.y_
                    if dx == 0 and dy == 0:
                        continue
                    z = np.sqrt(dy**2 + dx**2)
                    Dx += Force_x2*dx/(z**3)# - (t*dx/z if (t:=np.log(z))>0 else 0)
                    Dy += Force_x2*dy/(z**3)# - (t*dy/z if (t:=np.log(z))>0 else 0)
                for j in i.ancestors:
                    dx = i.x_-j.x_
                    dy = i.y_-j.y_
                    if dx == 0 and dy == 0:
                        continue
                    #z = np.sqrt(dy**2 + dx**2)
                    z_x = abs(dx) #if abs(dx) < 10000 else 10000
                    z_y = abs(dy) #if abs(dy) < 10000 else 10000
                    Dx += -Force_x*np.sign(dx)*z_x
                    Dy += -Force_x*np.sign(dy)*z_y
                for j in i.descendants:
                    dx = i.x_-j.x_
                    dy = i.y_-j.y_
                    if dx == 0 and dy == 0:
                        continue
                    z = np.sqrt(dy**2 + dx**2)
                    Dx -= Force_x2*dx/(z**3)# - (t*dx/z if (t:=np.log(z))>0 else 0)
                    Dy -= Force_x2*dy/(z**3)# - (t*dy/z if (t:=np.log(z))>0 else 0)

                g = np.log(len(node_lst))
                if abs(Dx) > 5/g or abs(Dy) > 5/g:
                    Dx = np.sign(Dx) * 5/g
                    Dy = np.sign(Dy) * 5/g
                
                node_lst[n].next_x = i.x_ + Dx
                node_lst[n].next_y = i.y_ + Dy

            for n,i in enumerate(node_lst[2:]):
                node_lst[n+2].x_ = i.next_x
                node_lst[n+2].y_ = i.next_y
        ###### display objects section #####
        temp = None
        if screen_mode == Screen_Mode.default or screen_mode == Screen_Mode.organizing:
            for i in range(len(node_lst)):
                if node_lst[i].get_radius() >= np.sqrt((mouse_pos[0]+ref_x - node_lst[i].x_)**2+(mouse_pos[1]+ref_y - node_lst[i].y_)**2):
                    temp = i
                    break
        
        if screen_mode == Screen_Mode.edit:
            win.blit(edit_txt, (WIDTH-180,10))
        elif screen_mode == Screen_Mode.organizing:
            win.blit(organizing_txt, (WIDTH-180,10))
        for n,i in enumerate(node_lst):
            for j in i.descendants:
                pg.draw.line(win,(255,255,255),(i.x_-ref_x,i.y_-ref_y),(j.x_-ref_x,j.y_-ref_y))
                dx = i.x_-j.x_
                dy = i.y_-j.y_
                z = np.sqrt((dx)**2 + (dy)**2)
                if z < 11:
                    continue
                start_point_x = j.x_ + i.weight_*dx/z -ref_x
                start_point_y = j.y_+i.weight_*dy/z -ref_y
                middle_point_x =j.x_ + (i.weight_ + 10)*dx/z -ref_x
                middle_point_y = j.y_+(i.weight_ + 10)*dy/z -ref_y
                start = (start_point_x,start_point_y)
                if dy != 0:
                    tan = -dx/dy
                    cos = 1/(np.sqrt(1+tan**2))
                    x = arrow_m*cos
                    upper = (middle_point_x+x,middle_point_y+x*tan)
                    lower = (middle_point_x-x,middle_point_y-x*tan)
                    pg.draw.line(win,(255,255,255),start,upper)
                    pg.draw.line(win,(255,255,255),start,lower)
                else:
                    upper = (middle_point_x+arrow_m,middle_point_y)
                    lower = (middle_point_x-arrow_m,middle_point_y)
                    pg.draw.line(win,(255,255,255),start,upper)
                    pg.draw.line(win,(255,255,255),start,lower)
                
        for n,i in enumerate(node_lst):
            if temp == n:
                i.draw(win,ref_x,ref_y,True)
                pass
            else:
                i.draw(win,ref_x,ref_y)
        
        if screen_mode == Screen_Mode.default or screen_mode == Screen_Mode.organizing:
            if temp != None:
                node_lst[temp].message_box.draw(win, mouse_pos[0] + 8,mouse_pos[1] + 8)
                if default_mouse_left:
                    pipe_to_main.send([None])
                    pipe_to_main.send([temp,"info_window"])
            pass   
        node_lst_lock.release()
        default_mouse_left = False
        pg.display.update()
        #### delays #####
        if screen_mode == Screen_Mode.edit:
            pg.time.delay(10)
        else:
            pg.time.delay(40)
    pipe_to_main.close()
    pass
