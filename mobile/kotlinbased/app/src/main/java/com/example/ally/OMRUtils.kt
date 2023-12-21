package com.example.ally

import android.graphics.Bitmap
import io.matthewnelson.encoding.base32.Base32
import io.matthewnelson.encoding.base32.Base32Default
import io.matthewnelson.encoding.core.Decoder.Companion.decodeToByteArray
import io.matthewnelson.encoding.core.Decoder.Companion.decodeToByteArrayOrNull
import io.matthewnelson.encoding.core.EncodingException
import org.opencv.android.Utils
import org.opencv.core.Core
import org.opencv.core.CvType
import org.opencv.core.Mat
import org.opencv.core.MatOfPoint
import org.opencv.core.MatOfPoint2f
import org.opencv.core.Scalar
import org.opencv.core.Size
import org.opencv.imgproc.Imgproc
import org.opencv.core.Point
import org.opencv.core.Rect
import org.opencv.objdetect.Objdetect
import org.opencv.objdetect.QRCodeDetector

class OMRUtils {

    fun proccessOmr(bitmap: Bitmap) : Bitmap {
        val mat = Mat()
        Utils.bitmapToMat(bitmap, mat)
        val canny = mat.clone()
//        val borders = mat.clone()
        val result = mat.clone()
        val weightRes = mat.clone()
        val dstMat = mat.clone()
        val resultAns: Mat
        val warp = mat.clone()
        val warpColored = warp.clone()
        val boxes: MutableList<Mat>
        val contours = mutableListOf<MatOfPoint>()

        Imgproc.cvtColor(canny, canny, Imgproc.COLOR_BGR2GRAY)
        Imgproc.GaussianBlur(canny, canny, Size(5.0, 5.0), 1.0)
        Imgproc.Canny(canny, canny, 10.0, 50.0)

        val qrCodeDetector = QRCodeDetector()
        val text = qrCodeDetector.detectAndDecode(mat)

        try {
            Imgproc.findContours(canny, contours, canny, Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE)

            val rectContours = rectangleContour(contours)
            val sheetContour2f = getCornerPoints(rectContours[0])
            val sheetContour = convertMatOfPoint(getCornerPoints(rectContours[0]))
            val nameContour = convertMatOfPoint(getCornerPoints(rectContours[1]))

//            Imgproc.drawContours(borders, sheetContour, -1, Scalar(0.0, 0.0, 255.0), 5)
//            Imgproc.drawContours(borders, nameContour, -1, Scalar(0.0, 0.0, 255.0), 5)
            if (sheetContour.isNotEmpty() && nameContour.isNotEmpty() && text.isNotEmpty()) {

                val decodedBytes = try {
                    text.decodeToByteArrayOrNull(Base32.Default)
                } catch (e: EncodingException) {
                    null
                }
                val str = String(decodedBytes!!)
                val questions = str.split(';')[0].toInt()
                val choices = str.split(';')[1].toInt()
                val answers = str.split(';')[2].split(',').map { it.toInt() }

                val cords = sheetContour2f.toList().sortedWith(compareBy {it.x + it.y})

                val src = Mat(4, 1, CvType.CV_32FC2)
                src.put(0, 0,
                    cords[0].x, cords[0].y,
                    cords[1].x, cords[1].y,
                    cords[2].x, cords[2].y,
                    cords[3].x, cords[3].y
                )

                val dst = Mat(4, 1, CvType.CV_32FC2)
                dst.put(0, 0,
                    0.0, 0.0,
                    mat.size().width, 0.0,
                    0.0, mat.size().height,
                    mat.size().width, mat.size().height)

                val perspectiveTransform = Imgproc.getPerspectiveTransform(src, dst)

                Imgproc.warpPerspective(result, warp, perspectiveTransform, Size(mat.size().width, mat.size().height))
                Imgproc.cvtColor(warp, warpColored, Imgproc.COLOR_BGR2GRAY)
                Imgproc.threshold(warpColored, warpColored, 130.0, 255.0, Imgproc.THRESH_BINARY_INV)

                boxes = splitBoxed(warpColored, questions, choices, warp.rows() / questions, warp.cols() / choices)

                val pixelValues = Array(questions) { DoubleArray(choices) }
                var columns = 0
                var rows = 0

                for (image in boxes) {
                    val totalPixels = Core.countNonZero(image)
                    pixelValues[rows][columns] = totalPixels.toDouble()
                    columns++
                    if (columns == choices) {
                        rows++
                        columns = 0
                    }
                }

                val index = mutableListOf<Int>()
                for (x in 0 until questions) {
                    val arr = pixelValues[x]
                    val indexValue = arr.indexOfFirst { it == arr.maxOrNull() }
                    index.add(indexValue)
                }

                val grading = mutableListOf<Int>()
                for (x in 0 until questions) {
                    grading.add(if (answers[x] == index[x]) 1 else 0)
                }

                resultAns = showAnswers(warp, index, grading, answers, questions, choices)

                val inversePerspectiveTransform = Imgproc.getPerspectiveTransform(dst, src)

                Imgproc.warpPerspective(resultAns, dstMat, inversePerspectiveTransform, Size(mat.size().width, mat.size().height))
                Core.addWeighted(weightRes, 0.3, dstMat, 0.7, 0.0, weightRes)
            }
        } catch (_: Exception){  }
        Utils.matToBitmap(weightRes, bitmap)
        return bitmap
    }

    private fun showAnswers(img: Mat, index: List<Int>, grading: List<Int>, answers: List<Int>, questions: Int, choices: Int): Mat {
        val secW = img.cols() / choices
        val secH = img.rows() / questions
        val diam = secH / 2

        for (x in 0 until questions) {
            val ans = index[x]
            val cX = (ans * secW) + secW / 2.0
            val cY = (x * secH) + secH / 2.0

            val repColor: Scalar = if (grading[x] >= 1) Scalar(0.0, 255.0, 0.0) else Scalar(255.0, 0.0, 0.0)

            Imgproc.circle(img, Point(cX, cY), diam, repColor, Core.FILLED)

            if (grading[x] == 0) {
                Imgproc.circle(img, Point(answers[x] * secW + secW / 2.0, x * secH + secH / 2.0),
                    diam, Scalar(0.0, 0.0, 255.0), Core.FILLED)
            }
        }

        return img
    }

    private fun splitBoxed(image: Mat, numRows: Int, numCols: Int, pieceHeight: Int, pieceWidth: Int): MutableList<Mat> {
        val pieces = mutableListOf<Mat>()

        for (i in 0 until numRows) {
            for (j in 0 until numCols) {
                val roi = Rect(j * pieceWidth, i * pieceHeight, pieceWidth, pieceHeight)
                val piece = Mat(image, roi).clone()
                pieces.add(piece)
            }
        }
        return pieces
    }

    private fun convertMatOfPoint(matOfPoint2f: MatOfPoint2f): List<MatOfPoint> {
        val listOfMatOfPoint = mutableListOf<MatOfPoint>()
        val points2fList = matOfPoint2f.toList()

        for (point2f in points2fList) {
            val matOfPoint = MatOfPoint(Point(point2f.x, point2f.y))
            listOfMatOfPoint.add(matOfPoint)
        }
        return listOfMatOfPoint
    }

    private fun rectangleContour(contours: List<MatOfPoint>): List<MatOfPoint> {
        val rectContours = mutableListOf<MatOfPoint>()

        for (contour in contours) {
            val area = Imgproc.contourArea(contour)
            if (area > 50) {
                val peri = Imgproc.arcLength(MatOfPoint2f(*contour.toArray()), true)
                val approx = MatOfPoint2f()
                Imgproc.approxPolyDP(MatOfPoint2f(*contour.toArray()), approx, 0.02 * peri, true)

                if (approx.toArray().size == 4) {
                    rectContours.add(contour)
                }
            }
        }

        rectContours.sortByDescending { Imgproc.contourArea(it) }
        return rectContours
    }

    private fun getCornerPoints(contour: MatOfPoint): MatOfPoint2f {
        val peri = Imgproc.arcLength(MatOfPoint2f(*contour.toArray()), true)
        val approx = MatOfPoint2f()
        Imgproc.approxPolyDP(MatOfPoint2f(*contour.toArray()), approx, 0.02 * peri, true)
        return approx
    }
}