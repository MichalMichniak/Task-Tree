import time
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
from map import *
import multiprocessing
import functools
import copy
WIDTH = 400
HEIGH = 400


    
def to_do_list_split(strr,node : Node,win,info_win,func,canv):
    """
    parse tasks list
    
    args :
        strr : str - string to parse
        node : Node - node of the edited tasks
        win :  - window to destroy after updating tasks
        info_win : - object of childs windows
        func : - function to refresh root window
        canv : - canva from root window to refresh content
    """
    lst = []#strr.split("*\n")
    s = ''
    for i in strr:
        if len(s)>0:
            if i == '*' and s[-1] == "\n":
                lst.append(s)
                s = ""
                continue
        s+=i
    if s != '':
        if s[-1] != "\n":
            s+="\n"
        lst.append(s)
    if len(lst)>0:
        if len(lst[0])>0:
            if lst[0][0] == '*':
                lst[0] = lst[0][1:]
    node.to_do_list = lst
    info_win.edit_mode = False
    func(canv)
    win.destroy()  

class Info_Windows:
    """
    Object of child windows
    """
    def __init__(self,node_lst : List[Node],node_lst_lock : multiprocessing.Lock,node_name):
        """
        Initialize values of new windows

        args :
            node_lst : List[Node] - list of actual nodes in program
            node_lst_lock : multiprocessing.Lock - lock for using list of nodes
            node_name : Tuple[int,int] - name of node
        """
        self.node_lst = node_lst
        self.node_lst_lock : multiprocessing.Lock = node_lst_lock
        self.node_name = node_name
        ### only one window can be open at a time
        self.edit_mode = False
        with self.node_lst_lock:
            self.node = self.node_lst[[i.name_ for i in self.node_lst].index(node_name)]

    def destroy(self,win : tk.Tk):
        """
        destroy window and set edit_mode to false
        """
        win.destroy()
        self.edit_mode = False

    def edit(self,func,canv):
        """
        Initialize a new edit tasks window

        args :
            func : - function to refresh root window
            canv : - canva from root window to refresh content after change
        """
        if not self.edit_mode:
            self.edit_mode = True
            edit = tk.Tk()
            def on_closing():
                self.edit_mode = False
                edit.destroy()
            edit.protocol("WM_DELETE_WINDOW", on_closing)
            frm = ttk.Frame(edit, padding=10)
            txt = tk.Text(edit, state='normal', width=80, height=24, wrap='none')
            ys = ttk.Scrollbar(edit, orient = 'vertical', command = txt.yview)
            xs = ttk.Scrollbar(edit, orient = 'horizontal', command = txt.xview)
            txt['yscrollcommand'] = ys.set
            txt['xscrollcommand'] = xs.set
            xs.grid(column = 0, row = 1, sticky = 'we')
            ys.grid(column = 1, row = 0, sticky = 'ns')
            edit.grid_columnconfigure(0, weight = 1)
            edit.grid_rowconfigure(0, weight = 1)

            txt.grid(column=0, row=0)
            strr = ""
            for i in self.node.to_do_list:
                strr += "*"+ i
            txt.insert('1.0', strr)
            #txt.insert('end', '\n')#self.node.description
            ttk.Button(frm, text="Cancel", command=lambda: self.destroy(edit)).grid(column=1, row=1)
            ttk.Button(frm, text="Ok", command=lambda: to_do_list_split(txt.get('1.0', 'end -1 chars'),self.node,edit,self,func,canv)).grid(column=2, row=1)
            frm.grid()
            edit.mainloop()
    
    def change_description(self,msg,win):
        """
        change a description of a node(string in Message_Box)
        """
        self.node.description = msg
        self.node.update_description()
        win.destroy()
        self.edit_mode = False


    def edit_description(self):
        """
        initialize window of editing description
        """
        if not self.edit_mode:
            self.edit_mode = True
            edit = tk.Tk()
            def on_closing():
                self.edit_mode = False
                edit.destroy()
            edit.protocol("WM_DELETE_WINDOW", on_closing)
            frm = ttk.Frame(edit, padding=10)
            txt = tk.Text(edit, state='normal', width=80, height=24, wrap='none')
            ys = ttk.Scrollbar(edit, orient = 'vertical', command = txt.yview)
            xs = ttk.Scrollbar(edit, orient = 'horizontal', command = txt.xview)
            txt['yscrollcommand'] = ys.set
            txt['xscrollcommand'] = xs.set
            xs.grid(column = 0, row = 1, sticky = 'we')
            ys.grid(column = 1, row = 0, sticky = 'ns')
            edit.grid_columnconfigure(0, weight = 1)
            edit.grid_rowconfigure(0, weight = 1)
            txt.grid(column=0, row=0)
            txt.insert('1.0', self.node.description)
            ttk.Button(frm, text="Cancel", command=lambda: self.destroy(edit)).grid(column=1, row=1)
            ttk.Button(frm, text="Ok", command=lambda: self.change_description(txt.get('1.0', 'end -1 chars'),edit)).grid(column=2, row=1)
            frm.grid()
            edit.mainloop()
    
    def del_parent_(self,lst : List[Node],win,func,canv):
        """
        delete parent of node

        args :
            lst : List[Node] - list of parents to delete
            win :  - window to destroy after updating parents
            func : - function to refresh root window
            canv : - canva from root window to refresh content
        ------------
        (could be with lock)
        """
        for i in lst:
            try:
                i.descendants.remove(self.node)
                self.node.ancestors.remove(i)
            except:
                pass
            pass
        self.edit_mode = False
        func(canv)
        win.destroy()
    
    def add_to_del(self, lst : List[Node], i: Node):
        """

        args :
            lst : List[Node] - list of parents to delete
            i : Node - added node to delete list(of parents)
        """
        if i not in lst:
            lst.append(i)
        else:
            lst.remove(i)

    def del_parent(self,func = lambda x: None, canv = 0):
        """
        initialize window to delete parent of node

        args :
            func : - function to refresh root window
            canv : - canva from root window to refresh content
        """
        if not self.edit_mode:
            self.edit_mode = True
            edit = tk.Tk()
            def on_closing():
                self.edit_mode = False
                edit.destroy()
            edit.protocol("WM_DELETE_WINDOW", on_closing)
            frm = ttk.Frame(edit, padding=10)
            frm.grid()
            lst_del_parents = []

            #ttk.Label(frm, text=self.node_name).grid(column=0, row=0)
            fram = tk.Frame(edit)
            canvas_container=tk.Canvas(fram, height=300,width=150)
            
            frame2=tk.Frame(canvas_container)
            myscrollbar=tk.Scrollbar(fram,orient="vertical",command=canvas_container.yview) # will be visible if the frame2 is to to big for the canvas
            canvas_container.create_window((0,0),window=frame2,anchor='nw')
            canvas_container.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())
            with self.node_lst_lock:
                for i in self.node.ancestors:
                    button = tk.Checkbutton(frame2,text=i.name_,command=functools.partial(self.add_to_del,lst_del_parents,i))
                    button.pack(side=tk.TOP, anchor=tk.W)
                    #button.select()
            frame2.update()
            canvas_container.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())
            canvas_container.pack(side=tk.LEFT)
            myscrollbar.pack(side=tk.RIGHT, fill = tk.Y)
            
            fram.grid(column=3, row=0)
            ttk.Button(frm, text="Ok", command=lambda:self.del_parent_(lst_del_parents,edit,func,canv)).grid(column=1, row=3)
            ttk.Button(frm, text="Cancel", command=lambda: self.destroy(edit)).grid(column=1, row=4)
            edit.mainloop()

    def add_to_add(self, lst : List[Node], name):
        """
        adding or removing new parent from list to add

        args :
            lst : List[Node] - list of parents to add
            name : str - parent name that is changed
        """
        if name not in lst:
            lst.append(name)
        else:
            lst.remove(name)
        

    def add_parent_(self,lst : List[Node],win,func,canv):
        """
        adding new parents to the node

        args :
            lst : List[Node] - list of parents to add
            win :  - window to destroy after updating parents
            func : - function to refresh root window
            canv : - canva from root window to refresh content
        -----------
        (could be with lock)
        """
        with self.node_lst_lock:
            for i in lst:
                try:
                    if i in [j.name_ for j in self.node_lst]:
                        next(filter(lambda x: x.name_ == i, self.node_lst)).add_descendant(self.node)
                except:
                    pass
                pass
        self.edit_mode = False
        func(canv)
        win.destroy()

    def add_parent(self,func = lambda x: None, canv = 0):
        """
        Initialization of new window to add new parents of node

        args :
            func : - function to refresh root window
            canv : - canva from root window to refresh content
        -----------
        (could be with lock)
        """
        if not self.edit_mode:
            self.edit_mode = True
            edit = tk.Tk()
            def on_closing():
                self.edit_mode = False
                edit.destroy()
            edit.protocol("WM_DELETE_WINDOW", on_closing)
            frm = ttk.Frame(edit, padding=10)
            frm.grid()
            lst_add_parents = []

            #ttk.Label(frm, text=self.node_name).grid(column=0, row=0)
            fram = tk.Frame(edit)
            canvas_container=tk.Canvas(fram, height=300,width=150)
            
            frame2=tk.Frame(canvas_container)
            myscrollbar=tk.Scrollbar(fram,orient="vertical",command=canvas_container.yview) # will be visible if the frame2 is to to big for the canvas
            canvas_container.create_window((0,0),window=frame2,anchor='nw')
            canvas_container.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())
            lst_temp = [i.name_ for i in self.node_lst]
            with self.node_lst_lock:
                desc_lst = [i.name_ for i in self.node.ancestors]
                desc_lst.append(self.node.name_)
                for i in lst_temp:
                    if i not in desc_lst:
                        button = tk.Checkbutton(frame2,text=i,command=functools.partial(self.add_to_add,lst_add_parents,i))
                        button.pack(side=tk.TOP, anchor=tk.W)

                    #button.select()
            frame2.update()
            canvas_container.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())
            canvas_container.pack(side=tk.LEFT)
            myscrollbar.pack(side=tk.RIGHT, fill = tk.Y)
            
            fram.grid(column=3, row=0)
            ttk.Button(frm, text="Ok", command=lambda:self.add_parent_(lst_add_parents,edit,func,canv)).grid(column=1, row=3)
            ttk.Button(frm, text="Cancel", command=lambda: self.destroy(edit)).grid(column=1, row=4)
            edit.mainloop()

class Root_window:
    """
    Objectof root window
    """
    def __init__(self,node_lst,node_lst_lock,node_name):
        """
        Initialize values of root window

        args :
            node_lst : List[Node] - list of actual nodes in program
            node_lst_lock : multiprocessing.Lock - lock for using list of nodes
            node_name : Tuple[int,int] - name of node
        """
        self.node_lst = node_lst
        self.node_lst_lock = node_lst_lock
        self.node_name = node_name
    
    def func(self,name):
        """
        function that adding complited tasks information to node
        """
        if name not in self.info.node.checked:
            self.info.node.checked.append(name)
        else:
            self.info.node.checked.remove(name)
        self.info.node.update_crown()

    def reload_checkbox_frame(self,canva : tk.Frame):
        """
        reload checkbox frame
        args : 
            canva : tk.Frame - canva to reload
        """
        for widget in canva.winfo_children():
            widget.destroy()
        mylist = self.info.node.to_do_list
        for n,i in list(enumerate(self.info.node.checked))[::-1]:
            if i not in mylist:
                #print(i)
                self.info.node.checked.pop(n)

        for item in mylist:
            button = tk.Checkbutton(canva,text=item[:-1],command=functools.partial(self.func,item))
            button.pack(side=tk.TOP, anchor=tk.W)
            if item in self.info.node.checked:
                button.select()
        canva.update()
        self.canvas_container.configure(yscrollcommand=self.myscrollbar.set, scrollregion="0 0 0 %s" % canva.winfo_height())
        self.canvas_container.pack(side=tk.LEFT)
        self.info.node.update_crown()
        pass
    
    def edit(self,info,canva):
        """
        Make new edit window
        """
        info.edit(self.reload_checkbox_frame,canva)
        pass

    def delete_node(self):
        """
        deleting node and removing every relation connected it also destroy root window
        """
        msg = messagebox.askokcancel(title="Delete Node", message="Do you want to delete the node?")
        if msg:
            with self.node_lst_lock:
                for i in self.info.node.ancestors:
                    try:
                        i.descendants.remove(self.info.node)
                    except:
                        pass
                for i in self.info.node.descendants:
                    try:
                        i.ancestors.remove(self.info.node)
                    except:
                        pass
                self.info.node.ancestors = []
                self.info.node.descendants = []
                try:
                    self.node_lst.remove(next(filter(lambda x: x.name_ == self.info.node.name_, self.node_lst)))
                except:
                    pass
            self.root.destroy()
        pass

    def run(self):
        """
        initialize root window
        """
        self.root = tk.Tk()
        self.info = Info_Windows(self.node_lst,self.node_lst_lock,self.node_name)
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()
        ttk.Label(frm, text=self.node_name).grid(column=0, row=0)
        fram = tk.Frame(self.root)

        self.canvas_container=tk.Canvas(fram, height=300,width=460)

        frame2=tk.Frame(self.canvas_container)
        ###
        
        ###  
        self.myscrollbar=tk.Scrollbar(fram,orient="vertical",command=self.canvas_container.yview)
        self.canvas_container.create_window((0,0),window=frame2,anchor='nw')
        self.canvas_container.configure(yscrollcommand=self.myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())
        self.reload_checkbox_frame(frame2)
        frame2.update()
        self.canvas_container.configure(yscrollcommand=self.myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())
        self.canvas_container.pack(side=tk.LEFT)
        self.myscrollbar.pack(side=tk.RIGHT, fill = tk.Y)
        
        ###


        fram.grid(column=0, row=1)
        ttk.Button(frm, text="Quit", command=self.root.destroy).grid(column=4, row=2)
        ttk.Button(frm, text="Edit", command=lambda: self.edit(self.info,frame2)).grid(column=2, row=2)
        ttk.Button(frm, text="Edit Description", command=self.info.edit_description).grid(column=3, row=2)
        ttk.Button(frm, text="Add parent", command=self.info.add_parent).grid(column=0, row=2)
        ttk.Button(frm, text="Del parent", command=self.info.del_parent).grid(column=1, row=2)
        ttk.Button(frm, text="Delete Node", command=self.delete_node).grid(column=5, row=2)
        self.root.mainloop()




def info_window(node_lst,node_lst_lock : multiprocessing.Lock,node_name):
    """
    function that handle node edition and its windows

    args :
        node_lst : List[Node] - list of actual nodes in program
        node_lst_lock : multiprocessing.Lock - lock for using list of nodes
        node_name : Tuple[int,int] - name of node
    """
    root = Root_window(node_lst,node_lst_lock,node_name)
    root.run()
    return node_name


