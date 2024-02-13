import cv2
import os
import numpy as np

def mark_rectangles(image):

    if image is None:
        print("Image not found. Please provide a valid image path.")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 2)

 
    edges = cv2.Canny(gray, 50, 150)

 
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    marked_image = image.copy()

    for contour in contours:
       
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        if cv2.contourArea(contour) > 100:
            cv2.drawContours(marked_image, [box], 0, (0,255,0), 4)  

    return marked_image
    

def mark_triangles(image):
    if image is None:
        print("Image not found. Please provide a valid image path.")
        return

 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  
    gray = cv2.GaussianBlur(gray, (9, 9), 2)

 
    edges = cv2.Canny(gray, 50, 150)


    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    marked_image = image.copy()

    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # If the polygon has 3 vertices, it's a triangle
        if len(approx) == 3:
            cv2.drawContours(marked_image, [contour], 0, (0,255,0), 4)  # Mark in red

    return marked_image


def mark_circles(image):
    if image is None:
        print("Image not found. Please provide a valid image path.")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    gray = cv2.GaussianBlur(gray, (9, 9), 2)

 
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1,  
        minDist=70,  
        param1=70,  
        param2=70, 
        minRadius=0,  
        maxRadius=100  
    )

   
    if circles is not None:
        
        circles = circles.astype(int)

        
        for circle in circles[0, :]:
            x, y, radius = circle
            x, y, radius = int(x), int(y), int(radius)
            cv2.circle(image, (x, y), radius, (0,255,0), 4)  

       
        return image
    else:
        print("No circular signs found in the image.")
        return image

def display_image(image):
    cv2.imshow('detected signs', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detect_sign(image):
    image=mark_rectangles(image)
    image=mark_triangles(image)
    image=mark_circles(image)
    display_image(image)


def main(): 
    print("program for marking all the traffic signs") 
    image_path='tt.jpg'
    image=cv2.imread(image_path)
    detect_sign(image) 

   
if __name__=="__main__": 
    main() 