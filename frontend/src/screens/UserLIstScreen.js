import React, { useEffect, useState } from "react";
import { LinkContainer } from "react-router-bootstrap";
import { Table, Button, Row, Col } from "react-bootstrap";
import Loader from "../components/Loader";
import FormContainer from "../components/FormContainer";
import Msg from "../components/Msg";
import { useDispatch, useSelector } from "react-redux";
import { listUsers, deleteUser } from "../actions/userActions";

function UserLIstScreen({ history }) {
  const dispatch = useDispatch();
  const usersList = useSelector((state) => state.usersList);
  const { loading, error, users } = usersList;

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const userDelete = useSelector((state) => state.userDelete);
  const { loading: loadingDelete, success: successDelete } = userDelete;

  useEffect(() => {
    if (userInfo && userInfo.isAdmin) {
      dispatch(listUsers());
    } else {
      history.push("/login");
    }
  }, [dispatch, history, successDelete, userInfo]);

  const deleteHandler = (id) => {
    if (window.confirm("are you sure you want to delete this user")) {
      dispatch(deleteUser(id));
    }
  };

  return (
    <div>
      {loading ? (
        <Loader />
      ) : error ? (
        <Msg variant="danger">{error}</Msg>
      ) : (
        <Table striped hover bordered responsive className="table-sm">
          <thead>
            <tr>
              <th> id</th>
              <th> Name</th>
              <th> email</th>
              <th> admin</th>
              <th> </th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>
                  {user.isAdmin ? (
                    <i className="fas fa-check" style={{ color: "green" }}></i>
                  ) : (
                    <i className="fas fa-check" style={{ color: "red" }}></i>
                  )}
                </td>
                <td>
                  <LinkContainer to={`/admin/user/${user.id}/edit`}>
                    <Button variant="light">
                      {" "}
                      Edit{"  "}
                      <i className="fas fa-edit" style={{ color: "black" }}></i>
                    </Button>
                  </LinkContainer>
                  <Button
                    variant="light"
                    onClick={() => deleteHandler(user.id)}
                  >
                    <i className="fas fa-trash" style={{ color: "red" }}></i>
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}{" "}
    </div>
  );
}

export default UserLIstScreen;
