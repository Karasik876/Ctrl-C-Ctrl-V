<template>
    <v-container class="fill-height">
        <v-row align="center" justify="center">
            <v-col align="center" justify="center" cols="12" md="6" lg="6">
                <h1>Регистрация</h1>
                <v-alert
                    v-if="errorMessages.length > 0"
                    v-for="(error, index) in errorMessages"
                    :key="index"
                    type="error"
                    dismissible
                >
                    {{ error }}
                </v-alert>
                <form class="" @submit.prevent="handleRegister">
                    <div class="form-group">
                        <v-text-field
                            label=""
                            v-model="firstName"
                            hide-details="auto"
                            placeholder="Имя"
                        ></v-text-field>
                    </div>
                    <div class="form-group">
                        <v-text-field
                            label=""
                            v-model="lastName"
                            hide-details="auto"
                            placeholder="Фамилия"
                        ></v-text-field>
                    </div>
                    <div class="form-group">
                        <v-text-field
                            label=""
                            v-model="email"
                            hide-details="auto"
                            placeholder="Email"
                        ></v-text-field>
                    </div>
                    <div class="form-group">
                        <v-text-field
                            label=""
                            type="password"
                            v-model="password"
                            hide-details="auto"
                            placeholder="Пароль"
                        ></v-text-field>
                    </div>
                    <div class="form-group">
                        <v-text-field
                            label=""
                            type="password"
                            v-model="confirmPassword"
                            hide-details="auto"
                            placeholder="Подтвердите пароль"
                        ></v-text-field>
                    </div>

                    <v-btn class="my-2" color="primary" type="submit">Создать аккаунт</v-btn>
                </form>

                <v-row>
                    <v-col cols="12">
                        <p>Уже есть аккаунт?</p>
                        <router-link
                        to="/login"
                        class="login-button"
                        >Войти в существующий аккаунт</router-link>
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: "Register",
        components: {
        },
        data() {
            return {
                loading: false,
                message: "",
                firstName: "",
                lastName: "",
                email: "",
                password: "",
                confirmPassword: "",
                errorMessages: []
            };
        },
        computed: {
            loggedIn() {
                return this.$store.state.auth.status.loggedIn;
            },
        },
        created() {
            if (this.loggedIn) {
                this.$router.push("/");
            }
        },
        methods: {
            handleRegister() {
                this.loading = true;

                let user = {
                    firstName: this.firstName,
                    lastName: this.lastName,
                    email: this.email,
                    password: this.password,
                    confirmPassword: this.confirmPassword
                }

                this.$store.dispatch("auth/register", user).then(() => {
                    this.$router.push("/login");
                })
                .catch(error => {
                    debugger
                    this.loading = false;
                    if (error.response && error.response.data && error.response.data.message) {
                    debugger
                    this.errorMessages.push(error.response.data);
                    } else {
                    this.errorMessages.push(Object.values(error.response.data).flat().join());
                    }
                });
            },
        },
    };
</script>
