// import logo from './logo.svg';
import './App.css';
import React, { Component } from 'react';
import { Container, Row, Col, Navbar, Nav, Card, Button } from "react-bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';
// import { render } from "react-dom";
// import MovieListDisplay from './movieList.js';

class App extends Component {
  constructor() {
    super();
    this.state = {
      activePage: 0,
    };
  } 
  render() {
    return (
      <>
      <Navbar bg="dark" variant="dark">
        <Navbar.Brand href="#home">Фильмы</Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link href="#features">Вход</Nav.Link>
          <Nav.Link href="#pricing">Выход</Nav.Link>
          <Nav.Link href="#pricing">Регистрация</Nav.Link>  
        </Nav>
      </Navbar>
      <Container>
        <Row>
            <Col xs={6} md={4}>
              <Card style={{ width: '18rem' }}>
                <Card.Img variant="top" src="holder.js/280x420" />
                <Card.Body>
                  <Card.Title></Card.Title>
                  <Card.Text>
                  </Card.Text>
                  <Button variant="primary"></Button>
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
