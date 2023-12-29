import axios from 'axios';

const API_URL = 'http://localhost:8000/users/auth/';
const API_URL_USER = 'http://localhost:8000/api/';

class AuthService {
  login(user) {
    return axios
      .post(API_URL + 'signin', {
        email: user.username,
        password: user.password
      })
      .then(async response => {
        if (response.status === 200) {
          const authToken = response.data.access;
          const refreshToken = response.data.refresh;
          localStorage.setItem('user', JSON.stringify(authToken));
          localStorage.setItem('user_refresh', JSON.stringify(refreshToken));

          return response.data.access;
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

  logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('user_refresh');
    // localStorage.removeItem('id');
    // localStorage.removeItem('username');
  }

  register(user) {
    return axios.post(API_URL + 'signup', {
      first_name: user.firstName,
      last_name: user.lastName,
      email: user.email,
      password: user.password,
      re_password: user.confirmPassword
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

  fetchUserId() {
    return axios
      .get(`${API_URL_USER}user/me`, {
        headers: {
          Authorization: `Token ${JSON.parse(localStorage.getItem('user'))}`
        }
      })
      .then(async response => {
        if (response.status === 200) {
          localStorage.setItem("id", response.data.id)
          localStorage.setItem("username", response.data.username)
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

export default new AuthService();
