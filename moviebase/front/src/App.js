// import logo from './logo.svg';
import './App.css';
import React, { Component } from 'react';
import axios from 'axios';
import { Container, Row, Col, Navbar, Nav, Card, } from "react-bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';

class App extends Component {
  constructor() {
    super();
    this.state = {
      films: []
    };
  } 

  componentDidMount() {

    axios.get('back/detail/1/')
      .then(function (response) {
        console.log(response);
        const films = response.data;
        this.setState({ films });
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  render() {
    return (
      <>
        <Navbar bg="dark" variant="dark">
          <Navbar.Brand href="#main">Фильмы</Navbar.Brand>
          <Nav className="mr-auto">
            <Nav.Link href="#login">Вход</Nav.Link>
            <Nav.Link href="#logout">Выход</Nav.Link>
            <Nav.Link href="#register">Регистрация</Nav.Link>  
          </Nav>
        </Navbar>
        <Container fluid="md">
          <Row>
            <Col>
              <Card style={{ width: '18rem' }}>
                <Card.Img variant="top" src="/media/images/300x450.webp" />
                <Card.Body>
                  <Card.Title>Фантастиеские Твари</Card.Title>
                  <Card.Link href="#detail">Подробнее</Card.Link>
                </Card.Body>
              </Card>
              </Col>
          </Row>
        </Container>
      </>
    );
  }
}
export default App;
