<template>
    <v-container class="fill-height">
        <v-row align="center" justify="center">
            <v-col align="center" justify="center" cols="12" md="6" lg="6">
                <h1>Вход</h1>
                <v-alert
                    v-if="errorMessages.length > 0"
                    v-for="(error, index) in errorMessages"
                    :key="index"
                    type="error"
                    dismissible
                >
                    {{ error }}
                </v-alert>
                <form @submit.prevent="handleLogin">
                    <!-- <label for="email">Email:</label> -->
                    <v-text-field
                        label=""
                        v-model="username"
                        hide-details="auto"
                        placeholder="Email"
                    ></v-text-field>
                    <!-- <input type="text" id="username_or_email" name="" required> -->

                    <!-- <label for="password">Пароль:</label> -->
                    <v-text-field
                        class="mt-2"
                        label=""
                        v-model="password"
                        type="password"
                        hide-details="auto"
                        placeholder="Пароль"
                    ></v-text-field>
                    <!-- <input type="password" id="password" name="password" required> -->

                    <v-btn class="my-2" color="primary" type="submit">Войти</v-btn>
                </form>
                <v-row>
                    <v-col cols="12">
                        <router-link to="/register" class="login-button">Зарегистрировать новый аккаунт</router-link>
                    </v-col>
                    <v-col cols="12">
                        <!-- <router-link to="/recover_password" class="login-button">Восстановить пароль</router-link> -->
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: "Login",
        components: {
        },
        data() {
            return {
                loading: false,
                message: "",
                username: "",
                password: "",
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
            handleLogin() {
                this.loading = true;

                let user = {
                    username: this.username, 
                    password: this.password
                }

                this.$store.dispatch("auth/login", user).then(() => {
                    this.$router.push("/");
                })
                .catch(error => {
                    this.loading = false;
                    if (error.response && error.response.data && error.response.data.message) {
                        this.errorMessages.push(error.response.data);
                    } else {
                        this.errorMessages.push(Object.values(error.response.data).flat().join());
                    }
                });
            },
        },
    };
</script>
