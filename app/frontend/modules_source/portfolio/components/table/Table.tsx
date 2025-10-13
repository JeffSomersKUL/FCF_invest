import React from "react";
import { useSelector } from "react-redux";
import { RootState } from "../../../general/store";

function Table() {
  const {assets} = useSelector((state: RootState) => state.assets);

  return (
    <div>
      <div className="title-positions">
        <h2>Positions</h2>
        <div className="amount-positions">{assets.length}</div>
      </div>
      <table className="assets-table">
        <thead>
          <tr>
            <th className="units"></th>
            <th className="ticker">Ticker</th>
            <th className="last-price">Last Price</th>
            <th className="change">Today's Change</th>
            <th className="change"> Weekly Change</th>
            <th className="total-return">Total Return</th>
          </tr>
        </thead>
        <tbody>
          {assets.map((asset, index) => (
            <Asset assetInfo={asset} key={index} />
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Table;
