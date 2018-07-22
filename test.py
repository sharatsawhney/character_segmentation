import cv2
import numpy as np

img = cv2.imread('data/vedantu-1.png',1)
height = img.shape[0]
width = img.shape[1]
src_img = cv2.resize(img, dsize =(1320, int(1320*height/width)), interpolation = cv2.INTER_AREA)
height = src_img.shape[0]
width = src_img.shape[1]
grey_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
bin_img = cv2.adaptiveThreshold(grey_img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,21,20)
coords = np.column_stack(np.where(bin_img > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle
h = bin_img.shape[0]
w = bin_img.shape[1]
center = (w//2,h//2)
M = cv2.getRotationMatrix2D(center,angle,1.0)
bin_img = cv2.warpAffine(bin_img,M,(w,h),
                         flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
kernel1 = np.array([[1,0,1],[0,1,0],[1,0,1]], dtype = np.uint8)
final_thr = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)


count_x = np.zeros(shape= (height))
for y in range(height):
    for x in range(width):
        if bin_img[y][x] == 255 :
            count_x[y] = count_x[y]+1

local_minima = []
for y in range(len(count_x)):
    if y >= 10 and y <= len(count_x)-11:
        arr1 = count_x[y-10:y+10]
    elif y < 10:
        arr1 = count_x[0:y+10]
    else:
        arr1 = count_x[y-10:len(count_x)-1]
    if min(arr1) == count_x[y]:
        local_minima.append(y)

final_local = []
init = []
end = []
for z in range(len(local_minima)):
    if z != 0 and z!= len(local_minima)-1:
        if local_minima[z] != (local_minima[z-1] +1) and local_minima[z] != (local_minima[z+1] -1):
            final_local.append(local_minima[z])
        elif local_minima[z] != (local_minima[z-1] + 1) and local_minima[z] == (local_minima[z+1] -1):
            init.append(local_minima[z])
        elif local_minima[z] == (local_minima[z-1] + 1) and local_minima[z] != (local_minima[z+1] -1):
            end.append(local_minima[z])
    elif z == 0:
        if local_minima[z] != (local_minima[z+1]-1):
            final_local.append(local_minima[z])
        elif local_minima[z] == (local_minima[z+1]-1):
            init.append(local_minima[z])
    elif z == len(local_minima)-1:
        if local_minima[z] != (local_minima[z-1]+1):
            final_local.append(local_minima[z])
        elif local_minima[z] == (local_minima[z-1]+1):
            end.append(local_minima[z])
for j in range(len(init)):
    mid = (init[j] + end[j])/2
    if (mid % 1) != 0:
        mid = mid+0.5
    final_local.append(int(mid))

final_local = sorted(final_local)

no_of_lines = len(final_local) - 1
lines_img = []

for i in range(no_of_lines):
    lines_img.append(bin_img[final_local[i]:final_local[i+1], :])
    cv2.imshow('img',bin_img[final_local[i]:final_local[i+1], :])
    cv2.waitKey(0)
