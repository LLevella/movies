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
        const url = `${BACK}/player/`;
        return axios.post(url,player);
    }
    updateMoviePlayerInfo(player){
        const url = `${BACK}/player/`;
        return axios.patch(url,player);
    }
}