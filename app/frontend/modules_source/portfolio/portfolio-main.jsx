import ReactDOM from "react-dom/client";

import { PortfolioContainer } from "./portfolio";
import store from "../general/store.ts";
import { Provider } from "react-redux";
import { setRatesToEUR } from "./slice/assetsSlice";

const domContainer = document.querySelector("#content");
const root = ReactDOM.createRoot(domContainer);
const usdRate = window.__USD_RATE__;
const gbpRate = window.__GBP_RATE__;
store.dispatch(setRatesToEUR({ USD: usdRate, GBP: gbpRate }));

root.render(
  <Provider store={store}>
    <PortfolioContainer/>
  </Provider>
);
