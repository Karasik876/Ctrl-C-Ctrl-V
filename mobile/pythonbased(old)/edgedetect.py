from kivy.clock import mainthread
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
import numpy as np
import cv2
from camera4kivy import Preview
import utils


class EdgeDetect(Preview):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzed_texture = None

    ####################################
    # Analyze a Frame - NOT on UI Thread
    ####################################

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
        # pixels : analyze pixels (bytes)
        # image_size   : analyze pixels size (w,h)
        # image_pos    : location of Texture in Preview (due to letterbox)
        # scale  : scale from Analysis resolution to Preview resolution
        # mirror : true if Preview is mirrored
        
        img = np.fromstring(pixels, np.uint8).reshape(image_size[1], image_size[0], 4)
        # Note, analyze_resolution changes the result. Because with a smaller
        # resolution the gradients are higher and more edges are detected.

        width_img = 700
        height_img = 700
        ###
        questions = 10
        choices = 5
        right_ans = [1, 2, 0, 1, 4, 3, 4, 2, 3, 0]
        ###

        # img = cv2.resize(img, (width_img, height_img))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
        img_canny = cv2.Canny(img_blur, 10, 50)
        try:
            contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            rect_contours = utils.rectangle_contour(contours)
            biggest_contour = utils.get_corner_points(rect_contours[0])
            second_contour = utils.get_corner_points(rect_contours[1])

            if biggest_contour.size != 0:
                # biggest_contour = utils.reorder(biggest_contour)
                #
                # p1_ans = np.float32(biggest_contour)
                # p2_ans = np.float32([[0, 0], [width_img, 0], [0, height_img], [width_img, height_img]])
                # matrix_ans = cv2.getPerspectiveTransform(p1_ans, p2_ans)
                # img_warp_colored_ans = cv2.warpPerspective(img, matrix_ans, (width_img, height_img))
                #
                # img_warp_gray_ans = cv2.cvtColor(img_warp_colored_ans, cv2.COLOR_BGR2GRAY)
                # img_thresh_ans = cv2.threshold(img_warp_gray_ans, 150, 255, cv2.THRESH_BINARY_INV, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
                #
                # boxes = utils.split_boxed(img_thresh_ans, questions, choices)
                #
                # pixel_values = np.zeros((questions, choices))
                # columns = 0
                # rows = 0
                # for image in boxes:
                #     total_pixels = cv2.countNonZero(image)
                #     pixel_values[rows][columns] = total_pixels
                #     columns += 1
                #     if columns == choices:
                #         rows += 1
                #         columns = 0
                #
                # index = []
                # for x in range(0, questions):
                #     arr = pixel_values[x]
                #     index_value = np.where(arr == np.amax(arr))
                #     index.append(index_value[0][0])
                #
                # grading = []
                # for x in range(0, questions):
                #     if right_ans[x] == index[x]:
                #         grading.append(1)
                #     else:
                #         grading.append(0)
                #
                # img_raw_drawing = np.zeros_like(img_warp_colored_ans)
                # img_raw_drawing = utils.show_answers(img_raw_drawing, index, grading, right_ans, questions, choices)
                # inverse_matrix_ans = cv2.getPerspectiveTransform(p2_ans, p1_ans)
                # inverse_img_warp_colored_ans = cv2.warpPerspective(img_raw_drawing, inverse_matrix_ans,
                #                                                    (width_img, height_img))

                img_raw = np.zeros_like(img)
                img_raw = utils.show_corners(img_raw, biggest_contour, second_contour)
                result_img = img.copy()
                result_img = cv2.addWeighted(result_img, 1, img_raw, 1, 0)
                # result_img = cv2.addWeighted(result_img, 1, inverse_img_warp_colored_ans, 1, 0)
                # result_img = cv2.resize(result_img, (image_size[0], image_size[1]))
                pixels = result_img.tostring()
        except Exception as e:
            pixels = img.tostring()

        self.make_thread_safe(pixels, image_size)

    @mainthread
    def make_thread_safe(self, pixels, size):
        if not self.analyzed_texture or\
           self.analyzed_texture.size[0] != size[0] or\
           self.analyzed_texture.size[1] != size[1]:
            self.analyzed_texture = Texture.create(size=size, colorfmt='rgba')
            self.analyzed_texture.flip_vertical()
        if self.camera_connected:
            self.analyzed_texture.blit_buffer(pixels, colorfmt='rgba') 
        else:
            # Clear local state so no thread related ghosts on re-connect
            self.analyzed_texture = None
            
    ################################
    # Annotate Screen - on UI Thread
    ################################

    def canvas_instructions_callback(self, texture, tex_size, tex_pos):
        # texture : preview Texture
        # size    : preview Texture size (w,h)
        # pos     : location of Texture in Preview Widget (letterbox)
        # Add the analyzed image
        if self.analyzed_texture:
            Color(1, 1, 1, 1)
            Rectangle(texture=self.analyzed_texture, size=tex_size, pos=tex_pos)










