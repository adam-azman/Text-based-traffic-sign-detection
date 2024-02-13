import cv2
import os
import numpy as np

def crop_circles(image_path):
   
    image = cv2.imread(image_path)
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

        
        path = r'croppedImages/'

       
        for i, circle in enumerate(circles[0, :], start=1):
            x, y, radius = circle
            x, y, radius = int(x), int(y), int(radius)       
            cropped_circle = image[y - radius:y + radius, x - radius:x + radius]

            output_path = os.path.join(path, f'circle_{i}.jpg')
            cv2.imwrite(output_path, cropped_circle)

            print(f"Saved sign(circle) {i} to {output_path}")

    else:
        print("No circles found in the image.")


def crop_and_save_triangles(image_path):
  
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found. Please provide a valid image path.")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

 
    gray = cv2.GaussianBlur(gray, (9, 9), 2)

    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    path = r'croppedImages/'

    for i, contour in enumerate(contours, start=1):

        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 3:
            x, y, w, h = cv2.boundingRect(contour)

            # Crop the triangle
            cropped_triangle = image[y:y+h, x:x+w]

            output_path = os.path.join(path,f'triangle_{i}.jpg')
            cv2.imwrite(output_path, cropped_triangle)

            print(f"Saved sign(triangle) {i} to {output_path}")

         

def crop_and_save_rectangles(image_path):
 
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found. Please provide a valid image path.")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 2)

    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   
    path = r'croppedImages/'

    for i, contour in enumerate(contours, start=1):
   
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        if cv2.contourArea(contour) > 100:
            x, y, w, h = cv2.boundingRect(contour)

            cropped_rectangle = image[y:y+h, x:x+w]

            output_path =os.path.join(path, f'rectangle_{i}.jpg')
            cv2.imwrite(output_path, cropped_rectangle)

            print(f"Saved sign(rectangle) {i} to {output_path}")



def crop_sign(image_path):
	crop_circles(image_path)
	crop_and_save_triangles(image_path)
	crop_and_save_rectangles(image_path)
    


def main(): 
    print("program for cropping all the traffic signs") 
    image_path='tt.jpg'
    crop_sign(image_path) 

   
if __name__=="__main__": 
    main() 
