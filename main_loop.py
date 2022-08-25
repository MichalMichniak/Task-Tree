from copy import copy
from map import *
import threading
import multiprocessing
from info_window import info_window
from Create_Window import create
import save
class thread_bind:
    """
    edit node thread structure
    """
    def __init__(self,name,target,args):
        self.thread : threading.Thread = threading.Thread(target=target,args=args)
        self.name_ = name
    
    def start(self):
        self.thread.start()
    
    def is_alive(self):
        return self.thread.is_alive()

    def join(self):
        self.thread.join()
        return self.name_


def main_loop(node_lst):
    """
    main loop of program. Statrts asynhronius tasks menage them.

    args :
        node_lst : List[Node] - list of actual nodes in program     
    """
    lst_thread = []
    map_pipe, map_main_pipe = multiprocessing.Pipe()
    node_lst_lock = threading.Lock()
    map_thread = threading.Thread(target=map_window_func,args=[node_lst,node_lst_lock,map_pipe])
    map_thread.start()
    node_name_lst = []
    create_lst = []
    while map_thread.is_alive():
        try:
            txt = map_main_pipe.recv()
            if len(txt) == 2:
                if txt[1] == "info_window":
                    node_lst_lock.acquire()
                    try:
                        name = node_lst[txt[0]].name_
                    except:
                        node_lst_lock.release()
                        continue
                    if name in node_name_lst:
                        node_lst_lock.release()
                        continue
                    else:
                        node_name_lst.append(name)
                    node_lst_lock.release()
                    lst_thread.append(thread_bind(name,target=info_window,args=[node_lst,node_lst_lock,name]))
                    lst_thread[-1].start()
                if txt[1] == "create_window":
                    create_lst.append(threading.Thread(target=create, args=[node_lst,node_lst_lock,copy(txt[0])]))
                    create_lst[-1].start()
                    
                    pass
        except EOFError:
            pass
        lst = []
        for n,i in enumerate(lst_thread):
            if not i.is_alive():
                lst.append(n)
                name_from_thread = i.join()
                node_name_lst.pop(node_name_lst.index(name_from_thread))
        for i in lst[::-1]:
            lst_thread.pop(i)
        pass
    map_main_pipe.close()
    map_thread.join()
    save.save_Nodes(node_lst)