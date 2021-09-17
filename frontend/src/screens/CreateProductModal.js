import { Row, Col, Button, Modal, Container, Form } from "react-bootstrap";
import Msg from "../components/Msg";
import Loader from "../components/Loader";
import FormContainer from "../components/FormContainer";
import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { createProduct } from "../actions/productActions";
import { PRODUCT_CREATE_RESET } from "../constants/productConstant";
function CreateProductModal(props) {
  const dispatch = useDispatch();

  const productCreate = useSelector((state) => state.productCreate);
  const { loading, error, success, product } = productCreate;

  const productList = useSelector((state) => state.productList);
  const {
    loading: loadingProducts,
    error: errorProducts,
    products,
  } = productList;

  const [name, setName] = useState("");
  const [price, setPrice] = useState(0);
  const [image, setImage] = useState("");
  const [countInStock, setCountInStock] = useState(0);
  const [description, setDescription] = useState("");
  const [brand, setBrand] = useState("");
  const [category, setCategory] = useState("");
  const [uploading, setUploading] = useState(false);

  const createProductHandler = () => {
    dispatch(
      createProduct({
        name,
        price,
        image,
        countInStock,
        category,
        description,
        brand,
      })
    );
  };
  useEffect(() => {
    if (success) {
      props.onHide();
      products.push(product);
      setName("");
      setPrice(0);
      setImage("");
      setCountInStock(0);
      setDescription("");
      setBrand("");
      setCategory("");
      dispatch({ type: PRODUCT_CREATE_RESET });
    }
  }, [props, products, product]);

  const uploadHandler = (e) => {
    const file = e.target.files[0];

    setUploading(true);
    try {
      setImage(file);
      setUploading(false);
    } catch (error) {
      setUploading(false);
    }
  };

  return (
    <Modal {...props} aria-labelledby="contained-modal-title-vcenter">
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          Create Product{" "}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body className="show-grid">
        {loading ? (
          <Loader />
        ) : error ? (
          <Msg variant="danger">{error}</Msg>
        ) : (
          <Form onSubmit={createProductHandler}>
            <Form.Group controlId="name">
              <Form.Label>Name</Form.Label>
              <Form.Control
                type="name"
                placeholder="enter name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              ></Form.Control>
            </Form.Group>

            <Form.Group controlId="price">
              <Form.Label>Price</Form.Label>
              <Form.Control
                type="number"
                placeholder="enter price"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
              ></Form.Control>
            </Form.Group>

            <Form.Group controlId="image">
              <Form.Label>Image</Form.Label>
              <Form.Control
                type="text"
                placeholder="enter image"
                value={image}
                onChange={(e) => setImage(e.target.value)}
              ></Form.Control>

              <Form.File
                id="image-file"
                label="choose file"
                custom
                onChange={uploadHandler}
              ></Form.File>
              {uploading && <Loader />}
            </Form.Group>

            <Form.Group controlId="brand">
              <Form.Label>Brand</Form.Label>
              <Form.Control
                type="text"
                placeholder="enter brand"
                value={brand}
                onChange={(e) => setBrand(e.target.value)}
              ></Form.Control>
            </Form.Group>

            <Form.Group controlId="countinstock">
              <Form.Label>count in stock</Form.Label>
              <Form.Control
                type="number"
                placeholder="enter count in stuck"
                value={countInStock}
                onChange={(e) => setCountInStock(e.target.value)}
              ></Form.Control>
            </Form.Group>

            <Form.Group controlId="category">
              <Form.Label>Category</Form.Label>
              <Form.Control
                type="text"
                placeholder="enter brand"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              ></Form.Control>
            </Form.Group>

            <Form.Group controlId="description">
              <Form.Label>Description</Form.Label>
              <Form.Control
                type="text"
                placeholder="enter brand"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              ></Form.Control>
            </Form.Group>

            <Modal.Footer>
              <Button variant="primary" type="submit">
                {" "}
                Create{" "}
              </Button>
              <Button onClick={props.onHide}>Close</Button>
            </Modal.Footer>
          </Form>
        )}
      </Modal.Body>
    </Modal>
  );
}
export default CreateProductModal;
