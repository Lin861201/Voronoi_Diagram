#$LAN=PYTHON$
#國立中山大學
#碩士一年級
#M103040045
#林子傑

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.constants import E, N
import threading
import random

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
        # trees.sort()
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

class VD():
    def __init__(self, PList, EList):
        self.PList = PList
        self.EList = EList

class Edge():
    def __init__(self, x, y, p1 = None, p2 = None, color = 'red', id = None):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.id = id
        if x.x < y.x:
            self.x, self.y= x, y
        elif y.x < x.x:
            self.x, self.y = y, x
        elif x.y < y.y:
            self.x, self.y = x, y
        elif y.y < x.y:
            self.x, self.y = y, x
        else:
            self.x, self.y= x, y

class Point():
    def __init__(self, x, y, id = None):
        self.x = x
        self.y = y
        self.id = id

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

def TwoPoint(p1,p2,color ='red'):
    p = [p1, p2]
    n = MathEx.CalcNormal(MathEx.CalcVactor(p[0], p[1]))
    x1 = n.x*600 + MathEx.GetMidPoint(p[0],p[1]).x
    y1 = n.y*600 + MathEx.GetMidPoint(p[1],p[0]).y
    n = MathEx.CalcNormal(MathEx.CalcVactor(p[1], p[0]))
    x2 = n.x*600 + MathEx.GetMidPoint(p[0],p[1]).x
    y2 = n.y*600 + MathEx.GetMidPoint(p[1],p[0]).y
    a = canvas.create_line(p1.x, 600-p1.y, p2.x, 600-p2.y,fill = 'pink',width = 0)
    DrawLine(Edge(Point(x1, y1), Point(x2, y2), p1, p2, color =color))
    return [a]

def ThreePoint(p1,p2,p3,color='red'):
    global EdgeList
    p = [p1, p2, p3]
    res = []
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
        a = canvas.create_line(p[i].x, 600-p[i].y, p[i+1].x, 600-p[i+1].y,fill = 'pink',width = 0)
        res.append(a)
        DrawLine(Edge(Point(x, y), center, p[i], p[i+1], color =color))
    return res

def cleanc():
    global PointList, EdgeList, first, Stepcnt
    first = True
    Stepcnt = 0
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
    # canvas.create_oval(x+5,y+5,x-5,y-5, fill = 'green')

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
    EdgeList.sort(key=lambda EdgeList: EdgeList.y.y)
    EdgeList.sort(key=lambda EdgeList: EdgeList.y.x)
    EdgeList.sort(key=lambda EdgeList: EdgeList.x.y)
    EdgeList.sort(key=lambda EdgeList: EdgeList.x.x)
    for i in EdgeList:
        f.write('E '+str(int(i.x.x))+' '+str(int(i.x.y))+' '+str(int(i.y.x))+' '+str(int(i.y.y))+'\n')
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
            DrawLine(Edge(Point(int(s[1]), int(s[2])), Point(int(s[3]), int(s[4]))))


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
        # TwoPoint(PointList[0], PointList[1])
    elif len(ReadData[NumData]) == 3:
        PointList = ReadData[NumData]
        # ThreePoint(PointList[0], PointList[1], PointList[2])
    else:
        PointList = ReadData[NumData]
    NumData += 1
    ShowGraph()

def GetRandomColor():
    de=("%02x"%random.randint(0,255))
    re=("%02x"%random.randint(0,255))
    we=("%02x"%random.randint(0,255))
    ge="#"
    return ge+de+re+we

def CalcCross(p1, p2, p3, p4):
    x1,y1,x2,y2 = p1.x, p1.y, p2.x, p2.y
    x3,y3,x4,y4 = p3.x, p3.y, p4.x, p4.y

    t1 = ((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1))*((x2-x1)*(y4-y1)-(x4-x1)*(y2-y1))
    if t1 > 0:
        return False

    # try:
    if (x2-x1) == 0:
        k1 = 999999999999
    else:
        k1 = (y2-y1)*1.0/(x2-x1)
    b1 = y1*1.0-x1*k1*1.0
    if (x4-x3)==0:
        k2 = None
        b2 = 0
    else:
        if (x4-x3) == 0:
                k2 = 999999999999
        else:
            k2=(y4-y3)*1.0/(x4-x3)
        b2=y3*1.0-x3*k2*1.0
    if k2 == None:
        x = x3
    else:
        if (k1-k2) == 0:
            x = 999999999999
        else:
            x = (b2-b1)*1.0/(k1-k2)
    y=k1*x*1.0+b1*1.0
    return [x,y]
    # except:
    #     return None

def ShowGraph():
    global PointList, EdgeList
    for i in PointList:
        a = canvas.create_oval(i.x+5,(600-i.y)+5,i.x-5,(600-i.y)-5, fill = 'pink')
        i.id = a
    for i in EdgeList:
        DrawLine(i)
        a = canvas.create_line(i.x.x, 600-i.x.y, i.y.x, 600-i.y.y,fill = i.color,width = 1)
        i.id = a

def DrawLine(line):
    EdgeList.append(line)
    a = canvas.create_line(line.x.x, 600-line.x.y, line.y.x, 600-line.y.y,fill = line.color,width = 1)
    line.id = a
    return a

def DrawPoint(point):
    PointList.append(point)
    a = canvas.create_oval(point.x+5,(600-point.y)+5,point.x-5,(600-point.y)-5, fill = 'pink')
    point.id = a

def CleanSingleEdge():
    p = []
    n = []
    for i in EdgeList:
        a,b,c,d = int(i.x.x), int(i.x.y), int(i.y.x), int(i.y.y)
        if a == c and b == d:
            continue
        if a >= 0 and a <= 600 and b >=0 and b <= 600:
            if [a,b] in p:
                n[p.index([a,b])] +=1
            else:
                p.append([a,b])
                n.append(1)
        if c >= 0 and c <= 600 and d >=0 and d <= 600:
            if [c,d] in p:
                n[p.index([c,d])] +=1
            else:
                p.append([c,d])
                n.append(1)
    cnt = 0
    while cnt < len(n):
        if n[cnt] != 1:
            del p[cnt]
            del n[cnt]
        else:
            cnt += 1
    res = len(p)
    cnt = 0
    while cnt < len(EdgeList):
        if [int(EdgeList[cnt].x.x),int(EdgeList[cnt].x.y)] in p or [int(EdgeList[cnt].y.x),int(EdgeList[cnt].y.y)] in p:
            canvas.delete(EdgeList[cnt].id)
            del EdgeList[cnt]
        else:
            cnt += 1
    if res != 0:
        CleanSingleEdge()

def RunHelper(PL):
    if len(PL) <= 1:
        return
    elif len(PL) == 2:
        a = TwoPoint(PL[0], PL[1])
        return a
    elif len(PL) == 3:
        a = ThreePoint(PL[0], PL[1], PL[2])
        return a 
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
        mymethod = Solution.outerTrees(sp_np.copy())
        for vertices in range(-1,len(mymethod)-1,1):
            if sp[mymethod[vertices]] in LeftPoint and sp[mymethod[vertices+1]] in LeftPoint or sp[mymethod[vertices]] in RightPoint and sp[mymethod[vertices+1]] in RightPoint:
                a = canvas.create_line(sp[mymethod[vertices]].x, 600-sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, 600-sp[mymethod[vertices+1]].y,fill = 'pink',width = 0)
                # print(sp[mymethod[vertices]].x, sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, sp[mymethod[vertices+1]].y)
                ConvexHullLine.append(a)
                pass
            else:
                a = canvas.create_line(sp[mymethod[vertices]].x, 600-sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, 600-sp[mymethod[vertices+1]].y,fill = 'green',width = 0)
                # print(sp[mymethod[vertices]].x, sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, sp[mymethod[vertices+1]].y)
                ConvexHullLine.append(a)
                cutLine.append([mymethod[vertices],mymethod[vertices+1]])

##############################################################################################################################################
        if (sp[cutLine[1][1]].y + sp[cutLine[1][0]].y) / 2 < (sp[cutLine[0][1]].y + sp[cutLine[0][0]].y)/2:
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
            if i.p1 not in PL or i.p2 not in PL:
                continue
            res = CalcCross(Point(x1,y1),Point(x2,y2),i.x,i.y)
            if res:
                dict.append([MathEx.Distance(Point(x2,y2), Point(res[0], res[1])), res, i])
                # canvas.create_oval(res[0]+5,(600-res[1])+5,res[0]-5,(600-res[1])-5, fill = 'red')
                # dict[MathEx.Distance(Point(x2,y2), Point(res[0], res[1]))] = res
        c = sorted(dict, key=lambda dict: dict[0])
        cntc = 0
        for i in range(len(c)):
            if c[i][2].p1 in PL and c[i][2].p2 in PL:
                cntc = i
                break
        DrawLine(Edge(Point(c[cntc][1][0], c[cntc][1][1]), Point(x2, y2), sp[e[0]], sp[e[1]], color = 'red'))
        CheckAngle = [Point(x2, y2),Point(c[cntc][1][0], c[cntc][1][1]),None]
        if sp[e[0]] == c[cntc][2].p1:
            sp[e[0]] = c[cntc][2].p2
        elif sp[e[0]] == c[cntc][2].p2:
            sp[e[0]] = c[cntc][2].p1
        elif sp[e[1]] == c[cntc][2].p1:
            sp[e[1]] = c[cntc][2].p2
        elif sp[e[1]] == c[cntc][2].p2:
            sp[e[1]] = c[cntc][2].p1

# #################################################################################################################################################

        while True:
            n = MathEx.CalcNormal(MathEx.CalcVactor(sp[e[1]], sp[e[0]]))
            x1 = -n.x*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).x
            y1 = -n.y*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).y
            x2 = n.x*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).x
            y2 = n.y*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).y
            dict = []
            for i in EdgeList:
                if i.p1 not in PL or i.p2 not in PL:
                    continue
                res = CalcCross(Point(x1,y1),Point(x2,y2),i.x,i.y)
                if res and res[1] <= c[cntc][1][1]:
                    if MathEx.Distance(Point(c[cntc][1][0],c[cntc][1][1]), Point(res[0], res[1])) < 0.0001:
                        continue
                    dict.append([MathEx.Distance(Point(c[cntc][1][0],c[cntc][1][1]), Point(res[0], res[1])), res, i])
            Dline = c[cntc][2] 
            Lline = Point(Dline.x.x, Dline.x.y) 
            Rline = Point(Dline.y.x, Dline.y.y) 
            Start = Point(c[cntc][1][0],c[cntc][1][1])
            for num, i in enumerate(EdgeList):
                if id(i) == id(Dline):
                    del EdgeList[num]
                    break 
            canvas.delete(Dline.id)
            c = sorted(dict, key=lambda dict: dict[0])
            cntc = 0
            for i in range(len(c)):
                if c[i][2].p1 in PL and c[i][2].p2 in PL:
                    cntc = i
                    break
            if len(c) == 0 or (len(c) ==  1 and c[0][0] < 0.1):
                if MathEx.CheckWise(CheckAngle[0], CheckAngle[1], End) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Lline):
                    DrawLine(Edge(Start, Rline, Dline.p1, Dline.p2))
                    DrawLine(Edge(Start, End, sp[e[1]], sp[e[0]], color='red'))
                elif MathEx.CheckWise(CheckAngle[0], CheckAngle[1], End) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Rline):
                    DrawLine(Edge(Start, Lline, Dline.p1, Dline.p2))
                    DrawLine(Edge(Start, End, sp[e[1]], sp[e[0]], color='red'))
                break
            DrawLine(Edge(Start, Point(c[cntc][1][0], c[cntc][1][1]), sp[e[0]], sp[e[1]], color = 'red'))
            CheckAngle[2] = Point(c[cntc][1][0], c[cntc][1][1])
            if MathEx.CheckWise(CheckAngle[0], CheckAngle[1], CheckAngle[2]) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Lline):
                DrawLine(Edge(Start, Rline, Dline.p1, Dline.p2))
                pass
            elif MathEx.CheckWise(CheckAngle[0], CheckAngle[1], CheckAngle[2]) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Rline):
                DrawLine(Edge(Start, Lline, Dline.p1, Dline.p2))
                pass
            CheckAngle[0],CheckAngle[1] = CheckAngle[1],CheckAngle[2]
            if sp[e[0]] == c[cntc][2].p1:
                sp[e[0]] = c[cntc][2].p2
            elif sp[e[0]] == c[cntc][2].p2:
                sp[e[0]] = c[cntc][2].p1
            elif sp[e[1]] == c[cntc][2].p1:
                sp[e[1]] = c[cntc][2].p2
            elif sp[e[1]] == c[cntc][2].p2:
                sp[e[1]] = c[cntc][2].p1
        CleanSingleEdge()
        for i in EdgeList:
            canvas.itemconfig(i.id,fill='red')
        return ConvexHullLine

Stepcnt = 0
first = True

def StepHelper(PL):
    global Stepcnt
    hyperplane = []
    LeftLine = []
    RightLine = []
    if len(PL) <= 1:
        return
    elif len(PL) == 2:
        a = TwoPoint(PL[0], PL[1], color = GetRandomColor())
        return a
    elif len(PL) == 3:
        a = ThreePoint(PL[0], PL[1], PL[2], color = GetRandomColor())
        return a 
    else:
        m = len(PL) // 2
        sp = sorted(PL, key=lambda PL: PL.x)
        LeftPoint = sp[:m]
        RightPoint = sp[m:]
        Lline = StepHelper(LeftPoint)
        Rline = StepHelper(RightPoint)
        Stepcnt = 0
        while Stepcnt < 1:
            pass
        if Lline:
            for i in Lline:
                canvas.delete(i)
        if Rline:
            for i in Rline:
                canvas.delete(i)
        cutLine = []
        ConvexHullLine = []
        sp_np = [[i.x, i.y] for i in sp]
        mymethod = Solution.outerTrees(sp_np.copy())
        for vertices in range(-1,len(mymethod)-1,1):
            if sp[mymethod[vertices]] in LeftPoint and sp[mymethod[vertices+1]] in LeftPoint or sp[mymethod[vertices]] in RightPoint and sp[mymethod[vertices+1]] in RightPoint:
                a = canvas.create_line(sp[mymethod[vertices]].x, 600-sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, 600-sp[mymethod[vertices+1]].y,fill = 'pink',width = 0)
                # print(sp[mymethod[vertices]].x, sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, sp[mymethod[vertices+1]].y)
                ConvexHullLine.append(a)
                pass
            else:
                a = canvas.create_line(sp[mymethod[vertices]].x, 600-sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, 600-sp[mymethod[vertices+1]].y,fill = 'green',width = 0)
                # print(sp[mymethod[vertices]].x, sp[mymethod[vertices]].y, sp[mymethod[vertices+1]].x, sp[mymethod[vertices+1]].y)
                ConvexHullLine.append(a)
                cutLine.append([mymethod[vertices],mymethod[vertices+1]])
        while Stepcnt < 2:
            pass
##############################################################################################################################################
        if (sp[cutLine[1][1]].y + sp[cutLine[1][0]].y) / 2 < (sp[cutLine[0][1]].y + sp[cutLine[0][0]].y)/2:
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
            if i.p1 not in PL or i.p2 not in PL:
                continue
            res = CalcCross(Point(x1,y1),Point(x2,y2),i.x,i.y)
            if res:
                dict.append([MathEx.Distance(Point(x2,y2), Point(res[0], res[1])), res, i])
                # canvas.create_oval(res[0]+5,(600-res[1])+5,res[0]-5,(600-res[1])-5, fill = 'red')
                # dict[MathEx.Distance(Point(x2,y2), Point(res[0], res[1]))] = res
        c = sorted(dict, key=lambda dict: dict[0])
        cntc = 0
        for i in range(len(c)):
            if c[i][2].p1 in PL and c[i][2].p2 in PL:
                cntc = i
                break
        hpid = DrawLine(Edge(Point(c[cntc][1][0], c[cntc][1][1]), Point(x2, y2), sp[e[0]], sp[e[1]], color = 'blue')) #??????HP
        hyperplane.append(hpid)
        CheckAngle = [Point(x2, y2),Point(c[cntc][1][0], c[cntc][1][1]),None]
        if sp[e[0]] == c[cntc][2].p1:
            sp[e[0]] = c[cntc][2].p2
        elif sp[e[0]] == c[cntc][2].p2:
            sp[e[0]] = c[cntc][2].p1
        elif sp[e[1]] == c[cntc][2].p1:
            sp[e[1]] = c[cntc][2].p2
        elif sp[e[1]] == c[cntc][2].p2:
            sp[e[1]] = c[cntc][2].p1

# #################################################################################################################################################
        while True:

            n = MathEx.CalcNormal(MathEx.CalcVactor(sp[e[1]], sp[e[0]]))
            x1 = -n.x*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).x
            y1 = -n.y*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).y
            x2 = n.x*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).x
            y2 = n.y*600 + MathEx.GetMidPoint(sp[e[0]], sp[e[1]]).y
            dict = []
            
            for i in EdgeList:
                if i.p1 not in PL or i.p2 not in PL:
                    continue
                res = CalcCross(Point(x1,y1),Point(x2,y2),i.x,i.y)
                if res and res[1] <= c[cntc][1][1]:
                    if MathEx.Distance(Point(c[cntc][1][0],c[cntc][1][1]), Point(res[0], res[1])) < 0.0001:
                        continue
                    # canvas.create_oval(res[0]+5,(600-res[1])+5,res[0]-5,(600-res[1])-5, fill = 'red')
                    dict.append([MathEx.Distance(Point(c[cntc][1][0],c[cntc][1][1]), Point(res[0], res[1])), res, i])
            Dline = c[cntc][2] 
            Lline = Point(Dline.x.x, Dline.x.y)
            Rline = Point(Dline.y.x, Dline.y.y) 
            Start = Point(c[cntc][1][0],c[cntc][1][1]) 
            for num, i in enumerate(EdgeList):
                if id(i) == id(Dline):
                    del EdgeList[num]
                    break 
            canvas.delete(Dline.id)
            c = sorted(dict, key=lambda dict: dict[0])
            cntc = 0
            for i in range(len(c)):
                if c[i][2].p1 in PL and c[i][2].p2 in PL:
                    cntc = i
                    break

            if len(c) == 0 or (len(c) ==  1 and c[0][0] < 0.1):
                if MathEx.CheckWise(CheckAngle[0], CheckAngle[1], End) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Lline):
                    DrawLine(Edge(Start, Rline, Dline.p1, Dline.p2))
                    hpid = DrawLine(Edge(Start, End, sp[e[1]], sp[e[0]], color='blue'))
                elif MathEx.CheckWise(CheckAngle[0], CheckAngle[1], End) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Rline):
                    DrawLine(Edge(Start, Lline, Dline.p1, Dline.p2))
                    hpid = DrawLine(Edge(Start, End, sp[e[1]], sp[e[0]], color='blue'))
                hyperplane.append(hpid)
                break
            hpid = DrawLine(Edge(Start, Point(c[cntc][1][0], c[cntc][1][1]), sp[e[0]], sp[e[1]], color = 'blue'))
            hyperplane.append(hpid)
            CheckAngle[2] = Point(c[cntc][1][0], c[cntc][1][1])
            if MathEx.CheckWise(CheckAngle[0], CheckAngle[1], CheckAngle[2]) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Lline):
                DrawLine(Edge(Start, Rline, Dline.p1, Dline.p2))
            elif MathEx.CheckWise(CheckAngle[0], CheckAngle[1], CheckAngle[2]) == MathEx.CheckWise(CheckAngle[0], CheckAngle[1], Rline):
                DrawLine(Edge(Start, Lline, Dline.p1, Dline.p2))
            CheckAngle[0],CheckAngle[1] = CheckAngle[1],CheckAngle[2]
            if sp[e[0]] == c[cntc][2].p1:
                sp[e[0]] = c[cntc][2].p2
            elif sp[e[0]] == c[cntc][2].p2:
                sp[e[0]] = c[cntc][2].p1
            elif sp[e[1]] == c[cntc][2].p1:
                sp[e[1]] = c[cntc][2].p2
            elif sp[e[1]] == c[cntc][2].p2:
                sp[e[1]] = c[cntc][2].p1
        CleanSingleEdge()
        while Stepcnt < 3:
            pass
        pc = GetRandomColor()
        for i in PL:
            canvas.itemconfig(i.id,fill=pc)
        for i in hyperplane:
            canvas.itemconfig(i,fill='red')
        return ConvexHullLine

def Step():
    global first, Stepcnt
    if first:
        t = threading.Thread(target = StepHelper, args=(PointList,))
        t.start()
        first = False
    else:
        Stepcnt+=1


def Run():
    global PointList, EdgeList
    EdgeList = []
    RunHelper(PointList)

    

btn_run = tk.Button(text='Run', width = 10, height = 1)
btn_clean = tk.Button(text='Clean', width = 10, height = 1)
btn_output = tk.Button(text='Output', width = 10, height = 1)
btn_readgraph = tk.Button(text='ReadG', width = 10, height = 1)
btn_readfile = tk.Button(text='ReadF', width = 10, height = 1)
btn_readfilerun = tk.Button(text='ReadFRun', width = 10, height = 1)
btn_step = tk.Button(text='step', width = 10, height = 1)
pos_label = tk.Label(text='', width = 10, height = 1)

btn_run.config(command = Run)
btn_clean.config(command = cleanc)
btn_output.config(command = OutputFile)
btn_readgraph.config(command = ReadGraphFile)
btn_readfile.config(command = ReadInputFile)
btn_readfilerun.config(command = RunReadFile)
btn_step.config(command = Step)

btn_run.grid(row=0, column=0)
btn_clean.grid(row=1, column=0)
btn_output.grid(row=2, column=0)
btn_readgraph.grid(row=3, column=0)
btn_readfile.grid(row=4, column=0)
btn_readfilerun.grid(row=5, column=0)
btn_step.grid(row=6, column=0)

canvas = tk.Canvas(win, bg='black', width = 10, height = 1)
canvas.config(width = 600, height = 600)
canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_move_press)
canvas.bind("<ButtonRelease-1>", on_button_release)
canvas.bind('<Motion>', motion)
canvas.place(x = 100, y = 0)
pos_label.place(x = 100, y = 600)

win.mainloop()