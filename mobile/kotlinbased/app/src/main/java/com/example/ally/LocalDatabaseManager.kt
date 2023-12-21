package com.example.ally

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper

class LocalDatabaseManager(val context: Context, val factory: SQLiteDatabase.CursorFactory?) :
    SQLiteOpenHelper(context, "localBase", factory, 1) {

    override fun onCreate(db: SQLiteDatabase?) {
        val query = "CREATE TABLE tokens (id INT PRIMARY KEY, access TEXT, refresh TEXT)"
        db!!.execSQL(query)
    }

    override fun onUpgrade(db: SQLiteDatabase?, oldVersion: Int, newVersion: Int) {
        db!!.execSQL("DROP TABLE IF EXISTS tokens")
        onCreate(db)
    }

    fun loginUser(access: String, refresh: String) {
        val values = ContentValues()
        values.put("access", access)
        values.put("refresh", refresh)

        val db = this.writableDatabase
        db.insert("tokens", null, values)
        db.close()
    }
}