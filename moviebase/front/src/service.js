import axios from 'axios';
const BACK = 'back/'
export default class MovieService{

    constructor(){}
    getMovies() {
        const url = BACK;
        return axios.get(url).then(response => response.data);
    }
    getDetailedMovies(movie){
        const url = `${BACK}/detail/${movie}/`;
        return axios.get(url).then(response => response.data);
    }
    getMoviePlayerInfo(movie, user) {
         const url = `${BACK}/player/${movie}/${user}/`;
        return axios.get(url).then(response => response.data);
    }
    createMoviePlayerInfo(player){
        const url = `${API_URL}/api/customers/`;
        return axios.post(url,player);
    }
    updateCustomer(customer){
        const url = `${API_URL}/api/customers/${customer.pk}`;
        return axios.put(url,customer);
    }
}