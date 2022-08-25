from main_loop import *
import pickle
from typing import Dict
def read_from_file():
    """
    unpickle information from binary file
    """
    temp = 0
    with open("Nodes.bin", 'rb') as file:
        # temp = {}
        # for i in node_lst:
        #     temp[i.name_] = [i.name_,i.x_,i.y_,i.weight_,i.description,i.color,i.to_do_list,i.checked,[j.name_ for j in i.descendants]]
        temp : Dict[List]= pickle.load(file)
    nodes_lst : List[Node] = []
    for i in temp.keys():
        node = temp[i]
        nodes_lst.append(Node(node[1],node[2],i,node[3],node[4]))
        nodes_lst[-1].color =  node[5]
        nodes_lst[-1].to_do_list = node[6]
        nodes_lst[-1].checked = node[7]
        nodes_lst[-1].update_crown()
    t = list(temp.keys())
    for n,i in enumerate(temp.keys()):
        node = temp[i]
        for j in node[8]:
            nodes_lst[n].add_descendant(nodes_lst[t.index(j)])
    return nodes_lst

if __name__ == "__main__":
    pg.init()
    y = read_from_file()
    i = 0