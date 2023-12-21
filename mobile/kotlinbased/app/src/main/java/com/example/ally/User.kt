package com.example.ally

import kotlinx.serialization.Serializable

@Serializable
data class UserCreate(
    val first_name: String,
    val last_name: String,
    val email: String,
    val password: String,
    val re_password: String
)

@Serializable
data class UserAuth(
    val email: String,
    val password: String,
)

@Serializable
data class UserVerify(
    val access: String,
)

@Serializable
data class UserRefresh(
    val refresh: String,
)