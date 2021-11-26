import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
from tkinter.constants import N


win = tk.Tk()
win.config(bg='white')
win.title("Voronoi Diagram")
win.geometry("800x650")

start_x, start_y, x, y, curX, curY = 0, 0, 0, 0, 0, 0
ReadData = []
NumData = 0
PointList = []
EdgeList = []


class Edge():
    def __init__(self, x, y, a, b):
        if x < a:
            self.x, self.y, self.a, self.b = x, y, a, b
        elif a < x:
            self.x, self.y, self.a, self.b = a, b, x, y
        elif y < b:
            self.x, self.y, self.a, self.b = x, y, a, b
        elif b < y:
            self.x, self.y, self.a, self.b = a, b, x, y
        else:
            self.x, self.y, self.a, self.b = x, y, a, b

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MathEx():
    def __init__(self):
        pass
    def GetCircumcenter(p1, p2, p3):
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y

        c1 = (x1*x1 + y1*y1) * (y2 - y3) + (x2*x2 + y2*y2) * (y3 - y1) + (x3*x3 + y3*y3) * (y1 - y2)
        c2 = (x1*x1 + y1*y1) * (x3 - x2) + (x2*x2 + y2*y2) * (x1 - x3) + (x3*x3 + y3*y3) * (x2 - x1)
        c3 = ((y2 - y3) * x1 + (y3 - y1) * x2 + (y1 - y2) * x3) * 2
        if c3 == 0:
            return False
        x = c1 / c3
        y = c2 / c3
        return Point(x, y)

    def medLine(p1,p2):
        k = -(p1.x-p2.x)/(p1.y-p2.y)
        x = (p1.x+p2.x)/2
        y = (p1.y+p2.y)/2
        a1 = Point((-y+k*x) / k, 0)
        a2 = Point((600-y+k*x) / k, 600)
        return a1,a2

    def CalcVactor(p1,p2):
        return Point(p2.x-p1.x, p2.y-p1.y)

    def CalcNormal(p):
        return Point(-p.y,p.x)

    def crossProduct(p1,p2,p):
        return (p2.x - p1.x) * (p.y - p1.y) - (p.x - p1.x) * (p2.y - p1.y)

    def GetMidPoint(p1,p2):
        return Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)

def SortPoint(p):
    return p.x*2+p.y

def SortEdge(n):
    return n.x*4+n.y*3+n.a*2+n.b

def TwoPoint(p1,p2):
    global EdgeList
    p = [p1, p2]
    n = MathEx.CalcNormal(MathEx.CalcVactor(p[0], p[1]))
    x1 = n.x*600 + MathEx.GetMidPoint(p[0],p[1]).x
    y1 = n.y*600 + MathEx.GetMidPoint(p[1],p[0]).y
    n = MathEx.CalcNormal(MathEx.CalcVactor(p[1], p[0]))
    x2 = n.x*600 + MathEx.GetMidPoint(p[0],p[1]).x
    y2 = n.y*600 + MathEx.GetMidPoint(p[1],p[0]).y
    EdgeList.append(Edge(x1, y1, x2, y2))

def ThreePoint(p1,p2,p3):
    global EdgeList
    p = [p1, p2, p3]
    center = MathEx.GetCircumcenter(p[0],p[1],p[2])
    if (MathEx.crossProduct(p[0], p[1], p[2])) == False:
        tmp = sorted([p[0], p[1], p[2]], key = SortPoint)
        TwoPoint(tmp[0], tmp[1])
        TwoPoint(tmp[1], tmp[2])
        return
    elif (MathEx.crossProduct(p[0], p[1], p[2])) > 0:
        p[1], p[2] = p[2], p[1]
    for i in range(-1,2,1):
        n = MathEx.CalcNormal(MathEx.CalcVactor(p[i], p[i+1]))
        x = n.x*600 + MathEx.GetMidPoint(p[i],p[i+1]).x
        y = n.y*600 + MathEx.GetMidPoint(p[i],p[i+1]).y
        EdgeList.append(Edge(x, y, center.x, center.y))

def cleanc():
    global PointList, EdgeList
    # if os.path.isfile('output.txt'):
    #     os.remove('output.txt')
    PointList = []
    EdgeList = []
    canvas.delete("all")

def on_button_press(event):
    global PointList

    x =  canvas.canvasx(event.x)
    y =  canvas.canvasy(event.y)

    PointList.append(Point(int(x), int(600 - y)))
    canvas.create_oval(x+5,y+5,x-5,y-5, fill = 'red')

def on_move_press(event):
    pass

def on_button_release(event):
    pass

def OutputFile():
    f = open('output.txt','w')
    for i in PointList:
        f.write('P '+str(int(i.x))+' '+str(int(i.y))+'\n')
    EdgeList.sort(key=SortEdge)
    for i in EdgeList:
        f.write('E '+str(int(i.x))+' '+str(int(i.y))+' '+str(int(i.a))+' '+str(int(i.b))+'\n')
    f.close

def ReadGraphFile():
    cleanc()
    file_path = filedialog.askopenfilename(initialdir='./')
    f = open(file_path,'r')
    for line in f.readlines():
        if line[0] == 'P':
            s = line.split()
            PointList.append(Point(int(s[1]), int(s[2])))
        if line[0] == 'E':
            s = line.split()
            EdgeList.append(Edge(int(s[1]), int(s[2]), int(s[3]), int(s[4])))
    ShowGraph()


def ReadInputFile():
    global ReadData, NumData
    NumData = 0
    ReadData = []
    file_path = filedialog.askopenfilename(initialdir='./')
    f = open(file_path,'r')
    line = f.readlines()
    for i in line:
        if i[0] == '#' or i == '\n':
            continue
        elif i[0] == '0':
            break
        s = i.split()
        if len(s) == 1:
            n = []
            cnt = int(s[0])
        else:
            n.append(Point(int(s[0]), int(s[1])))
            cnt -= 1
        if cnt == 0:
            ReadData.append(n)
    f.close()

def RunReadFile():
    global NumData, EdgeList, PointList, ReadData
    cleanc()
    if NumData >= len(ReadData):
        messagebox.showinfo("msg", "Done!")
    elif len(ReadData[NumData]) == 1:
        PointList = ReadData[NumData]
    elif len(ReadData[NumData]) == 2:
        PointList = ReadData[NumData]
        TwoPoint(PointList[0], PointList[1])
    elif len(ReadData[NumData]) == 3:
        PointList = ReadData[NumData]
        ThreePoint(PointList[0], PointList[1], PointList[2])
    NumData += 1
    ShowGraph()
    


def ShowGraph():
    global PointList, EdgeList
    for i in PointList:
        canvas.create_oval(i.x+5,(600-i.y)+5,i.x-5,(600-i.y)-5, fill = 'red')
    for i in EdgeList:
        canvas.create_line(i.x, 600-i.y, i.a, 600-i.b,fill = 'red',width = 5)

def Run():
    global PointList, EdgeList
    EdgeList = []
    if len(PointList) <= 1:
        return
    elif len(PointList) == 2:
        TwoPoint(PointList[0], PointList[1])
        # a, b = MathEx.medLine(PointList[0], PointList[1])
        # EdgeList.append(Edge(a.x, a.y, b.x, b.y))
    elif len(PointList) == 3:
        ThreePoint(PointList[0], PointList[1], PointList[2])
    else:
        messagebox.showinfo("Error", "Numbers of point is 0 ~ 3")
        cleanc()
    ShowGraph()
    

btn_step = tk.Button(text='Run', width = 10, height = 1)
btn_clean = tk.Button(text='Clean', width = 10, height = 1)
btn_output = tk.Button(text='Output', width = 10, height = 1)
btn_readgraph = tk.Button(text='ReadG', width = 10, height = 1)
btn_readfile = tk.Button(text='ReadF', width = 10, height = 1)
btn_readfilerun = tk.Button(text='ReadFRun', width = 10, height = 1)

btn_step.config(command = Run)
btn_clean.config(command = cleanc)
btn_output.config(command = OutputFile)
btn_readgraph.config(command = ReadGraphFile)
btn_readfile.config(command = ReadInputFile)
btn_readfilerun.config(command = RunReadFile)

btn_step.grid(row=0, column=0)
btn_clean.grid(row=1, column=0)
btn_output.grid(row=2, column=0)
btn_readgraph.grid(row=3, column=0)
btn_readfile.grid(row=4, column=0)
btn_readfilerun.grid(row=5, column=0)

canvas = tk.Canvas(win, bg='black', width = 10, height = 1)
canvas.config(width = 600, height = 600)
canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_move_press)
canvas.bind("<ButtonRelease-1>", on_button_release)
canvas.place(x = 100, y = 0)

win.mainloop()