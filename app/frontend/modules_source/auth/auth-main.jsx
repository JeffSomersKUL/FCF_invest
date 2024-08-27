import ReactDOM from "react-dom/client"

import { Form } from "./auth-form"

const domContainer = document.querySelector('#login-form');
const root = ReactDOM.createRoot(domContainer);
root.render(<Form/>);