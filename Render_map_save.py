# coding=utf-8
import xml.dom.minidom
import cv2
import math
import win32api
import win32con
import win32gui
from win32api import *
from win32con import *
from win32gui import *
from OpenGL.WGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import uuid
# roundabout
# REAL_X = 3800.0
# REAL_Y = 9370.0
# scale = 180.0
# name = 'test.png'
# REAL_X = 5330.0
# REAL_Y = 8580.0
# scale = 120.0            # 2000
# southeastgate
# REAL_X = 5330.0
# REAL_Y = 8980.0
# scale = 150.0
# ramp
# REAL_X = 5820.0
# REAL_Y = 7860.0
# scale = 120.0
# realx = [3800.0, 5330.0, 5330.0, 5820.0]
# realy = [9370.0, 8580.0, 8980.0, 7860.0]
# scale = [180.0, 120.0, 150.0, 120.0]
size =  15000            # 15000
# name = ['roundabout.png', 'junction.png', 'south_east_gate.png','ramp.png']
realx = [5400.0, 4900.0]
realy = [9100.0, 8200.0]
scale = [800.0, 1300.0]
name = ['partA.png','partC.png']
load = ['Tsinghua Map-Part A.net.xml','Tsinghua Map-Part C.net.xml']
# WIDTH_FACTOR = 2.1 * 180.0 / scale * float(size) / 800.0
# WIDTH_FACTOR = float(size)  / scale



def render_map(size, real_x, real_y, scale, name,load):
    LOC_X = -real_x / scale
    LOC_Y = -real_y / scale
    load_path = './TUmap/' + load
    dom_obj = xml.dom.minidom.parse(load_path)
    # 得到元素对象
    element_obj = dom_obj.documentElement
    sub_element_edge = element_obj.getElementsByTagName("edge")
    sub_element_junction = element_obj.getElementsByTagName("junction")
    sub_element_tlLogic = element_obj.getElementsByTagName("tlLogic")
    glClearColor(0.78,0.78,0.78, 1)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(LOC_X, LOC_Y, 0)#移动地图，只渲染显示区域   # -2.2, -4.4

    # glScaled(0.015434,0.027010, 1)
    sub_element_edge=sub_element_edge
    sub_element_junction=sub_element_junction

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    # glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    #直线法绘制道路

    # for i in range(len(sub_element_edge)):
    #     if sub_element_edge[i].getAttribute('type') != 'internal':
    #         sub_element_lane = sub_element_edge[i].getElementsByTagName("lane")
    #         for j in range(len(sub_element_lane)):
    #             shape = sub_element_lane[j].getAttribute("shape")
    #             type = str(sub_element_lane[j].getAttribute("allow"))
    #             shape_list = shape.split(" ")
    #             try:
    #                 width = float(sub_element_lane[j].getAttribute("width"))
    #             except:
    #                 # print(sub_element_lane[j].getAttribute("width"))
    #                 width = 3.5
    #
    #             glLineWidth(width * WIDTH_FACTOR)
    #             if type == 'pedestrian':
    #                 glColor3f(0.663, 0.663, 0.663)
    #             elif type == 'bicycle':
    #                 glColor3f(0.455, 0.721, 0.926)
    #             else:
    #                 glColor3f(0.0,0.0,0.0)
    #             glBegin(GL_LINE_STRIP)
    #             for k in range(len(shape_list)):
    #                 shape_point = shape_list[k].split(",")
    #                 glVertex2f((float(shape_point[0]) / scale) * 1, (float(shape_point[1]) / scale) * 1)
    #             glEnd()
    for i in range(len(sub_element_edge)):
        if sub_element_edge[i].getAttribute('function') != 'internal':
            sub_element_lane = sub_element_edge[i].getElementsByTagName("lane")  # 提取单车道数据
            for j in range(len(sub_element_lane)):
                shape = sub_element_lane[j].getAttribute("shape")  # 提取形状数据
                type = str(sub_element_lane[j].getAttribute("allow"))
                try:
                    width = float(sub_element_lane[j].getAttribute("width"))
                except:
                    # print(sub_element_lane[j].getAttribute("width"))
                    width = 3.5
                shape_list = shape.split(" ")
                for k in range(len(shape_list) - 1):
                    shape_point_1 = shape_list[k].split(",")
                    shape_point_2 = shape_list[k + 1].split(",")
                    shape_point_1[0] = float(shape_point_1[0]) # / scale
                    shape_point_1[1] = float(shape_point_1[1]) # / scale
                    shape_point_2[0] = float(shape_point_2[0]) # / scale
                    shape_point_2[1] = float(shape_point_2[1]) # / scale
                    # 道路顶点生成
                    dx1 = shape_point_2[0] - shape_point_1[0]
                    dy1 = shape_point_2[1] - shape_point_1[1]
                    v1 = np.array([-dy1, dx1])
                    absdx = abs(shape_point_1[0] - shape_point_2[0])
                    absdy = abs(shape_point_1[1] - shape_point_2[1])
                    if math.sqrt(absdx * absdx + absdy * absdy) > 0:
                        v3 = v1 / math.sqrt(absdx * absdx + absdy * absdy) * width * 0.45
                        # print(v3)
                        [x1, y1] = ([shape_point_1[0], shape_point_1[1]] +  v3) / scale
                        [x2, y2] = ([shape_point_1[0], shape_point_1[1]] -  v3) / scale
                        [x4, y4] = ([shape_point_2[0], shape_point_2[1]] +  v3) / scale
                        [x3, y3] = ([shape_point_2[0], shape_point_2[1]] -  v3) / scale # 0.0176 * v3
                        # print(x1,y1)
                        glBegin(GL_POLYGON)  # 开始绘制单车道
                        if type == 'pedestrian':
                            glColor3f(0.663, 0.663, 0.663)
                        elif type == 'bicycle':
                            glColor3f(0.455, 0.721, 0.926)
                        else:
                            glColor3f(0.0,0.0,0.0)
                        glVertex2f(x1, y1)
                        glVertex2f(x2, y2)
                        glVertex2f(x3, y3)
                        glVertex2f(x4, y4)
                        glEnd()  # 结束绘制线段

    for i in range(len(sub_element_junction)):
        shape = sub_element_junction[i].getAttribute("shape")
        shape_list = shape.split(" ")

        glLineWidth(10) #TODO:line width 是否会对scale那里产生影响，考虑调成1重新生成
        glBegin(GL_POLYGON)
        glColor3f(0.0,0.0,0.0)
        for k in range(len(shape_list)):
            shape_point = shape_list[k].split(",")
            if shape_point[0] != '' :
                glVertex2f((float(shape_point[0]) / scale) * 1, (float(shape_point[1]) / scale) * 1)
        glEnd()




    glFlush()

    glDisable(GL_BLEND)
    glDisable(GL_LINE_SMOOTH)
    glDisable(GL_POLYGON_SMOOTH)

    pPixelData = np.zeros([size,size, 4], np.uint8)
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glReadPixels(0, 0, size, size, GL_RGBA, GL_UNSIGNED_BYTE,  pPixelData)
    image = cv2.flip(pPixelData, 0, dst=None)
    # return image
    path = './Tsinghua_examples/'  + name
    cv2.imwrite(path, image)


for i in range(len(realx)):
    hInstance = win32api.GetModuleHandle(None)

    wndClass = win32gui.WNDCLASS()
    # wndClass.lpfnWndProc = win32gui.DefWindowProc()
    wndClass.hInstance = hInstance
    wndClass.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
    wndClass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wndClass.lpszClassName = str(uuid.uuid4())
    wndClass.style = win32con.CS_OWNDC

    wndClassAtom = win32gui.RegisterClass(wndClass)

    # 隐藏窗口的宽和高
    width, height = size, size
    hWnd = win32gui.CreateWindow(wndClassAtom, '', win32con.WS_POPUP, 0, 0, width, height, 0, 0, hInstance, None)

    # Ok, window created, now we can create OpenGL context
    PFD_TYPE_RGBA = 0
    PFD_MAIN_PLANE = 0
    PFD_DOUBLEBUFFER = 0x00000001
    PFD_DRAW_TO_WINDOW = 0x00000004
    PFD_SUPPORT_OPENGL = 0x00000020
    pfd = PIXELFORMATDESCRIPTOR()

    # note - we don't using double buffering
    pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL
    pfd.iPixelType = PFD_TYPE_RGBA
    pfd.cColorBits = 32
    pfd.cDepthBits = 24
    pfd.iLayerType = PFD_MAIN_PLANE

    hdc = win32gui.GetDC(hWnd)

    pixelformat = ChoosePixelFormat(hdc, pfd)
    SetPixelFormat(hdc, pixelformat, pfd)

    oglrc = wglCreateContext(hdc)
    wglMakeCurrent(hdc, oglrc)

    render_map(size, realx[i], realy[i], scale[i], name[i], load[i])




