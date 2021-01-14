import axios from 'axios';
const BACK = 'back/'
export default class MovieService{

    constructor(){}
    getMovies() {
        const url = BACK;
        return axios.get(url).then(response => response.data);
    }
    getDetailedMovies(id){
        const url = `${BACK}/detail`;
        return axios.get(url).then(response => response.data);
    }
    getCustomer(pk) {
        const url = `${API_URL}/api/customers/${pk}`;
        return axios.get(url).then(response => response.data);
    }
    deleteCustomer(customer){
        const url = `${API_URL}/api/customers/${customer.pk}`;
        return axios.delete(url);
    }
    createCustomer(customer){
        const url = `${API_URL}/api/customers/`;
        return axios.post(url,customer);
    }
    updateCustomer(customer){
        const url = `${API_URL}/api/customers/${customer.pk}`;
        return axios.put(url,customer);
    }
}