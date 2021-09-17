import { Alert } from "react-bootstrap";

function Msg({ variant, children }) {
  return <Alert variant={variant}>{children}</Alert>;
}

export default Msg;
