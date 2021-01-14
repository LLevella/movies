import axios from 'axios';

const AUTH = 'auth/';

export default class UserService{
    getUser(token) {
        const url = `${AUTH}/users/me/`;
        return axios.get(url,  {
                headers:
                    { "Authorization": `Token ${token}` }
            });
    }
    newUser(user){
        const url = `${AUTH}/users/`;
        return axios.post(url, user);
    }
    login(user) {
        const url =  `${AUTH}/token/login`;
        return axios.post(url, user).then(response => response);
    }
    logout(user, token) {
        const url =  `${AUTH}/token/logout`;
        return axios.post(url,user,  {
                headers:
                    { "Authorization": `Token ${token}` }
            }).then(response => response);
    }
}