<template>
    <v-container class="fill-height">
        <v-row align="center" justify="center">
            <v-col align="center" justify="center" cols="12" md="6" lg="6">
                <v-alert
                    v-if="errorMessages.length > 0"
                    v-for="(error, index) in errorMessages"
                    :key="index"
                    type="error"
                    dismissible
                >{{ error }}
                </v-alert>
                <h1>Создать новый тест</h1>
                <form @submit.prevent="handleCreateTest">
                    <div class="form-group">
                        <v-text-field
                            v-model="testName"
                            hide-details="auto"
                            placeholder="Название теста"
                        ></v-text-field>
                    </div>
                    <div class="form-group">
                        <v-select
                            v-model="selectedTestQuestions"
                            :items="testQuestions"
                            label="Количество вопросов"
                            item-value="id"
                            outlined
                            required
                        ></v-select>
                    </div>
                    <div class="form-group">
                        <v-select
                            v-model="selectedTestAnswers"
                            :items="testAnswers"
                            label="Количество ответов"
                            item-value="id"
                            outlined
                            required
                        ></v-select>
                    </div>
                    <div class="form-group">
                        <v-text-field
                            v-model="answers"
                            hide-details="auto"
                            placeholder="Ответы"
                        ></v-text-field>
                    </div>
                    <v-btn class="my-2" color="primary" type="submit">Создать тест</v-btn>
                    <v-col cols="12">
                        <router-link to="/tests" class="login-button">Вернуться к тестам</router-link>
                    </v-col>
                </form>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: "CreateTest",
        components: {
        },
        data() {
            return {
                message: "",
                errorMessages: [],
                selectedTestQuestions: "",
                selectedTestAnswers: "",
                testAnswers: [
                    {
                        id: 1,
                        title: '1 ответ'
                    },
                    {
                        id: 2,
                        title: '2 ответа'
                    },
                    {
                        id: 3,
                        title: '3 ответа'
                    },
                ],
                testQuestions: [
                    {
                        id: 10,
                        title: '10 вопросов'
                    },
                    {
                        id: 20,
                        title: '20 вопросов'
                    },
                ],
                answers: ""
            };
        },
        computed: {
            loggedIn() {
                return this.$store.state.auth.status.loggedIn;
            },
        },
        created() {
            if (!this.loggedIn) {
                this.$router.push("/login");
            }
        },
        methods: {
            handleCreateTest() {
                let test = {
                    testName: this.testName,
                    selectedTestQuestions: this.selectedTestQuestions,
                    selectedTestAnswers: this.selectedTestAnswers,
                    answers: this.answers
                }

                this.$store.dispatch("test/addTest", test).then(() => {
                    this.$router.push("/tests/my");
                })
                .catch(error => {
                    const errorMessages = [];
                    if (error.response && error.response.data && error.response.data.message) {
                        debugger
                        this.errorMessages.push(error.response.data);
                    } else {
                        for (const field in error.response.data) {
                            if (error.response.data.hasOwnProperty(field)) {
                                const fieldErrors = error.response.data[field].map(errorText => `${field}: ${errorText}`);
                                errorMessages.push(...fieldErrors);
                            }
                        }

                        this.errorMessages = errorMessages;
                    }
                });
            },
        },
    };
</script>
