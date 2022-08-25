import time
import tkinter as tk
import tkinter.ttk as ttk
from map import *
import multiprocessing
import functools
import copy

class Create_Window:
    """
    Add new element window
    """
    def __init__(self,node_lst,node_lst_lock,v):
        """
        Initialize values of new window
        args :
            node_lst : List[Node] - list of actual nodes in program
            node_lst_lock : multiprocessing.Lock - lock for using list of nodes
            v : Tuple[int,int] - coordinates of new element
        """
        self.node_lst = node_lst
        self.node_lst_lock = node_lst_lock
        self.v_ = v
        pass

    def create_object(self):
        """
        Asynhronius adding new Node to list of nodes
        """
        strr = self.text.get()
        if strr == "":
            return
        while strr[0] == " ":
            strr = strr[1:]
            if len(strr) == 0:
                return
        node = Node(self.v_[0],self.v_[1],strr)
        with self.node_lst_lock:
            self.node_lst.append(node)
            sorted(self.node_lst,key=lambda x: x.name_)
        self.root.destroy()
        pass

    def run(self):
        """
        Initialize and run window
        """
        self.root = tk.Tk()
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()
        self.text = tk.StringVar()
        name = ttk.Entry(self.root, textvariable=self.text)
        name.grid(column=0, row=1)
        ttk.Button(frm, text="Ok", command=self.create_object).grid(column=0, row=3)
        ttk.Button(frm, text="Canel", command=self.root.destroy).grid(column=1, row=3)
        self.root.mainloop()
        pass



def create(node_lst,node_lst_lock : multiprocessing.Lock,v):
    root = Create_Window(node_lst,node_lst_lock,v)
    root.run()