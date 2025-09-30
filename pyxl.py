from tkinter import *
from tkinter import ttk

from random import randrange


class PyxlCursor:
    
    def __init__(self, x=0, y=0, weight=2):
        self.x = x
        self.y = y
        self.weight = weight

    def draw(self, context, p_size):
        w = self.weight
        x1 = self.x * p_size
        y1 = self.y * p_size
        x2 = x1 + p_size
        y2 = y1 + p_size
        context.create_rectangle(x1+w, y1+w, x2-w, y2-w, fill="", outline="#000000", width=self.weight)


class PyxlCanvas:
    
    def __init__(self, parent, width, height, bg=0x000000):
        self.img = [[randrange(0x0, 0xffffff) for _ in range(width)] for _ in range(height)]
        self.imgw = width
        self.imgh = height
        self.px = 16
        self.width = width * self.px
        self.height = height * self.px
        self.cursor = PyxlCursor()
        self.bg = bg
        
        self.outer = Frame(parent, width=self.width, height=self.height, bg=self.htc(bg))
        self.outer.pack(expand=True, fill=BOTH)

        self.canvas = Canvas(self.outer, width=self.width, height=self.height, bg=self.htc(bg), scrollregion=(0,0,self.width,self.height))

        hbar = Scrollbar(self.outer, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=self.canvas.xview)

        vbar = Scrollbar(self.outer, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)

        self.canvas.config(width=self.width, height=self.height)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(expand=True, fill=BOTH)

        self.draw()
    
    def htc(self, h):
        s = hex(h)[2:]
        s = ("0" * (6 - len(s))) + s
        return "#" + s

    def draw_one_pixel(self, x, y, color):
        x1 = x * self.px
        y1 = y * self.px
        x2 = x1 + self.px
        y2 = y1 + self.px
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)
        
    def draw(self):
        for i, row in enumerate(self.img):
            for j, col in enumerate(row):
                self.draw_one_pixel(j, i, self.htc(col))
        
        self.cursor.draw(self.canvas, self.px)

    def clear(self):
        for i, row in enumerate(self.img):
            for j, col in enumerate(row):
                self.draw_one_pixel(j, i, self.htc(self.bg))

    def resize(self):
        self.width = self.imgw * self.px
        self.height = self.imgh * self.px

        self.outer.config(width=self.width, height=self.height)
        self.canvas.config(width=self.width, height=self.height, scrollregion=(0,0,self.width,self.height))

    def on_zoom_in(self, event):
        self.clear()
        self.px += 1
        self.resize()
        self.draw()

    def on_zoom_out(self, event):
        self.clear()
        self.px = max(self.px - 1, 1)
        self.resize()
        self.draw()

    def on_draw(self, event):
        pass

    def on_erase(self, event):
        self.draw_one_pixel(self.cursor.x, self.cursor.y, self.htc(self.bg))
        self.img[self.cursor.y][self.cursor.x] = self.bg

    def clear_cursor(self):
        self.draw_one_pixel(self.cursor.x, self.cursor.y, self.htc(self.img[self.cursor.y][self.cursor.x]))

    def on_cursor_left(self, event):
        self.clear_cursor()
        self.cursor.x = max(self.cursor.x - 1, 0)
        self.cursor.draw(self.canvas, self.px)

    def on_cursor_right(self, event):
        self.clear_cursor()
        self.cursor.x = min(self.cursor.x + 1, self.imgw)
        self.cursor.draw(self.canvas, self.px)

    def on_cursor_up(self, event):
        self.clear_cursor()
        self.cursor.y = max(self.cursor.y - 1, 0)
        self.cursor.draw(self.canvas, self.px)

    def on_cursor_down(self, event):
        self.clear_cursor()
        self.cursor.y = min(self.cursor.y + 1, self.imgh)
        self.cursor.draw(self.canvas, self.px)
        

"""
Binds each key in keys to the same callback function
"""
def meta_bind(r, keys, callback):
    for k in keys:
        r.bind(k, callback)


def main():
    root = Tk()

    t = Frame(root, bg="#ffffff")
    c = PyxlCanvas(root, 32, 32)
    
    root.bind("i", c.on_zoom_in)
    root.bind("o", c.on_zoom_out)
    root.bind("d", c.on_draw)
    root.bind("e", c.on_erase)

    meta_bind(root, ("h", "<Left>"), c.on_cursor_left)
    meta_bind(root, ("j", "<Down>"), c.on_cursor_down)
    meta_bind(root, ("k", "<Up>"), c.on_cursor_up)
    meta_bind(root, ("l", "<Right>"), c.on_cursor_right)

    root.mainloop()


if __name__ == "__main__":
    main()
