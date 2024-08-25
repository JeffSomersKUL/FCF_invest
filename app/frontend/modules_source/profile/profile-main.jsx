import ReactDOM from "react-dom/client"

import { ProfileContainer } from "./profile"

const domContainer = document.querySelector('#profile');
const root = ReactDOM.createRoot(domContainer);
root.render(<ProfileContainer/>);