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
REAL_X = 5400.0
REAL_Y = 9200.0
scale = 1200.0            # 2000
size =  800             # 15000
WIDTH_FACTOR = 2.0 * 180.0 / scale
LOC_X = -REAL_X / scale
LOC_Y = -REAL_Y / scale

glutInit()
glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
glutInitWindowPosition(50,100)
glutInitWindowSize(size, size)
glutCreateWindow(u'Test Tsinghua Map')

# hInstance = win32api.GetModuleHandle(None)
#
# wndClass = win32gui.WNDCLASS()
# # wndClass.lpfnWndProc = win32gui.DefWindowProc()
# wndClass.hInstance = hInstance
# wndClass.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
# wndClass.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
# wndClass.lpszClassName = str(uuid.uuid4())
# wndClass.style = win32con.CS_OWNDC
#
# wndClassAtom = win32gui.RegisterClass(wndClass)
#
# # 隐藏窗口的宽和高
# width, height =size, size
# hWnd = win32gui.CreateWindow(wndClassAtom, '', win32con.WS_POPUP, 0, 0, width, height, 0, 0, hInstance, None)
#
# # Ok, window created, now we can create OpenGL context
# PFD_TYPE_RGBA = 0
# PFD_MAIN_PLANE = 0
# PFD_DOUBLEBUFFER = 0x00000001
# PFD_DRAW_TO_WINDOW = 0x00000004
# PFD_SUPPORT_OPENGL = 0x00000020
# pfd = PIXELFORMATDESCRIPTOR()
#
# # note - we don't using double buffering
# pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL
# pfd.iPixelType = PFD_TYPE_RGBA
# pfd.cColorBits = 32
# pfd.cDepthBits = 24
# pfd.iLayerType = PFD_MAIN_PLANE
#
# hdc = win32gui.GetDC(hWnd)
#
# pixelformat = ChoosePixelFormat(hdc, pfd)
# SetPixelFormat(hdc, pixelformat, pfd)
#
# oglrc = wglCreateContext(hdc)
# wglMakeCurrent(hdc, oglrc)





def render_map():
    # dom_obj = xml.dom.minidom.parse("Map/Map6_Tsinghua/grid-map.net.xml")
    dom_obj = xml.dom.minidom.parse("TUmap/Tsinghua Map-Part A.net.xml")
    # 得到元素对象

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
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    #直线法绘制道路

    for i in range(len(sub_element_edge)):
        if sub_element_edge[i].getAttribute('type') != 'internal':
            sub_element_lane = sub_element_edge[i].getElementsByTagName("lane")
            for j in range(len(sub_element_lane)):
                shape = sub_element_lane[j].getAttribute("shape")
                type = str(sub_element_lane[j].getAttribute("allow"))
                shape_list = shape.split(" ")
                try:
                    width = float(sub_element_lane[j].getAttribute("width"))
                except:
                    # print(sub_element_lane[j].getAttribute("width"))
                    width = 3.5
                glLineWidth(width * WIDTH_FACTOR)
                if type == 'pedestrian':
                    glColor3f(0.663, 0.663, 0.663)
                elif type == 'bicycle':
                    # glColor3f(0.545, 0.271, 0.074)
                    glColor3f(0.455, 0.721, 0.926)
                else:
                    glColor3f(0.0,0.0,0.0)
                glBegin(GL_LINE_STRIP)
                for k in range(len(shape_list)):
                    shape_point = shape_list[k].split(",")
                    glVertex2f((float(shape_point[0]) / scale) * 1, (float(shape_point[1]) / scale) * 1)
                glEnd()
    # for i in range(len(sub_element_edge)):
    #     if sub_element_edge[i].getAttribute('function') != 'internal':
    #         sub_element_lane = sub_element_edge[i].getElementsByTagName("lane")  # 提取单车道数据
    #         for j in range(len(sub_element_lane)):
    #             shape = sub_element_lane[j].getAttribute("shape")  # 提取形状数据
    #             type = str(sub_element_lane[j].getAttribute("allow"))
    #             shape_list = shape.split(" ")
    #             for k in range(len(shape_list) - 1):
    #                 shape_point_1 = shape_list[k].split(",")
    #                 shape_point_2 = shape_list[k + 1].split(",")
    #                 shape_point_1[0] = float(shape_point_1[0]) / scale
    #                 shape_point_1[1] = float(shape_point_1[1]) / scale
    #                 shape_point_2[0] = float(shape_point_2[0]) / scale
    #                 shape_point_2[1] = float(shape_point_2[1]) / scale
    #                 # 道路顶点生成
    #                 dx1 = shape_point_2[0] - shape_point_1[0]
    #                 dy1 = shape_point_2[1] - shape_point_1[1]
    #                 v1 = np.array([-dy1, dx1])
    #                 absdx = abs(shape_point_1[0] - shape_point_2[0])
    #                 absdy = abs(shape_point_1[1] - shape_point_2[1])
    #                 if math.sqrt(absdx * absdx + absdy * absdy) > 0:
    #                     v3 = v1 / math.sqrt(absdx * absdx + absdy * absdy)
    #                     print(v3)
    #                     [x1, y1] = [shape_point_1[0], shape_point_1[1]] + 0.0176 * v3
    #                     [x2, y2] = [shape_point_1[0], shape_point_1[1]] - 0.0176 * v3
    #                     [x4, y4] = [shape_point_2[0], shape_point_2[1]] + 0.0176 * v3
    #                     [x3, y3] = [shape_point_2[0], shape_point_2[1]] - 0.0176 * v3
    #                     print(x1,y1)
    #                     glBegin(GL_POLYGON)  # 开始绘制单车道
    #                     if type == 'pedestrian':
    #                         glColor3f(0.663, 0.663, 0.663)
    #                     elif type == 'bicycle':
    #                         glColor3f(0.545, 0.271, 0.074)
    #                     else:
    #                         glColor3f(0.0,0.0,0.0)
    #                     glVertex2f(x1, y1)
    #                     glVertex2f(x2, y2)
    #                     glVertex2f(x3, y3)
    #                     glVertex2f(x4, y4)
    #                     glEnd()  # 结束绘制线段

    for i in range(len(sub_element_junction)):
        shape = sub_element_junction[i].getAttribute("shape")
        shape_list = shape.split(" ")

        glLineWidth(10)
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
    return image

    # cv2.imwrite("tsinghua_total_test.jpg", image )
    # cv2.imwrite("test1.jpg", image)

# image = cv2.imread("tsinghua.jpg")
# render_map()
glutDisplayFunc(render_map)
glutMainLoop()



