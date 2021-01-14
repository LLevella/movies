import React, { Component} from 'react';
import { ModalView, ShortCardView } from './simple'
import { Spinner} from 'react-bootstrap';
import MovieService from './movieServices';

const movieService = new MovieService();
export default class MovieList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      modalShow: true,
      data: [],
      status: 0,
      statusText: "",
    };
    console.log(props.currentState)
      this.updateState = this.updateState.bind(this);
      this.updateId = this.updateId.bind(this);
  }

  updateState(show) {
    this.setState({modalShow: show})
  }

  updateId(id) {
    this.props.updateState({ movie: id });
  }
  componentDidMount() { 
    movieService.getMovies()
      .then(
        (result) => {
          console.log(result);
          this.setState({
            isLoaded: true,
            data: result.data,
            status:  +result.status,
            statusText:  result.statusText
          });
        },
        // Примечание: важно обрабатывать ошибки именно здесь, а не в блоке catch(),
        // чтобы не перехватывать исключения из ошибок в самих компонентах.
        (error) => {
          this.setState({
            isLoaded: true,
            error: error
          });
        }
      )
  }
  render() {
   
    if (this.state.error) {
      let message = { head: "Ошибка", body: this.state.error.message };
      return (
        <ModalView
          show={this.state.modalShow}
          update={this.updateState}
          msg={message}
        />
      );
    }
    else if (!this.state.isLoaded) {
      return (
        <Spinner animation="border" role="status">
          <span className="sr-only">Loading...</span>
        </Spinner>
      );
    }
    else if (this.state.status !== 200) {
      let message = { head: "Предупреждение", body: this.state.statusText };
      return (
        <ModalView
          show = {this.state.modalShow}
          update = {this.updateState}
          msg = {message}
        />
      );
    }
    else { 
      const data = this.state.data;
      return (
      <>
        {data.map((movie) =>
         <ShortCardView
          movie={movie}
          getID = {this.updateId}
        />
          )}
      </>
      );
      }
  }
}