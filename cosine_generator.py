import numpy as np
import cv2
import math
import time

image_width = 1080
image_height = 600
exit = False

img = np.zeros((image_height, image_width, 3), np.uint8)
vid_rec = cv2.VideoWriter('CoSine_Generator.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 30, (image_width, image_height))

def angle_to_coordinates(origin_x, origin_y, angle_degree, radius):
    '''
    [P] given origin (x,y) , radious (r), angle (θ) find point (u,v) on circle to connect (x,y) ---r--> (u,v)
    [S] The point (0,r) ends up at u = r * sin(θ), v = r * cos(θ)
    '''
    coordinate = (0,0)
    point_u = radius*math.sin(math.radians(angle_degree))
    point_v = radius*math.cos(math.radians(angle_degree))
    coordinate = (int(origin_x+point_u), int(origin_y-point_v)) #clock wise -> [+,-] and [-,-], #anticlock = [+,+] and [-,-]
    return coordinate

def marker_sphere_line(_layer, mouse_x, mouse_y, radius, num_of_line, color=(132,123,100), thickness=2, linetype=cv2.LINE_AA):     
    angle = (360/num_of_line)  
    _angle = angle 
    for line in range(num_of_line):
        atc = angle_to_coordinates(mouse_x, mouse_y, angle, radius)
        cv2.line(_layer, (mouse_x, mouse_y), atc, color, thickness, linetype)                   
        angle += _angle
    return _layer

def render_generator_cross(frame, center, radius, color):
    vline = ((center[0],center[1]-radius),(center[0], center[1]+radius))
    hline = ((center[0]-radius,center[1]),(center[0]+radius, center[1]))
    cv2.line(img=frame, pt1=vline[0], pt2=vline[1], color=color, thickness=2, lineType=cv2.LINE_AA)
    cv2.line(img=frame, pt1=hline[0], pt2=hline[1], color=color, thickness=2, lineType=cv2.LINE_AA)
    return frame

def render_generator_circle(frame, center, radius, color):
    cv2.circle(img=frame, center=center, radius=radius, color=color, thickness=2, lineType=cv2.LINE_AA)
    frame = render_generator_cross(frame, center, radius, color)
    return frame

def process_mouse_event(event, x, y, flags, cntr):
    clone = np.zeros((image_height, image_width, 3), np.uint8)
    clone = render_generator_circle(clone, (350, 350), 200, (132,123,100))
    clone = marker_sphere_line(clone, 350, 350, 200, 180)
    if event == cv2.EVENT_MOUSEMOVE:
        cv2.putText(clone, str(f"({x},{y})"), (x,y), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(132,12,120),thickness=2, lineType=cv2.LINE_AA)
        cv2.line(clone, pt1=(350,350), pt2=(x,y),color=(132,132,132), thickness=2, lineType=cv2.LINE_AA)
    cv2.imshow('image', clone) 

cntr = 0

while True:
    # frame = np.zeros((image_height, image_width, 3), np.uint8)
    cntr +=1 
    num_of_line = 360
    radius = 150
    mouse_x = 200
    mouse_y = 300
    center = (mouse_x+300, mouse_y)
    graph_norm_ax = 500
    angle = (360/num_of_line)  
    _angle = angle 
    seg_points = []
    for line in range(num_of_line):
        frame = np.zeros((image_height, image_width, 3), np.uint8)

        atc = angle_to_coordinates(mouse_x, mouse_y, angle, radius)
        cv2.line(frame, (mouse_x, mouse_y), atc, (132,132,132), thickness=2, lineType=cv2.LINE_AA)

        vline = ((center[0],center[1]-radius),(center[0], center[1]+radius))
        hline = ((center[0],center[1]),(center[0]+graph_norm_ax, center[1]))
        cv2.line(img=frame, pt1=hline[0], pt2=hline[1], color=(132,123,100), thickness=2, lineType=cv2.LINE_AA)
        cv2.line(img=frame, pt1=vline[0], pt2=vline[1], color=(132,123,100), thickness=2, lineType=cv2.LINE_AA)

        frame = render_generator_circle(frame, (mouse_x, mouse_y), radius, (132,123,100))          

        seg_points.append([500+line,atc[1]])
        poly_img = cv2.polylines(frame, np.array([seg_points]), False, (132,123,100), thickness=2, lineType=cv2.LINE_AA)
        cv2.line(img=frame, pt1=atc, pt2=(500+line, atc[1]), color=(132,123,100), thickness=2, lineType=cv2.LINE_AA)
        cv2.circle(frame, atc, 5, (255,255,0), -1, cv2.LINE_AA)
        cv2.circle(frame, (500+line, atc[1]), 5, (255,255,0), -1, cv2.LINE_AA)

        # cv2.putText(frame, str(f"{cntr}"), (50,50), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(132,12,120),thickness=2, lineType=cv2.LINE_AA)
        angle += _angle
        time.sleep(0.007)
        cv2.imshow("Frame", frame)
        vid_rec.write(frame)
        key = cv2.waitKey(1) & 0xFF
        if cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) <1 or key == ord("q"):
            exit = True
            break
        
    cv2.imshow("Frame", frame)
    vid_rec.write(frame)
    key = cv2.waitKey(1) & 0xFF
    if cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) <1 or key == ord("q") or exit:
        break

vid_rec.release()
cv2.destroyAllWindows()
