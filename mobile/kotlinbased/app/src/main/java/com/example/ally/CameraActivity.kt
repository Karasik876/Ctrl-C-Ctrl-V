package com.example.ally

import android.graphics.Bitmap
import android.graphics.Matrix
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.camera.core.ImageProxy
import com.example.ally.databinding.ActivityCameraBinding
import com.ingenieriiajhr.jhrCameraX.BitmapResponse
import com.ingenieriiajhr.jhrCameraX.CameraJhr
import com.ingenieriiajhr.jhrCameraX.ImageProxyResponse
import org.opencv.android.OpenCVLoader


class CameraActivity : AppCompatActivity() {

    lateinit var binding : ActivityCameraBinding
    lateinit var cameraJhr: CameraJhr

    val omrUtils = OMRUtils()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCameraBinding.inflate(layoutInflater)
        setContentView(binding.root)

        if(OpenCVLoader.initDebug()) Log.d("OPENCV2023","TRUE")
        else Log.d("OPENCV2023","INCORRECTO")

        cameraJhr = CameraJhr(this)
    }

    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (cameraJhr.allpermissionsGranted() && !cameraJhr.ifStartCamera){
            startCameraJhr()
        }else{
            cameraJhr.noPermissions()
        }
    }

    private fun startCameraJhr() {
        cameraJhr.addlistenerBitmap(object :BitmapResponse{
            override fun bitmapReturn(bitmap: Bitmap?) {
                val newBitmap = omrUtils.proccessOmr(bitmap!!)
                if (bitmap!=null){
                    runOnUiThread {
                        binding.imgBitMap2.setImageBitmap(newBitmap)
                    }
                }
            }
        })

        cameraJhr.addlistenerImageProxy(object : ImageProxyResponse {
            override fun imageProxyReturn(imageProxy: ImageProxy) {
                try {
                    val bitmap = Bitmap.createBitmap(imageProxy.width,imageProxy.height,Bitmap.Config.ARGB_8888)
                    imageProxy.use { bitmap.copyPixelsFromBuffer(imageProxy.planes[0].buffer) }
                    runOnUiThread {
                        binding.imgBitMap.setImageBitmap(bitmap)
                    }
                }catch (e: IllegalStateException) {
                    // Handle the exception here
                    println("error en conversion imageproxy")
                }

            }
        })

        cameraJhr

        cameraJhr.initBitmap()
        cameraJhr.initImageProxy()
        //selector camera LENS_FACING_FRONT = 0;    LENS_FACING_BACK = 1;
        //aspect Ratio  RATIO_4_3 = 0; RATIO_16_9 = 1;  false returImageProxy, true return bitmap
        cameraJhr.start(1,0,binding.cameraPreview,false,false,true)
    }

    fun Bitmap.rotate(degrees:Float) = Bitmap.createBitmap(this,0,0,width,height,Matrix().apply { postRotate(degrees) },true)
}