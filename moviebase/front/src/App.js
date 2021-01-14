// import logo from './logo.svg';
import './App.css';
import React, { Component } from 'react';
import { Container, Row, Navbar, Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import MovieRouter from './movieRouter'
import UserService from './userServices'

const userService = new UserService();
class App extends Component {
  constructor() {
    super();
    this.state = {
      isLoaded: false,
      error: null,
      username: "Гость",
      user_id: -1,
      movie: -1,
      is_loggedIn: false
    };
    this.updateState = this.updateState.bind(this);
  }
  updateState(app) {
    this.setState(app)
  }
    componentDidMount() { 
    userService.getUser("52086a7ecd654cb11851b42aefec814e75669cef")
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            is_loggedIn: true,
            username: result.data.username,
            user_id: result.data.id
          });
        },
        // Примечание: важно обрабатывать ошибки именно здесь, а не в блоке catch(),
        // чтобы не перехватывать исключения из ошибок в самих компонентах.
        (error) => {
          this.setState({
            isLoaded: true,
            error: error,
            is_loggedIn: false
          });
        }
      )
    }
  
  render() {
    const is_loggedIn = this.state.is_loggedIn;
    const username = this.state.username;
    return (
      <>
        <Navbar bg="dark" variant="dark">
          <Navbar.Brand href="#main">Фильмы</Navbar.Brand>
          <Nav className="mr-auto"> 
          {is_loggedIn ? (
              <Nav.Link href="#logout" onClick={() => this.updateState("logout")}>Выход</Nav.Link>
            ) : (
                <>
                  <Nav.Link href="#login" onClick={() => this.updateState("login")} >Вход</Nav.Link>
                  <Nav.Link href="#register" onClick={() => this.updateState("register")}>Регистрация</Nav.Link>
                </>
            )
          }
          </Nav>
          <Navbar.Text>
              Добро пожаловать, {username}
          </Navbar.Text>
        </Navbar>
        <Container>
          <Row className="justify-content-md-center" >
              <MovieRouter></MovieRouter>
          </Row>
        </Container>
      </>
    );
  }
}
export default App;
