<template>
    <v-container class="fill-height">
        <v-row align="center" justify="center">
            <v-col cols="12" md="6" lg="6">
                <v-card>
                    <h1>Тесты</h1>
                    <v-list v-if="testsListAll.length === 0">
                        <v-list-item>
                            <v-list-item-content>Список тестов пуст</v-list-item-content>
                        </v-list-item>
                        </v-list>
                        <v-list v-else>
                        <v-list-item
                            v-for="test in testsListAll"
                            :key="test.id"
                        >
                            <v-card>
                                <v-list-item-title>Название: <b>{{ test.test_name }}</b></v-list-item-title>
                                <v-list-item-title>Количество вопросов: <b>{{ test.questions }}</b></v-list-item-title>
                                <v-list-item-title>Количество ответов: <b>{{ test.choices }}</b></v-list-item-title>
                                <v-list-item-title>Ответы: <b>{{ test.answers }}</b></v-list-item-title>
                            </v-card>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: "TestList",
        components: {
        },
        data() {
            return {
                message: "",
                errorMessages: [],
                testsListAll: []
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
            else {
                this.fetchTests()
            }
        },
        methods: {
            fetchTests() {
                this.$store.dispatch("test/fetchTests").then(() => {
                    this.testsListAll = this.$store.state.test.testsListAll
                })
                .catch(error => {
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
