package com.example.ally

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val userName: EditText = findViewById(R.id.user_name)
        val userSurname: EditText = findViewById(R.id.user_surname)
        val userEmail: EditText = findViewById(R.id.user_email)
        val userPassword: EditText = findViewById(R.id.user_password)
        val userRepassword: EditText = findViewById(R.id.user_repassword)
        val submitBtn: Button = findViewById(R.id.reg_submit_btn)
        val linkToAuth: TextView = findViewById(R.id.link_to_auth)
        val linkToCamera: TextView = findViewById(R.id.link_to_camera)

        linkToCamera.setOnClickListener {
            val intent = Intent(this, CameraActivity::class.java)
            startActivity(intent)
        }

        linkToAuth.setOnClickListener {
            val intent = Intent(this, AuthActivity::class.java)
            startActivity(intent)
        }

        submitBtn.setOnClickListener {
            val name = userName.text.toString().trim()
            val surname = userSurname.text.toString().trim()
            val email = userEmail.text.toString().trim()
            val password = userPassword.text.toString().trim()
            val repassword = userRepassword.text.toString().trim()

            if (name == "" || surname == "" || email == "" || password == "" || repassword == "") {
                Toast.makeText(this, "Нужно заполнить все поля!", Toast.LENGTH_LONG).show()
            } else {
                val user = UserCreate(name, surname, email, password, repassword)
                val request = RequestsManager()
                val response = request.registerUser(user)

                if (response.getString("message") == "OK"){
                    Toast.makeText(this, "Пользователь $name зарегистрирован!", Toast.LENGTH_LONG).show()
                    userName.text.clear()
                    userSurname.text.clear()
                    userEmail.text.clear()
                    userPassword.text.clear()
                    userRepassword.text.clear()
                    val intent = Intent(this, TestsActivity::class.java)
                    startActivity(intent)
                }
                else {
                    Toast.makeText(this, response.getString("message"), Toast.LENGTH_LONG).show()
                    userPassword.text.clear()
                    userRepassword.text.clear()
                }
            }
        }
    }
}