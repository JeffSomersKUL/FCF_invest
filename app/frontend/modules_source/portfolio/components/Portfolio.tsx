import React from "react";
import Table from "./table/table";

export function PortfolioContainer({ balance }) {
  const balanceCash = balance.balances;
  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-xl-8 col-lg-12 col-12 p-2">
          <Table />
        </div>
        <div
          className="col-xl-4 col-lg-12 col-12 p-2"
          style={{ height: "fit-content" }}>
          <Summary balanceCash={balanceCash} />
        </div>
      </div>
    </div>
  );
}
