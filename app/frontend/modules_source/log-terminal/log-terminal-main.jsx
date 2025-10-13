import ReactDOM from "react-dom/client";

import { LogTerminal } from "./log-terminal";

const domContainer = document.querySelector("#log-content");
const root = ReactDOM.createRoot(domContainer);
root.render(
  <LogTerminal title={window.__TITLE__}/>
);
