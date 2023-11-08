import cv2
import numpy as np
import qrcode
import utils
import json

###
width_img = 700
height_img = 700
questions = 5
answers = 5
right_ans = [1, 2, 0, 1, 4]
###

img = cv2.imread('sheet.png')
img = cv2.resize(img, (width_img, height_img))
img_contours = img.copy()
img_biggest_contours = img.copy()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
img_canny = cv2.Canny(img_blur, 10, 50)


contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 5)
rect_contours = utils.rectangle_contour(contours)
biggest_contour = utils.get_corner_points(rect_contours[0])
grade_points = utils.get_corner_points(rect_contours[1])

if biggest_contour.size != 0 and grade_points.size != 0:
    cv2.drawContours(img_biggest_contours, biggest_contour, -1, (0, 255, 0), 20)
    cv2.drawContours(img_biggest_contours, grade_points, -1, (0, 0, 0), 20)

    biggest_contour = utils.reorder(biggest_contour)
    grade_points = utils.reorder(grade_points)

    p1_ans = np.float32(biggest_contour)
    p2_ans = np.float32([[0, 0], [width_img, 0], [0, height_img], [width_img, height_img]])
    matrix_ans = cv2.getPerspectiveTransform(p1_ans, p2_ans)
    img_warp_colored_ans = cv2.warpPerspective(img, matrix_ans, (width_img, height_img))

    p1_grd = np.float32(grade_points)
    p2_grd = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
    matrix_grd = cv2.getPerspectiveTransform(p1_grd, p2_grd)
    img_warp_colored_grd = cv2.warpPerspective(img, matrix_grd, (325, 150))

    img_warp_gray_ans = cv2.cvtColor(img_warp_colored_ans, cv2.COLOR_BGR2GRAY)
    img_thresh_ans = cv2.threshold(img_warp_gray_ans, 180, 255, cv2.THRESH_BINARY_INV)[1]

    boxes = utils.split_boxed(img_thresh_ans, questions, answers)

    pixel_values = np.zeros((questions, answers))
    columns = 0
    rows = 0
    for image in boxes:
        total_pixels = cv2.countNonZero(image)
        pixel_values[rows][columns] = total_pixels
        columns += 1
        if columns == answers:
            rows += 1
            columns = 0

    index = []
    for x in range(0, questions):
        arr = pixel_values[x]
        index_value = np.where(arr == np.amax(arr))
        index.append(index_value[0][0])

    grading = []
    for x in range(0, questions):
        if right_ans[x] == index[x]:
            grading.append(1)
        else:
            grading.append(0)
    score = f'{sum(grading)}/{answers}'

    final_img = img_warp_colored_ans.copy()
    final_img = utils.show_answers(final_img, index, grading, right_ans, questions, answers)

    img_raw_drawing = np.zeros_like(img_warp_colored_ans)
    img_raw_drawing = utils.show_answers(img_raw_drawing, index, grading, right_ans, questions, answers)
    inverse_matrix_ans = cv2.getPerspectiveTransform(p2_ans, p1_ans)
    inverse_img_warp_colored_ans = cv2.warpPerspective(img_raw_drawing, inverse_matrix_ans, (width_img, height_img))

    qr_data = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = {
        'questions': questions,
        'choices': answers,
        'right_ans': right_ans
    }
    str_data = json.dumps(data)
    qr_data.add_data(utils.encrypt(str_data))
    qr_data.make()
    qrcode = qr_data.make_image(fill_color="white", back_color="black")
    qrcode.save('qr.png')
    qr = cv2.imread('qr.png')
    qr = cv2.resize(qr, (350, 350))

    img_raw_grade = np.zeros_like(img_warp_colored_grd)
    # cv2.putText(img_raw_grade, score, (50, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 3)
    inverse_matrix_grd = cv2.getPerspectiveTransform(p2_grd, p1_grd)
    inverse_img_warp_colored_grd = cv2.warpPerspective(qr, inverse_matrix_grd, (width_img, height_img))

    result_img = img.copy()
    result_img = cv2.addWeighted(result_img, 1, inverse_img_warp_colored_ans, 1, 0)
    result_img = cv2.addWeighted(result_img, 1, inverse_img_warp_colored_grd, 1, 0)

    qr_code_detector = cv2.QRCodeDetector()
    decodedText, _, _ = qr_code_detector.detectAndDecode(result_img)
    print(json.loads(utils.decrypt(decodedText)))

    cv2.imshow('Original', result_img)
    cv2.waitKey(0)
