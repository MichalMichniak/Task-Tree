import pygame as pg
from typing import List
from Crown import Crown
from Message_Box import *

POINTED_AT_COLOR = (0,255,0)

class Node:
    """
    Node class - representation of subject
    """
    def __init__(self,x,y, name="No name",weight = 30, desription = ""):
        """
        Initialization of node

        args :
            x : int - x coordinate of node
            y : int - y coordinate of node
            name : str - name of the node
            weight : int - radius of node
            description : str - description
        """
        self.description = desription
        ### initialization of message box
        self.message_box : Message_Box = Message_Box(name, self.description)

        self.x_ = x
        self.y_ = y
        self.next_x = x
        self.next_y = y
        self.color = (255,255,255)
        self.weight_ = weight
        self.ancestors : List[Node] = []
        self.descendants : List[Node] = []
        font_size = 16 if (k:=int(round(self.weight_* 0.7)*2/int((1+len(name))*1.1))*4)<15 else k
        if font_size > 28 :
            font_size = 28
        font = pg.font.SysFont(None, font_size)
        text_width, text_height = font.size(name)
        self.name_x_shift = text_width/2
        self.name_y_shift = text_height/2
        self.name_ = name
        ### for checkboxes
        self.to_do_list = []
        self.checked = []
        ### 
        self.render_name = font.render(name, True, (80,50,200))
        ### for eventual DFS or BFS
        self.mark = False
        ### crown
        self.crown = Crown(self.checked,len(self.to_do_list))
        pass
    
    def set_coords(self,x,y):
        self.x_ = x
        self.y_ = y
    
    def update_description(self):
        self.message_box.update_description(self.description)
        pass
    
    def update_crown(self):
        self.crown = Crown(self.checked,len(self.to_do_list))
        pass

    def draw(self,win,ref_x,ref_y,pointed_at = False):
        """
        draw node

        args :
            win : - okno do wyświetlenia
            ref_x : int - x coordinate of shift vector
            ref_y : int - y coordinate of shift vector
        """
        self.crown.draw(win,self.color,(self.x_ - ref_x,self.y_ - ref_y),self.weight_)
        if pointed_at:
            pg.draw.circle(win,POINTED_AT_COLOR,(self.x_ - ref_x,self.y_ - ref_y),self.weight_)
            pg.draw.circle(win,self.color,(self.x_ - ref_x,self.y_ - ref_y),self.weight_-2)
        else:
            pg.draw.circle(win,self.color,(self.x_ - ref_x,self.y_ - ref_y),self.weight_)
            
        pg.draw.rect(win,self.color,(self.x_ - ref_x - self.name_x_shift,self.y_ - ref_y- self.name_y_shift,self.name_x_shift*2,self.name_y_shift*2))
        win.blit(self.render_name, (self.x_ - ref_x - self.name_x_shift ,self.y_ - ref_y - self.name_y_shift))

    def get_radius(self):
        return self.weight_

    def move(self,dx,dy):
        self.x_ += dx
        self.y_ += dy

    def add_descendant(self,node):
        self.descendants.append(node)
        node.add_ancestor(self)

    def add_ancestor(self,node):
        self.ancestors.append(node)