from main_loop import *
from read_from_file import *

def main():
    pg.init()
    node_lst = read_from_file()
    main_loop(node_lst)
    pass


if __name__ == '__main__':
    main()