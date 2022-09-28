import cv2 as cv
import numpy as np
import time
from tkinter import *  
  
from tkinter import messagebox  
  
 
index = 1

#loading the test image
img = cv.imread("tld_img/1.jpg") #change name to test new image



#..............................DETECTION.................................




#funcion for reducing resolution of the image:
def re_sc(frame, scale=0.75):
  width= int(frame.shape[1]*scale)
  height= int(frame.shape[0]*scale)
  dimention = (width,height)
  return cv.resize(frame, dimention, interpolation= cv.INTER_AREA)



#calling funcion to rescale image:
img_r = re_sc(img)



#cropping the image:
cropped = img_r[0:200, 0:800]
#cv.imshow("cropped", cropped)

blank= np.zeros(cropped.shape)



#converting the colorspace from bgr to lab:
lab = cv.cvtColor(cropped, cv.COLOR_BGR2LAB)
#cv.imshow("TLD_con",lab)



#blurring the image:
blur=cv.GaussianBlur(lab,(7,7), cv.BORDER_DEFAULT)
#cv.imshow('blur',blur)




#edge detction:
edge=cv.Canny(blur, 125,175)
#cv.imshow('b',edge)



#contours
contours, hierarchies = cv.findContours(edge, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contours(s) found!')



contours= sorted(contours, key=lambda x:cv.contourArea(x), reverse=True)

'''cv.drawContours(blank, contours, -1, (0,255,0),1)
cv.imshow('contour',blank)
blank= np.zeros(cropped.shape)'''

contv=0
diff=0
hdiff=10
for cont in contours:
  contv=contv+1
  (x, y, w, h) = cv.boundingRect(cont)
  diff=w-h
  
  if diff<0:
    diff=diff*-1
    
  if diff<hdiff:
    hdiff=diff
    index=contv-1
  if contv==5:
    break
'''cv.drawContours(blank, contours, -1, (0,255,0),1)
cv.imshow('contour',blank)
blank= np.zeros(cropped.shape)'''



'''for cont in contours:
  (x, y, w, h) = cv.boundingRect(cont)
  cv.rectangle(cropped, (x,y), (x + w, y + h),(0,255,0),2)
cv.imshow("crp_der", cropped)'''



#...........................intermidiate output...............................
'''

cv.imshow("CROPPED_IMG", cropped)                             

cv.imshow("COLOUR_SPACE_CONVERSION",lab)                    

cv.imshow('GAUSSIAN_BLUR_IMG',blur)

cv.imshow('EDGE_DETECTION',edge)

cv.drawContours(blank, contours, -1, (0,255,0),1)
cv.imshow('CONTOURS',blank)
blank= np.zeros(cropped.shape)
'''
#..............................DETECTED OUTPUT...............................


(x, y, w, h) = cv.boundingRect(contours[index])
xt=x-5
yt=y-5
cv.rectangle(cropped, (xt,yt), (xt + w+10, yt + h+10),(0,255,0),2)
cv.imshow("OUTPUT", cropped)



#..............................classification.................................



cx = x + (w/2)
cy = y + (h/2)

cx = int(cx)
cy = int(cy)

#print(cx)
#print(cy)

#print(img_r[cy][cx])

#colour detection logic:

r=int (img_r[cy][cx][2])
g=int (img_r[cy][cx][1])
b=int (img_r[cy][cx][0])

cv.imshow('FINAL_OUTPUT',img_r)


#................................ROI.............................

'''for cont in contours:
  (x, y, w, h) = cv.boundingRect(cont)
  cv.rectangle(cropped, (x,y), (x + w, y + h),(0,255,0),2)
cv.imshow("DETECTED SHAPES",cropped)'''


#............................colour index.........................
print('\n')
#red index
bg_avg = (g + b)/2
red = r - bg_avg
#if red<0:
  #red=0
print('RED INDEX:')
print(red)
print('\n')


#yellow index
bg_avg = (g + r)/2
yellow =  bg_avg - b
#if yellow<0:
  #yellow=0
print('YELLOW INDEX:')
print(yellow)
print('\n')


#green index
bg_avg = (r + b)/2
green = g - bg_avg
#if green<0:
  #green=0
print('GREEN INDEX:')
print(green)
print('\n')


top = Tk()  
  
top.geometry("200x00")      
  

  


#printing colour
if red >= yellow:
  if red > green:
    print("red")
    messagebox.showinfo("information","TRAFFIC LIGHT COLOUR IS: Red stop the vehicle")  
  else:
    print("green")
    messagebox.showinfo("information","TRAFFIC LIGHT COLOUR IS: Green ")  
elif yellow > green:
  print("yellow")
  messagebox.showinfo("information","TRAFFIC LIGHT COLOUR IS: Yellow slow down the vehicle")  
else:
  print("green")
  messagebox.showinfo("information","TRAFFIC LIGHT COLOUR IS: Green")  

top.mainloop() 
cv.waitKey(0)






















