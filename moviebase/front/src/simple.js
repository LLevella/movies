import React, {Component, } from 'react';
import { Modal, Button, Col, Card} from 'react-bootstrap';
export default class ModalView extends Component {
  render() {
      return (
        <Modal
              show={this.props.show}
              size="lg"
              aria-labelledby="contained-modal-title-vcenter"
              centered
              onHide={() => this.props.update(!this.props.show)}
            >
            <Modal.Header closeButton>
              <Modal.Title id="contained-modal-title-vcenter">
                Внимание
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
            <h4>{this.props.msg.head}</h4>
              <p>
               {this.props.msg.body}
              </p>
            </Modal.Body>
            <Modal.Footer>
              <Button  onClick={() => this.props.update(!this.props.show)} >Close</Button>
            </Modal.Footer>
          </Modal>
      );
  }
}

class ShortCardView extends Component {
  render() {
    return (
      <Col sm>
       <Card  style={{ width: '18rem' }}>
          <Card.Img variant="top" src={this.props.movie.poster} />
          <Card.Body>
            <Card.Title>{this.props.movie.title}</Card.Title>
            <Card.Link href="#detail" onClick={() => this.props.getID(!this.props.id)} >Подробнее</Card.Link>
          </Card.Body>
        </Card>
      </Col>
      );
  }
};

export { ModalView, ShortCardView };