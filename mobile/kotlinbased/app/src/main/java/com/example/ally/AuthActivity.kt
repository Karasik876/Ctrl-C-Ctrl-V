package com.example.ally

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast

class AuthActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_auth)

        val linkToReg: TextView = findViewById(R.id.link_to_reg)
        val userEmail: EditText = findViewById(R.id.user_email_login)
        val userPassword: EditText = findViewById(R.id.user_password_login)
        val submitBtn: Button = findViewById(R.id.auth_submit_btn)

        linkToReg.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
        }

        submitBtn.setOnClickListener {
            val email = userEmail.text.toString().trim()
            val password = userPassword.text.toString().trim()

            if (email == "" || password == "") {
                Toast.makeText(this, "Нужно заполнить все поля!", Toast.LENGTH_LONG).show()
            } else {
                val user = UserAuth(email, password)
                val request = RequestsManager()
                val response = request.authUser(user)

                if (response.getString("detail") == "OK") {
                    val db = LocalDatabaseManager(this, null)
                    db.loginUser(response.getString("access"), response.getString("refresh"))
                    Toast.makeText(this, "Успешный вход!", Toast.LENGTH_LONG).show()

                    val intent = Intent(this, TestsActivity::class.java)
                    startActivity(intent)
                } else {
                    Toast.makeText(this, response.getString("detail"), Toast.LENGTH_LONG).show()
                    userPassword.text.clear()
                }
            }
        }
    }
}