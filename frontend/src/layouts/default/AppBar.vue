<template>
  <header class="main-header">
    <nav class="main-nav">
      <div class="left-section">
          <h1 class="project-name"><a href="/">Ally</a></h1>
          <router-link
            class="nav-link"
            to="/tests"
          >Шаблоны тестов</router-link>
          <a href="templates.html" class="nav-link"></a>
          <router-link
            class="nav-link"
            to="/create_test"
          >Создать тест</router-link>
      </div>
      <div class="right-section">
        <template v-if="!currentUser">
          <div class="auth-buttons">
            <router-link
              to="/login"
              class="login-button"
            >Войти</router-link>
            <router-link
              to="/register"
              class="create-account-button"
            >Создать аккаунт</router-link>
          </div>
        </template>
        <template v-else>
          <div class="auth-buttons">
            <a style="cursor: pointer;" class="login-button" @click="logOut">
              Выйти
            </a>
            <!-- <router-link
              to="/logout"
              class="login-button"
            >Выйти</router-link> -->
          </div>
        </template>
      </div>
    </nav>
  </header>
</template>

<script>
  export default {
    data() {
      return {
        appTitle: "Менеджер задач",
        username: ''
      }
    },
    computed: {
      currentUser() {
        // if (this.$store.state.auth.status.loggedIn)
          // this.fetchUserId()

        return this.$store.state.auth.user;
      },
    },
    methods: {
      logOut() {
        this.$store.dispatch('auth/logout');
        this.$router.push('/login');
      },
      handleAddTask() {
        this.$router.push('/add_task');
      },
      handleFetchUserTasks() {
        this.$router.push('/tasks');
      },
      handleFetchAllTasks() {
        this.$router.push('/tasks_all');
      },
      fetchUserId() {
        this.$store.dispatch("auth/fetchUserId").then(() => {
          this.username = localStorage.getItem("username");
        }).catch(error => {
          this.loading = false;
          if (error.response && error.response.data && error.response.data.message) {
            this.errorMessages.push(error.response.data);
          } else {
            const errors = Object.values(error.response.data).flat();

            errors.forEach(errorMessage => {
              this.errorMessages.push(errorMessage);
            });
          }
        });
      }
    }
  };
</script>
