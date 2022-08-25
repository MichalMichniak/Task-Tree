import pygame as pg


class Message_Box:
    """
    Message_Box class (box with the description of the node after moving mouse above the node)
    """
    def __init__(self, title, txt , title_color = (0,0,20), txt_color = (0,0,40), title_line_color = (0,0,0,10), background_color = (255,255,255)):
        """
        initialization and precomputing values of message box

        args :
            title : str - name of the node
            txt : str - description of the node
            title_color : Tuple[ini,int,int] - color of title
            txt_color : Tuple[ini,int,int] - color of description
            title_line_color : Tuple[ini,int,int] - color of line between title and description
            background_color : Tuple[ini,int,int] - background color
        """
        self.title_ = title
        self.txt_color = txt_color
        self.txt_ = txt.split("\n")
        self.font = pg.font.SysFont(None, 24)
        self.font_txt = pg.font.SysFont(None, 18)
        self.title_line_color = title_line_color
        self.txt_y_size = 0
        self.txt_x_size = 0
        self.background_color = background_color
        self.title_size = self.font.size(self.title_)
        for i in self.txt_:
            text_width, text_height = self.font_txt.size(i)
            self.txt_y_size += text_height+1
            self.txt_x_size = max(self.txt_x_size,text_width)
        self.title_rendered =  self.font.render(self.title_, True, title_color)
        self.txt_rendered = []
        for i in self.txt_:
            self.txt_rendered.append(self.font_txt.render(i, True, txt_color))
        self.width_ = 6 + max(self.txt_x_size,self.title_size[0])
        self.heigh_ = 6 + self.title_size[1] + 3 + self.txt_y_size
    
    def update_description(self,txt):
        """
        update description

        args :
            txt : str - new description of the node
        """
        self.txt_ = txt.split("\n")
        self.txt_y_size = 0
        self.txt_x_size = 0
        for i in self.txt_:
            text_width, text_height = self.font_txt.size(i)
            self.txt_y_size += text_height+1
            self.txt_x_size = max(self.txt_x_size,text_width)
        self.txt_rendered = []
        for i in self.txt_:
            self.txt_rendered.append(self.font_txt.render(i, True, self.txt_color))
        self.width_ = 6 + max(self.txt_x_size,self.title_size[0])
        self.heigh_ = 6 + self.title_size[1] + 3 + self.txt_y_size
        pass

    def draw_title(self,win : pg.display,x,y):
        """
        display MessageBox with only title

        args :
            win : - okno do wyświetlenia
            x : int - x coordinate of top left corner of window
            y : int - y coordinate of top left corner of window
        """
        pg.draw.rect(win,self.background_color, (x,y,self.title_size[0]+6,self.title_size[1]+6))
        for i in [[(x,y),(x+self.title_size[0]+6,y)],
        [(x+self.title_size[0]+6,y),(x+self.title_size[0]+6,y+self.title_size[1]+6)],
        [(x,y+self.title_size[1]+6),(x+self.title_size[0]+6,y+self.title_size[1]+6)],
        [(x,y),(x,y+self.title_size[1]+6)]
        ]:
            pg.draw.line(win,(0,0,0),i[0],i[1])
        win.blit(self.title_rendered , (x + 3,y + 3))
        pass

    def draw_title_with_txt(self,win : pg.display,x,y):
        """
        display MessageBox with title and description

        args :
            win : - okno do wyświetlenia
            x : int - x coordinate of top left corner of window
            y : int - y coordinate of top left corner of window
        """
        pg.draw.rect(win,self.background_color, (x,y,self.width_,self.heigh_))
        win.blit(self.title_rendered , (x + 3,y + 3))
        pg.draw.line(win,self.title_line_color,(x + 2, y + 4 + self.title_size[1]) , (x + self.width_ - 2, y + 4 + self.title_size[1]))
        y_temp = y + 5 + self.title_size[1]
        for n,i in enumerate(self.txt_rendered):
            win.blit(i , (x + 3,y_temp))
            y_temp += self.font_txt.size(self.txt_[n])[1]
        for i in [[(x,y),(x+self.width_,y)],
        [(x+self.width_,y),(x+self.width_,y+self.heigh_)],
        [(x,y+self.heigh_),(x+self.width_,y+self.heigh_)],
        [(x,y),(x,y+self.heigh_)]
        ]:
            pg.draw.line(win,(0,0,0),i[0],i[1])
        pass


    def draw(self,win : pg.display,x,y):
        """
        display MessageBox

        args :
            win : - okno do wyświetlenia
            x : int - x coordinate of top left corner of window
            y : int - y coordinate of top left corner of window
        """
        if len(self.txt_) == 1 and self.txt_[0] == "":
            self.draw_title(win,x,y)
        else:
            self.draw_title_with_txt(win,x,y)
    