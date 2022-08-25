from main_loop import *
import pickle
def save_Nodes(node_lst : List[Node]):
    """
    save nodes (pickle information to file)
    """
    with open("Nodes.bin", 'wb') as file:
        temp = {}
        for i in node_lst:
            temp[i.name_] = [i.name_,i.x_,i.y_,i.weight_,i.description,i.color,i.to_do_list,i.checked,[j.name_ for j in i.descendants]]#[j.name_ for j in i.ancestors],
        pickle.dump(temp,file)