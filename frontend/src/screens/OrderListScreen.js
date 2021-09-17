import React, { useEffect, useState } from "react";
import { LinkContainer } from "react-router-bootstrap";
import { Table, Button, Row, Col } from "react-bootstrap";
import Loader from "../components/Loader";
import FormContainer from "../components/FormContainer";
import Msg from "../components/Msg";
import { useDispatch, useSelector } from "react-redux";
import { listOrders, deliverOrder } from "../actions/orderActions";
import { ORDER_DELIVERED_RESET } from "../constants/OrderConstants";

function OrderListScreen({ history }) {
  const dispatch = useDispatch();
  const orderList = useSelector((state) => state.orderList);
  const { loading, error, orders } = orderList;

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  useEffect(() => {
    if (userInfo && userInfo.isAdmin) {
      dispatch(listOrders());
    } else {
      history.push("/login");
    }
  }, [dispatch, history, userInfo]);

  return (
    <div>
      <h1>Orders</h1>
      {loading ? (
        <Loader />
      ) : error ? (
        <Msg variant="danger">{error}</Msg>
      ) : (
        <Table striped hover bordered responsive className="table-sm">
          <thead>
            <tr>
              <th> id</th>
              <th> user</th>
              <th> date</th>
              <th> price</th>
              <th> paid</th>
              <th> delivered</th>
              <th> </th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order._id}>
                <td>{order._id}</td>
                <td>{order.user && order.user.name}</td>
                <td>{order.createdAt}</td>
                <td>{order.totalPrice}</td>

                <td>
                  {order.isPaid ? (
                    <i className="fas fa-check" style={{ color: "green" }}>
                      {order.paidAt}
                    </i>
                  ) : (
                    <i
                      className="far fa-times-circle"
                      style={{ color: "red" }}
                    ></i>
                  )}
                </td>

                <td>
                  {order.isDelivered ? (
                    <i className="fas fa-check" style={{ color: "green" }}>
                      {order.deliverdAt}
                    </i>
                  ) : (
                    <i
                      className="far fa-times-circle"
                      style={{ color: "red" }}
                    ></i>
                  )}
                </td>

                <td>
                  <LinkContainer to={`/order/${order._id}`}>
                    <Button variant="light">
                      {" "}
                      Detail{"  "}
                      <i className="fas fa-edit" style={{ color: "black" }}></i>
                    </Button>
                  </LinkContainer>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}{" "}
    </div>
  );
}

export default OrderListScreen;
