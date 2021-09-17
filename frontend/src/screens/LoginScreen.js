import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Form, Button, Row, Col } from "react-bootstrap";
import Loader from "../components/Loader";
import FormContainer from "../components/FormContainer";
import Msg from "../components/Msg";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../actions/userActions";
import GoogleLogin from "react-google-login";
import FacebookLogin from "react-facebook-login";

import { googleLogin } from "../actions/userActions";
function LoginScreen({ location, history }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const dispatch = useDispatch();
  const redirect = location.search ? location.search.split("=")[1] : "/";
  const userLogin = useSelector((state) => state.userLogin);
  const { error, loading, userInfo } = userLogin;
  const userGLogin = useSelector((state) => state.userGLogin);
  const {
    error: errorG,
    success,
    loading: loadingG,
    userInfo: userInfoG,
  } = userGLogin;
  useEffect(() => {
    if (userInfo || userInfoG || success) {
      history.push(redirect);
    }
  }, [history, userInfo, userInfoG, success, redirect]);
  const submitHandler = (e) => {
    e.preventDefault();
    dispatch(login(email, password));
  };
  const googleResponse = (response) => {
    console.log(response);
    dispatch(googleLogin(response));
  };
  const responseFacebook = (response) => {
    console.log(response);
    //  dispatch(googleLogin(response));
  };
  return (
    <FormContainer>
      <h1> signin </h1>
      {error && <Msg variant="danger">{error}</Msg>}
      {loading && <Loader></Loader>}
      <Form onSubmit={submitHandler}>
        <Form.Group controlId="email">
          <Form.Label>E-mail address</Form.Label>
          <Form.Control
            type="email"
            placeholder="enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group controlId="password">
          <Form.Label>password</Form.Label>
          <Form.Control
            type="password"
            placeholder="enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Button type="submit" variant="primary">
          {" "}
          Sign in{" "}
        </Button>
      </Form>

      <div className="App">
        <h1>LOGIN WITH GOOGLE</h1>

        <GoogleLogin
          clientId="662075843272-0glea5naeogpktspv6nehh03ru0dm36b.apps.googleusercontent.com"
          buttonText="LOGIN WITH GOOGLE"
          onSuccess={googleResponse}
          onFailure={googleResponse}
        />
      </div>
      <div>
        <FacebookLogin
          appId="2415710988726197"
          autoLoad={true}
          fields="name,email,picture"
          scope="public_profile,user_friends"
          callback={responseFacebook}
          icon="fa-facebook"
        />
      </div>
      <Row className="py-3">
        <Col>
          {" "}
          new customer?{" "}
          <Link to={redirect ? `/register?redirect=${redirect}` : "/register"}>
            {" "}
            Register
          </Link>
        </Col>
      </Row>
    </FormContainer>
  );
}

export default LoginScreen;
