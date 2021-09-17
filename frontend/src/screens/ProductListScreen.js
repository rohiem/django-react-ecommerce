import React, { useEffect, useState } from "react";
import { LinkContainer } from "react-router-bootstrap";
import { Table, Button, Row, Col } from "react-bootstrap";
import Loader from "../components/Loader";
import FormContainer from "../components/FormContainer";
import Msg from "../components/Msg";
import Paginate from "../components/Paginate";
import { useDispatch, useSelector } from "react-redux";
import {
  listProducts,
  deleteProduct,
  createProduct,
} from "../actions/productActions";
import { PRODUCT_CREATE_RESET } from "../constants/productConstant";
import CreateProductModal from "../screens/CreateProductModal";
function ProductListScreen({ history, match }) {
  const dispatch = useDispatch();
  const productList = useSelector((state) => state.productList);
  const { loading, error, products, page, pages } = productList;

  const productDelete = useSelector((state) => state.productDelete);
  const {
    loading: loadingDelete,
    error: errorDelete,
    success: successDelete,
  } = productDelete;

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const productCreate = useSelector((state) => state.productCreate);
  const {
    loading: loadingCreate,
    error: errorCreate,
    success: successCreate,
    product: productCreated,
  } = productCreate;

  const [modalShow, setModalShow] = useState(false);

  let keyword = history.location.search;
  useEffect(() => {
    dispatch({ type: PRODUCT_CREATE_RESET });
    dispatch(listProducts(keyword));

    if (!userInfo.isAdmin) {
      history.push("/login");
    }
    if (successDelete) {
      dispatch(listProducts());
    }
  }, [dispatch, history, userInfo, successCreate, successDelete, keyword]);

  const deleteHandler = (id) => {
    if (window.confirm("are you sure you want to delete this product")) {
      dispatch(deleteProduct(id));
    }
  };

  return (
    <div>
      <Row className="align-items-center">
        <Col>
          {" "}
          <h1> products</h1>
        </Col>
        <Col className="text-right">
          {" "}
          <Button className="my-3" onClick={() => setModalShow(true)}>
            <i className="fas fa-plus"></i> create product
          </Button>
          <CreateProductModal
            show={modalShow}
            onHide={() => setModalShow(false)}
          />
        </Col>
      </Row>
      {loadingDelete && <Loader />}
      {errorDelete && <Msg variant="danger">{errorDelete}</Msg>}
      {loadingCreate && <Loader />}
      {errorCreate && <Msg variant="danger">{errorCreate}</Msg>}
      {loading ? (
        <Loader />
      ) : error ? (
        <Msg variant="danger">{error}</Msg>
      ) : (
        <div>
          <Table striped hover bordered responsive className="table-sm">
            <thead>
              <tr>
                <th> id</th>
                <th> Name</th>
                <th> price</th>
                <th> category</th>
                <th> brand</th>
                <th> </th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product._id}>
                  <td>{product._id}</td>
                  <td>
                    <LinkContainer to={`/product/${product._id}`}>
                      <h4>{product.name}</h4>
                    </LinkContainer>
                  </td>
                  <td>{product.price}</td>
                  <td>{product.category}</td>
                  <td>{product.brand}</td>
                  <td>
                    <LinkContainer to={`/admin/products/${product._id}/edit`}>
                      <Button variant="light">
                        {" "}
                        Edit product{"  "}
                        <i
                          className="fas fa-edit"
                          style={{ color: "black" }}
                        ></i>
                      </Button>
                    </LinkContainer>
                    <Button
                      variant="light"
                      onClick={() => deleteHandler(product._id)}
                    >
                      <i className="fas fa-trash" style={{ color: "red" }}></i>
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
          <Paginate page={page} pages={pages} isAdmin={userInfo.isAdmin} />
        </div>
      )}{" "}
    </div>
  );
}

export default ProductListScreen;
