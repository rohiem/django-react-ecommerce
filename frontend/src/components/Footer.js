import React from "react";
import { Container, Row, Col } from "react-bootstrap";

function Footer() {
  return (
    <div>
      <Container>
        <Row>
          <Col className="text-center py3">
            <footer>Footer &copy;</footer>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Footer;
