import Footer from "./components/Footer";
import Headers from "./components/Headers";
import "./App.css";
import { Container } from "react-bootstrap";
import HomeScreen from "./screens/HomeScreen";
import ProductScreen from "./screens/ProductScreen";
import CartScreen from "./screens/CartScreen";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import LoginScreen from "./screens/LoginScreen";
import RegisterScreen from "./screens/RegisterScreen";
import ProfileScreen from "./screens/ProfileScreen";
import ShippingScreen from "./screens/ShippingScreen";
import PaymentScreen from "./screens/PaymentScreen";
import PlaceOrderScreen from "./screens/PlaceOrderScreen";
import OrderScreen from "./screens/OrderScreen";
import UserLIstScreen from "./screens/UserLIstScreen";
import UserEditScreen from "./screens/UserEditScreen";
import ProductListScreen from "./screens/ProductListScreen";
import ProductEditScreen from "./screens/ProductEditScreen";
import NotFound from "./screens/NotFound";
import OrderListScreen from "./screens/OrderListScreen";
function App() {
  return (
    <Router>
      <Headers />
      <main>
        <Container>
          <h1>welcome to react-ecommerce</h1>
          <Switch>
            <Route exact path="/" component={HomeScreen} />
            <Route path="/login" component={LoginScreen} />
            <Route path="/register" component={RegisterScreen} />
            <Route path="/profile" component={ProfileScreen} />
            <Route path="/shipping" component={ShippingScreen} />
            <Route path="/payment" component={PaymentScreen} />
            <Route path="/placeorder" component={PlaceOrderScreen} />
            <Route path="/order/:id" component={OrderScreen} />
            <Route path="/product/:id" component={ProductScreen} />
            <Route path="/cart/:id?" component={CartScreen} />
            <Route path="/admin/userlist" component={UserLIstScreen} />
            <Route path="/admin/user/:id/edit" component={UserEditScreen} />
            <Route exact path="/admin/products" component={ProductListScreen} />
            <Route exact path="/admin/orders" component={OrderListScreen} />
            <Route
              path="/admin/products/:id/edit"
              component={ProductEditScreen}
            />

            <Route path="*" component={NotFound} />
          </Switch>
        </Container>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
