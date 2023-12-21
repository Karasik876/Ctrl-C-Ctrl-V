package com.example.ally

import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.coroutines.*
import kotlinx.serialization.*
import kotlinx.serialization.json.*
import org.json.JSONException
import org.json.JSONObject

class RequestsManager {

    private val host: String = "192.168.0.106:8000"

    fun registerUser(user: UserCreate) : JSONObject {
        var resp = JSONObject("""{"e": "e"}""")
        runBlocking {
            val client = HttpClient(CIO) {
                install(ContentNegotiation) {
                    json(Json {
                        prettyPrint = true
                        isLenient = true
                    })
                }
            }
            val response: HttpResponse = client.post("http://$host/users/auth/signup") {
                contentType(ContentType.Application.Json)
                setBody(user)
            }
            var message = "OK"
            if (response.status != HttpStatusCode.Created) {
                message = try {
                    JSONObject(response.bodyAsText()).getString("password").replace('[', ' ').replace(']', ' ').replace('"', ' ').trim()
                } catch (e: JSONException) {
                    "Что-то пошло не так :("
                }
            }
            resp = JSONObject(
                """
                    {
                        "code": "${response.status}",
                        "message": "$message"
                    }
                """.trimIndent()
            )
            client.close()
        }
        return resp
    }

    fun authUser(user: UserAuth) : JSONObject {
        var resp = JSONObject("""{"e": "e"}""")
        runBlocking {
            val client = HttpClient(CIO) {
                install(ContentNegotiation) {
                    json(Json {
                        prettyPrint = true
                        isLenient = true
                    })
                }
            }
            val response: HttpResponse = client.post("http://$host/users/auth/signin") {
                contentType(ContentType.Application.Json)
                setBody(user)
            }
            println(response.bodyAsText())
            val message: JSONObject = if (response.status != HttpStatusCode.OK) {
                try {
                    JSONObject(response.bodyAsText())
                } catch (e: JSONException) {
                    JSONObject("""{"detail": "Что-то пошло не так :("}""")
                }
            } else {
                JSONObject(
                    """
                    {
                        "code": "${response.status}",
                        "detail": "OK",
                        "access": "${JSONObject(response.bodyAsText()).getString("access")}",
                        "refresh": "${JSONObject(response.bodyAsText()).getString("refresh")}"
                    }
                """.trimIndent()
                )
            }
            resp = message
            client.close()
        }
        return resp
    }

    fun verifyUser(user: UserVerify) : JSONObject {
        var resp = JSONObject("""{"e": "e"}""")
        runBlocking {
            val client = HttpClient(CIO) {
                install(ContentNegotiation) {
                    json(Json {
                        prettyPrint = true
                        isLenient = true
                    })
                }
            }
            val response: HttpResponse = client.post("http://$host/users/auth/verify") {
                contentType(ContentType.Application.Json)
                setBody(user)
            }
            val message = if (response.status == HttpStatusCode.OK) {
                JSONObject("""{"code": "${response.status}", "detail": "OK"}""")
            } else {
                JSONObject(response.bodyAsText())
            }
            resp = message
        }
        return resp
    }

    fun refreshUser(user: UserRefresh) : JSONObject {
        var resp = JSONObject("""{"e": "e"}""")
        runBlocking {
            val client = HttpClient(CIO) {
                install(ContentNegotiation) {
                    json(Json {
                        prettyPrint = true
                        isLenient = true
                    })
                }
            }
            val response: HttpResponse = client.post("http://$host/users/auth/verify") {
                contentType(ContentType.Application.Json)
                setBody(user)
            }
            val message = if (response.status == HttpStatusCode.OK) {
                JSONObject("""{"code": "${response.status}", "detail": "OK", "access": "${JSONObject(response.bodyAsText()).getString("access")}"}""")
            } else {
                JSONObject(response.bodyAsText())
            }
            resp = message
        }
        return resp
    }
}