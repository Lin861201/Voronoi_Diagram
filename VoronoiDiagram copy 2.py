#$LAN=PYTHON$

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
from tkinter.constants import E, N
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

win = tk.Tk()
win.config(bg='white')
win.title("Voronoi Diagram")
win.geometry("800x650")

start_x, start_y, x, y, curX, curY = 0, 0, 0, 0, 0, 0
ReadData = []
NumData = 0
PointList = []
EdgeList = []

class Solution:
    def cross( o, a, b):
        ax = a[0] - o[0]
        ay = a[1] - o[1]
        bx = b[0] - o[0]
        by = b[1] - o[1]
        return ax * by - bx * ay

    def outerTrees(trees):
        n = len(trees)
        if n <= 2:
            return trees
        trees.sort()
        
        lower = list()
        res1 = list()
        for i in range(n):
            while len(lower) >= 2 and Solution.cross(lower[-2], lower[-1], trees[i]) < 0:
                lower.pop()
                res1.pop()
            lower.append(tuple(trees[i]))
            res1.append(i)
        upper = list()
        res2 = list()
        for i in range(n -1, -1, -1):
            while len(upper) >= 2 and Solution.cross(upper[-2], upper[-1], trees[i]) < 0:
                upper.pop()
                res2.pop()
            upper.append(tuple(trees[i]))
            res2.append(i)
        return res1[1:]+res2[1:]


class Edge():
    def __init__(self, x, y, a, b, p1 = None, p2 = None, color = 'red', id = None):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.id = id
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

class LCrossP():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


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

    def Distance(p1, p2):
        return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**0.5

    def CheckWise(p1,p2,p3):
        x1,y1,x2,y2,x3,y3 = p1.x, p1.y, p2.x, p2.y, p3.x, p3.y
        return 1 if (x2-x1)*(y3-y1)-(x3-x1)*(y2-y1) > 0 else -1

def SortPoint(p):
    return p.x*2+p.y

def SortEdge(n):
    return n.x*4*600+n.y*3*600+n.a*2*600+n.b*600

def TwoPoint(p1,p2):
    p = [p1, p2]
    n = MathEx.CalcNormal(MathEx.CalcVactor(p[0], p[1]))
    x1 = n.x*600 + MathEx.GetMidPoint(p[0],p[1]).x
    y1 = n.y*600 + MathEx.GetMidPoint(p[1],p[0]).y
    n = MathEx.CalcNormal(MathEx.CalcVactor(p[1], p[0]))
    x2 = n.x*600 + MathEx.GetMidPoint(p[0],p[1]).x
    y2 = n.y*600 + MathEx.GetMidPoint(p[1],p[0]).y
    DrawLine(Edge(x1, y1, x2, y2, p1, p2))

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
        DrawLine(Edge(x, y, center.x, center.y, p[i], p[i+1]))

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

    DrawPoint(Point(int(x), int(600 - y)))
    canvas.create_oval(x+5,y+5,x-5,y-5, fill = 'green')

def on_move_press(event):
    pass

def on_button_release(event):
    pass

def motion(event):
    x, y = event.x, event.y
    pos_label.configure(text = str(x)+', '+str(600-y))

def OutputFile():
    f = open('output.txt','w', encoding="utf-8")
    for i in PointList:
        f.write('P '+str(int(i.x))+' '+str(int(i.y))+'\n')
    EdgeList.sort(key=lambda EdgeList: EdgeList.b)
    EdgeList.sort(key=lambda EdgeList: EdgeList.a)
    EdgeList.sort(key=lambda EdgeList: EdgeList.y)
    EdgeList.sort(key=lambda EdgeList: EdgeList.x)
    for i in EdgeList:
        f.write('E '+str(int(i.x))+' '+str(int(i.y))+' '+str(int(i.a))+' '+str(int(i.b))+'\n')
    f.close

def ReadGraphFile():
    cleanc()
    file_path = filedialog.askopenfilename(initialdir='./')
    f = open(file_path,'r',encoding="utf-8")
    for line in f.readlines():
        if line[0] == 'P':
            s = line.split()
            DrawPoint(Point(int(s[1]), int(s[2])))
        if line[0] == 'E':
            s = line.split()
            DrawLine(Edge(int(s[1]), int(s[2]), int(s[3]), int(s[4])))


def ReadInputFile():
    global ReadData, NumData
    NumData = 0
    ReadData = []
    file_path = filedialog.askopenfilename(initialdir='./')
    f = open(file_path,'r',encoding="utf-8")
    line = f.readlines()
    for i in line:
        if i[0] == '#' or i == '\n':
            continue
        s = i.split()
        if len(s) == 1:
            if s[0] == '0':
                break
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
    else:
        PointList = ReadData[NumData]
    NumData += 1
    ShowGraph()

def CalcCross(p1, p2, p3, p4):
    x1,y1,x2,y2 = p1.x, p1.y, p2.x, p2.y
    x3,y3,x4,y4 = p3.x, p3.y, p4.x, p4.y

    t1 = ((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1))*((x2-x1)*(y4-y1)-(x4-x1)*(y2-y1))
    if t1 > 0:
        return False

    try:
        k1 = (y2-y1)*1.0/(x2-x1)
        b1 = y1*1.0-x1*k1*1.0
        if (x4-x3)==0:
            k2 = None
            b2 = 0
        else:
            k2=(y4-y3)*1.0/(x4-x3)
            b2=y3*1.0-x3*k2*1.0
        if k2 == None:
            x = x3
        else:
            x = (b2-b1)*1.0/(k1-k2)
        y=k1*x*1.0+b1*1.0
        return [x,y]
    except:
        return False

def ShowGraph():
    global PointList, EdgeList
    for i in PointList:
        a = canvas.create_oval(i.x+5,(600-i.y)+5,i.x-5,(600-i.y)-5, fill = 'pink')
    for i in EdgeList:
        a = canvas.create_line(i.x, 600-i.y, i.a, 600-i.b,fill = i.color,width = 1)
        i.id = a

def DrawLine(line):
    EdgeList.append(line)
    a = canvas.create_line(line.x, 600-line.y, line.a, 600-line.b,fill = line.color,width = 1)
    line.id = a

def DrawPoint(point):
    PointList.append(point)
    a = canvas.create_oval(point.x+5,(600-point.y)+5,point.x-5,(600-point.y)-5, fill = 'pink')
    point.id = a

def RunHelper(PL):
    TmpEdge = []
    if len(PL) <= 1:
        return
    elif len(PL) == 2:
        TwoPoint(PL[0], PL[1])
    elif len(PL) == 3:
        ThreePoint(PL[0], PL[1], PL[2])
    else:
        m = len(PL) // 2
        sp = sorted(PL, key=lambda PL: PL.x)
        LeftPoint = sp[:m]
        RightPoint = sp[m:]
        Lline = RunHelper(LeftPoint)
        Rline = RunHelper(RightPoint)
        if Lline:
            for i in Lline:
                canvas.delete(i)
        if Rline:
            for i in Rline:
                canvas.delete(i)
        cutLine = []
        ConvexHullLine = []
        sp_np = [[i.x, i.y] for i in sp]
        print(sp_np)
        hull = ConvexHull(sp_np) #hull.vertices為逆時針
        # print(hull.vertices)
        mymethod = Solution.outerTrees(sp_np.copy()) #逆時針
        print(sp_np)
        print('my',mymethod)
        print([sp_np[i] for i in mymethod])
        print('other',hull.vertices)
        print([[sp[i].x,sp[i].y]for i in hull.vertices])
        # mymethod = hull.vertices
        print('LP: {}, RP: {}'.format(LeftPoint, RightPoint))
        for vertices in range(-1,len(mymethod)-1,1): #非上下切線標示成黃色
            print(sp[mymethod[vertices]].x, sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, sp[mymethod[vertices+1]].y)
            if sp[mymethod[vertices]] in LeftPoint and sp[mymethod[vertices+1]] in LeftPoint or sp[mymethod[vertices]] in RightPoint and sp[mymethod[vertices+1]] in RightPoint:
                a = canvas.create_line(sp[mymethod[vertices]].x, 600-sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, 600-sp[mymethod[vertices+1]].y,fill = 'green',width = 0)
                # print(sp[mymethod[vertices]].x, sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, sp[mymethod[vertices+1]].y)
                ConvexHullLine.append(a)
            else:
                a = canvas.create_line(sp[mymethod[vertices]].x, 600-sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, 600-sp[mymethod[vertices+1]].y,fill = 'orange',width = 0)
                # print(sp[mymethod[vertices]].x, sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, sp[mymethod[vertices+1]].y)
                ConvexHullLine.append(a)
                cutLine.append([mymethod[vertices],mymethod[vertices+1]])

##############################################################################################################################################
        # print(sp[cutLine[1][1]].y, sp[cutLine[1][0]].y, sp[cutLine[0][1]].y, sp[cutLine[0][0]].y)
        if max(sp[cutLine[1][1]].y, sp[cutLine[1][0]].y) < max(sp[cutLine[0][1]].y, sp[cutLine[0][0]].y):
            cutLine[1],cutLine[0] = cutLine[0], cutLine[1]
        e = cutLine[0]
        n = MathEx.CalcNormal(MathEx.CalcVactor(sp[e[1]], sp[e[0]]))
        x2 = n.x*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).x
        y2 = n.y*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).y
        End = Point(x2, y2)
        e = cutLine[1]
        n = MathEx.CalcNormal(MathEx.CalcVactor(sp[e[1]], sp[e[0]]))
        x1 = -n.x*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).x
        y1 = -n.y*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).y
        x2 = n.x*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).x
        y2 = n.y*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).y
        dict = []
        for i in EdgeList:
            res = CalcCross(Point(x1,y1),Point(x2,y2),Point(i.x,i.y),Point(i.a,i.b))
            if res:
                # print(res)
                dict.append([MathEx.Distance(Point(x2,y2), Point(res[0], res[1])), res, i])
                # canvas.create_oval(res[0]+5,(600-res[1])+5,res[0]-5,(600-res[1])-5, fill = 'red')
                # dict[MathEx.Distance(Point(x2,y2), Point(res[0], res[1]))] = res
        c = sorted(dict, key=lambda dict: dict[0])
        DrawLine(Edge(c[0][1][0], c[0][1][1], x2, y2, sp[e[0]], sp[e[1]], color = 'blue'))
        # TmpEdge.append(Edge(c[0][1][0], c[0][1][1], x2, y2, sp[e[0]], sp[e[1]], color = 'blue'))
        # print(c[0][1][0], c[0][1][1], x2, y2)
        CheckAngle = [Point(x2, y2),Point(c[0][1][0], c[0][1][1]),None]
        # print(sp[e[0]].x, sp[e[0]].y, sp[e[1]].x, sp[e[1]].y)
        # print(c[0][2].p1.x, c[0][2].p1.y, c[0][2].p2.x, c[0][2].p2.y)
        if sp[e[0]] == c[0][2].p1:
            sp[e[0]] = c[0][2].p2
        elif sp[e[0]] == c[0][2].p2:
            sp[e[0]] = c[0][2].p1
        elif sp[e[1]] == c[0][2].p1:
            sp[e[1]] = c[0][2].p2
        elif sp[e[1]] == c[0][2].p2:
            sp[e[1]] = c[0][2].p1

# #################################################################################################################################################

        while True:
            n = MathEx.CalcNormal(MathEx.CalcVactor(sp[e[1]], sp[e[0]]))
            x1 = -n.x*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).x
            y1 = -n.y*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).y
            x2 = n.x*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).x
            y2 = n.y*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).y
            dict = []
            for i in EdgeList:
                res = CalcCross(Point(x1,y1),Point(x2,y2),Point(i.x,i.y),Point(i.a,i.b))
                if res and res[1] <= c[0][1][1]:
                    if MathEx.Distance(Point(c[0][1][0],c[0][1][1]), Point(res[0], res[1])) < 0.0001:
                        continue
                    dict.append([MathEx.Distance(Point(c[0][1][0],c[0][1][1]), Point(res[0], res[1])), res, i])
                    # canvas.create_oval(res[0]+5,(600-res[1])+5,res[0]-5,(600-res[1])-5, fill = 'green')
            Dline = c[0][2] #要刪除的線段
            Lline = Point(Dline.x, Dline.y) #線段的右點
            Rline = Point(Dline.a, Dline.b) #線段的左點
            Start = Point(c[0][1][0],c[0][1][1]) #交點
            for num, i in enumerate(EdgeList):
                if id(i) == id(Dline):
                    del EdgeList[num]
                    break 
            canvas.delete(Dline.id)
            c = sorted(dict, key=lambda dict: dict[0])
            if len(c) == 0:
                if MathEx.CheckWise(CheckAngle[0], CheckAngle[1], End) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Lline):
                    DrawLine(Edge(Start.x, Start.y, Rline.x, Rline.y, Dline.p1, Dline.p2))
                    DrawLine(Edge(Start.x, Start.y, End.x, End.y, sp[e[1]], sp[e[0]], color='blue'))
                elif MathEx.CheckWise(CheckAngle[0], CheckAngle[1], End) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Rline):
                    DrawLine(Edge(Start.x, Start.y, Lline.x, Lline.y, Dline.p1, Dline.p2))
                    DrawLine(Edge(Start.x, Start.y, End.x, End.y, sp[e[1]], sp[e[0]], color='blue'))
                break
            DrawLine(Edge(Start.x, Start.y, c[0][1][0], c[0][1][1], sp[e[0]], sp[e[1]], color = 'blue'))
            # TmpEdge.append(Edge(Start.x, Start.y, c[0][1][0], c[0][1][1], sp[e[0]], sp[e[1]], color = 'blue'))
            CheckAngle[2] = Point(c[0][1][0], c[0][1][1])
            if MathEx.CheckWise(CheckAngle[0], CheckAngle[1], CheckAngle[2]) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Lline):
                DrawLine(Edge(Start.x, Start.y, Rline.x, Rline.y, Dline.p1, Dline.p2))
                pass
            elif MathEx.CheckWise(CheckAngle[0], CheckAngle[1], CheckAngle[2]) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Rline):
                DrawLine(Edge(Start.x, Start.y, Lline.x, Lline.y, Dline.p1, Dline.p2))
                pass
            CheckAngle[0],CheckAngle[1] = CheckAngle[1],CheckAngle[2]
            if sp[e[0]] == c[0][2].p1:
                sp[e[0]] = c[0][2].p2
            elif sp[e[0]] == c[0][2].p2:
                sp[e[0]] = c[0][2].p1
            elif sp[e[1]] == c[0][2].p1:
                sp[e[1]] = c[0][2].p2
            elif sp[e[1]] == c[0][2].p2:
                sp[e[1]] = c[0][2].p1
        return ConvexHullLine




def Run():
    global PointList, EdgeList
    EdgeList = []
    RunHelper(PointList)

    

btn_step = tk.Button(text='Run', width = 10, height = 1)
btn_clean = tk.Button(text='Clean', width = 10, height = 1)
btn_output = tk.Button(text='Output', width = 10, height = 1)
btn_readgraph = tk.Button(text='ReadG', width = 10, height = 1)
btn_readfile = tk.Button(text='ReadF', width = 10, height = 1)
btn_readfilerun = tk.Button(text='ReadFRun', width = 10, height = 1)
pos_label = tk.Label(text='', width = 10, height = 1)

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
canvas.bind('<Motion>', motion)
canvas.place(x = 100, y = 0)
pos_label.place(x = 100, y = 600)

win.mainloop()