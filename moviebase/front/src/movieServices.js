import axios from 'axios';


export default class MovieService{
    constructor() {
        this.BACK = 'back/';
    }
    getMovies() {
        const url = this.BACK;
        return axios.get(url);
    }
    getDetailedMovies(movie, token){
        const url = `${this.BACK}/detail/${movie}/`;
        return axios.get(url, {
                headers:
                    { "Authorization": `Token ${token}` }
            }
        );
    }
    getMoviePlayerInfo(movie, user, token) {
         const url = `${this.BACK}/player/${movie}/${user}/`;
        return axios.get(url,  {
                headers:
                    { "Authorization": `Token ${token}` }
            });
    }
    createMoviePlayerInfo(player, token){
        const url = `${this.BACK}/player/`;
        return axios.post(url, player,  {
                headers:
                    { "Authorization": `Token ${token}` }
            });
    }
    updateMoviePlayerInfo(player, token){
        const url = `${this.BACK}/player/`;
        return axios.patch(url, player,  {
                headers:
                    { "Authorization": `Token ${token}` }
            });
    }
};