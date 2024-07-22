import numpy as np
import cv2
# from tkinter.filedialog import askopenfilename, askdirectory
from utils import (
    sort_pts,
    get_closest_point_index,
    screen_web_page
)

class ImgLoader:
    def __init__(
            self,
            path_base_img   : str,
            path_output_img : str = "./", 
    ) -> None:
        self.path_base_img   = path_base_img
        self.path_output_img = path_output_img
        self.base_image      = cv2.imread("./base.jpg")
        self.base_image_copy = self.base_image.copy()
        self.points          = []

    def update_output_path(
        self,
        new_output_path : str
    ) -> None:
        self.path_output_img = new_output_path


    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.base_image_copy, (x,y), 4, (0,0,255), -1)
            self.points.append([x, y])
            if len(self.points) <= 4:
                cv2.imshow('image', self.base_image_copy)

    def init_points(self) -> None:
        cv2.imshow('image', self.base_image_copy)
        cv2.setMouseCallback('image', self.click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        self.points = sort_pts(self.points)
        self.h_base, self.w_base, self.c_base = self.base_image.shape


    def click_update_event(self, event, x, y, flags, params) -> None:
        
        if event == cv2.EVENT_LBUTTONDOWN:
            closest_point_index = get_closest_point_index(self.points, [x, y])
            self.points[closest_point_index] = [x,y]
            self.render_box()
   
    def render_box(self) -> None:
        self.base_image_copy = self.base_image.copy()

        for i in range(len(self.points)):
            curr_point = (self.points[i][0],self.points[i][1])
            cv2.circle(self.base_image_copy, curr_point, 4, (0,0,255), -1)
            
        cv2.line(self.base_image_copy, (self.points[0][0],self.points[0][1]), (self.points[1][0],self.points[1][1]), (0,0,255), 1)
        cv2.line(self.base_image_copy, (self.points[1][0],self.points[1][1]), (self.points[2][0],self.points[2][1]), (0,0,255), 1)
        cv2.line(self.base_image_copy, (self.points[2][0],self.points[2][1]), (self.points[3][0],self.points[3][1]), (0,0,255), 1)
        cv2.line(self.base_image_copy, (self.points[3][0],self.points[3][1]), (self.points[0][0],self.points[0][1]), (0,0,255), 1)
        cv2.imshow('image', self.base_image_copy)

    def adjust_points(self) -> None:
        self.render_box()
        cv2.setMouseCallback('image', self.click_update_event)
        cv2.waitKey(0)

    
    def insert_img(self, img_path : str) -> str:
        subject_image = cv2.imread(img_path)
        h_subject, w_subject = subject_image.shape[:2]

        pts1 = np.float32([[0, 0], [w_subject, 0], [w_subject, h_subject], [0, h_subject]])
        pts2 = np.float32(self.points)

        transformation_matrix = cv2.getPerspectiveTransform(pts1, pts2)
        warped_img = cv2.warpPerspective(subject_image, transformation_matrix, (self.w_base, self.h_base))

        mask = np.zeros(self.base_image.shape, dtype=np.uint8)
        roi_corners = np.int32(self.points)
        
        filled_mask = mask.copy()
        cv2.fillConvexPoly(filled_mask, roi_corners, (255, 255, 255))

        inverted_mask = cv2.bitwise_not(filled_mask)

        masked_image = cv2.bitwise_and(self.base_image, inverted_mask)
        output = cv2.bitwise_or(warped_img, masked_image)
        cv2.resize(output, (int(0.2 * self.w_base), int(0.2 * self.h_base)))

        name_result = self.path_output_img + "output_" + img_path.split("/")[-1]
        cv2.imwrite(name_result, output)
        cv2.destroyAllWindows()
        return name_result

    def create_overlayed_image_from_website(
        self,
        website_url      : str,
        path_website_img : str = "tmp_website.png"
    ) -> None:
        screen_web_page(website_url, path_website_img)
        return self.insert_img(path_website_img)



#path_base_img = askopenfilename(title= 'Select the background image')
#path_dir_subjects = askdirectory(title= 'Select the directory of the subject images')
# path_base_img = "./base.jpg"
# imgLoader = ImgLoader(path_base_img)
# imgLoader.init_points()
# imgLoader.adjust_points()
# imgLoader.insert_img("./subjects/Karimou.png")

# imgLoader.create_overlayed_image("https://sideral.ai")

# quit()