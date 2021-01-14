import React, { Component} from 'react';
import MovieList from './movieList'

export default class MovieRouter extends Component {
  render() {
    let current = this.props.currentState.app;
    if (current === "list") {
      return (
        <MovieList/>
      );
    }
  }
}