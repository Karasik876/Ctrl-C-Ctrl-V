import axios from 'axios';

const API_URL = 'http://localhost:8000/';

class TestService {
    fetchTests(user) {
        return axios
            .get(`${API_URL}tests/`,{
                headers: {
                    Authorization: `Bearer ${JSON.parse(localStorage.getItem('user'))}`
                }
            })
            .then(async response => {
                if (response.status === 200) {
                    return response.data;
                } else if (response.status === 400) {
                    const errors = await response.data;
                    if (typeof errors === 'object') {
                        errorMessages.value = Object.values(errors).flat();
                    } else {
                        errorMessages.value = [errors];
                    }
                }
                else {
                }
            });
    }

    addTest(test) {
        return axios
            .post(API_URL + 'tests/create', {
                test_name: test.testName,
                questions: test.selectedTestQuestions,
                choices: test.selectedTestAnswers,
                answers: test.answers,
            }, {
                headers: {
                    Authorization: `Bearer ${JSON.parse(localStorage.getItem('user'))}`
                }
            })
            .then(async response => {
                if (response.status === 201) {
                    return response.data;
                } else if (response.status === 400) {
                    const errors = await response.data;
                    if (typeof errors === 'object') {
                        errorMessages.value = Object.values(errors).flat();
                    } else {
                        errorMessages.value = [errors];
                    }
                }
                else {
                }
            });
    }
}

export default new TestService();
