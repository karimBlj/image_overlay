import numpy as np
import cv2
from typing import List, Tuple

def sort_pts(points):
    sorted_pts = np.zeros((4, 2), dtype="float32")
    s = np.sum(points, axis=1)
    sorted_pts[0] = points[np.argmin(s)]
    sorted_pts[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    sorted_pts[1] = points[np.argmin(diff)]
    sorted_pts[3] = points[np.argmax(diff)]

    return sorted_pts

class ImgLoader:
    def __init__(self, path_base_img : str):
        self.path_base_img = path_base_img
        self.base_image = cv2.imread("./base.jpg")
        self.base_image_copy = self.base_image.copy()
        self.points = []


    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.base_image_copy, (x,y), 4, (0,0,255), -1)
            self.points.append([x, y])
            if len(self.points) <= 4:
                cv2.imshow('image', self.base_image_copy)

    def init_points(self):
        cv2.imshow('image', self.base_image_copy)
        cv2.setMouseCallback('image', self.click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        self.sorted_pts = sort_pts(self.points)
        self.h_base, self.w_base, self.c_base = self.base_image.shape


    def insert_img(self, img_path : str):
        subject_image = cv2.imread(img_path)

        
        #cv2.imshow("test", subject_image)
        h_subject, w_subject = subject_image.shape[:2]

        pts1 = np.float32([[0, 0], [w_subject, 0], [w_subject, h_subject], [0, h_subject]])
        pts2 = np.float32(self.sorted_pts)

        # Get the transformation matrix and use it to get the warped image of the subject
        transformation_matrix = cv2.getPerspectiveTransform(pts1, pts2)
        warped_img = cv2.warpPerspective(subject_image, transformation_matrix, (self.w_base, self.h_base))

        # Create a mask
        mask = np.zeros(self.base_image.shape, dtype=np.uint8)
        roi_corners = np.int32(self.sorted_pts)
        
        # Fill in the region selected with white color
        filled_mask = mask.copy()
        cv2.fillConvexPoly(filled_mask, roi_corners, (255, 255, 255))

        # Invert the mask color
        inverted_mask = cv2.bitwise_not(filled_mask)

        # Bitwise AND the mask with the base image
        masked_image = cv2.bitwise_and(self.base_image, inverted_mask)



        # Using Bitwise OR to merge the two images
        output = cv2.bitwise_or(warped_img, masked_image)
        # cv2.imshow('Fused Image', output)
        name_result = "output_" + img_path[:-4] + ".png"
        cv2.imwrite(name_result, output)
        # cv2.waitKey(0)
        cv2.destroyAllWindows()


imgLoader = ImgLoader("./base.jpg")
imgLoader.init_points()
imgLoader.insert_img("./subjects/Karimou.png")
print("IMG WRITTEN")