<template>
  <div v-if="!loggedIn">
    <main class="main-content">
        <section class="create">
            <img class="steps-image" src="@/assets/img/steps.png" width="137" height="470">
            <div class="create-content">
                <div class="create-content-text">
                    <h2>Создавайте и оценивайте тесты в любом месте</h2>
                    <p>Проводите контрольные работы и оценивайте их вместе с Ally, в классе или онлайн. Сэкономьте время на оценивании
                        и получите чёткое представление об успеваемости ваших учеников.
                    </p>
                </div>
                <div class="main-content-auth-buttons">
                    <router-link
                      to="/login"
                      class="login-button"
                    >Вход</router-link>
                    <router-link
                      to="/register"
                      class="create-account-button"
                    >Создать аккаунт</router-link>
                </div>
            </div>
        </section>
    </main>
  </div>
</template>

<script>
  export default {
    name: "Main",
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
        // handleLogin() {
        //     this.loading = true;

        //     let user = {
        //         username: this.username, 
        //         password: this.password
        //     }

        //     this.$store.dispatch("auth/login", user).then(() => {
        //         this.$router.push("/");
        //     })
        //     .catch(error => {
        //         debugger
        //         this.loading = false;
        //         if (error.response && error.response.data && error.response.data.message) {
        //         debugger
        //         this.errorMessages.push(error.response.data);
        //         } else {
        //         this.errorMessages.push(Object.values(error.response.data).flat().join());
        //         }
        //     });
        // },
    },
  };
</script>
