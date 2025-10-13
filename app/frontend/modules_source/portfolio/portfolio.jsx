import { useState, Fragment, useEffect } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { useSelector, useDispatch } from "react-redux";
import ReactEcharts from "echarts-for-react";
import { CaretDownFill, CaretUpFill } from "react-bootstrap-icons";

import { fetchAssetPrice } from "./slice/assetsSlice";

ChartJS.register(ArcElement, Tooltip, Legend);

function getSymbol(currency) {
  if (currency == "EUR") {
    return "€";
  } else if (currency == "USD") {
    return "$";
  } else if ((currency = "GBp")) {
    return "£";
  }
  return "?";
}

function formatNumber(number) {
  return new Intl.NumberFormat("de-DE", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(number);
}

const renderChange = (begin, end) => {
  const change = begin - end;
  const isPositive = change > 0;
  return (
    <span style={{ display: "flex", alignItems: "center", gap: "5px" }}>
      {isPositive ? (
        <CaretUpFill style={{ color: "green" }} />
      ) : (
        <CaretDownFill style={{ color: "red" }} />
      )}
      <div style={{ fontSize: "12px" }}>
        {Math.abs(change).toFixed(2)}
        {` (${Math.abs((change / begin) * 100).toFixed(2)}%)`}
      </div>
    </span>
  );
};

function Percentage({ value }) {
  const formattedValue = (value * 100).toFixed(2) + "%";

  const color = value > 0 ? "green" : value < 0 ? "red" : "black";

  return <div style={{ color: color }}>{formattedValue}</div>;
}

function getAssetsTotals(assets) {
  let assetsEuro = 0;
  let assetsUSD = 0;
  let assetsGBP = 0;

  assets.forEach((asset) => {
    const totalValue = asset.net_quantity * asset.price;

    if (asset.currency === "EUR") {
      assetsEuro += totalValue;
    } else if (asset.currency === "USD") {
      assetsUSD += totalValue;
    } else if (asset.currency === "GBP") {
      assetsGBP += totalValue;
    }
  });
  return {
    assetsEuro,
    assetsUSD: assetsUSD * window.__USD_RATE__,
    assetsGBP: assetsGBP * window.__GBP_RATE__,
  };
}

function BalanceChart2({
  cashEuro,
  cashUSD,
  cashGBP,
  assetsEuro,
  assetsUSD,
  assetsGBP,
}) {
  const borderColor = "#82b2ffc2";
  const borderWidth = 2;

  const rawData = [
    {
      value: cashEuro,
      category: "cash",
      name: "Euros",
      symbol: "€ (cash)",
      color: "#2176FF",
      itemStyle: { borderColor: borderColor, borderWidth: borderWidth },
    },
    {
      value: cashUSD,
      category: "cash",
      name: "Dollars",
      symbol: "$ (cash)",
      color: "#478EFF",
      itemStyle: { borderColor: borderColor, borderWidth: borderWidth },
    },
    {
      value: cashGBP,
      category: "cash",
      name: "Ponds",
      symbol: "£ (cash)",
      color: "#70A7FF",
      itemStyle: { borderColor: borderColor, borderWidth: borderWidth },
    },
    {
      value: assetsEuro,
      category: "assets",
      symbol: "€ (assets)",
      name: "Assets EUR",
      color: "#31AF90",
    },
    {
      value: assetsUSD,
      category: "assets",
      symbol: "$ (assets)",
      name: "Assets USD",
      color: "#80DBC4",
    },
    {
      value: assetsGBP,
      category: "assets",
      symbol: "£ (assets)",
      name: "Assets GBP",
      color: "#A0E4D3",
    },
  ];

  const filteredSeriesData = rawData.filter((item) => item.value > 0);
  const totalValue = filteredSeriesData.reduce(
    (sum, item) => sum + item.value,
    0
  );
  const assetLegendData = filteredSeriesData
    .filter((item) => item.category === "assets")
    .map((item) => item.name);

  const cashLegendData = filteredSeriesData
    .filter((item) => item.category === "cash")
    .map((item) => item.name);

  const combinedLegendData = [...assetLegendData, ...cashLegendData];
  const colors = filteredSeriesData.map((item) => item.color);

  const option = {
    tooltip: {
      trigger: "item",
      formatter: function (params) {
        const formattedValue = formatNumber(params.value);
        return `${params.name}: ${formattedValue}€ (${params.percent}%)`;
      },
    },
    legend: [
      {
        orient: "vertical",
        left: "5%",
        bottom: "0%",
        data: assetLegendData,
        textStyle: {
          fontSize: 12,
          color: "rgba(39, 48, 75, 0.71)",
        },
        formatter: function (name) {
          const item = filteredSeriesData.find((data) => data.name === name);
          if (item) {
            const percentage =
              totalValue > 0 ? ((item.value / totalValue) * 100).toFixed(1) : 0;
            return `${name} (${percentage}%)`;
          }
          return name;
        },
      },
      {
        orient: "vertical",
        right: "5%",
        bottom: "0%",
        data: cashLegendData,
        textStyle: {
          fontSize: 12,
          color: "rgba(39, 48, 75, 0.71)",
        },
        formatter: function (name) {
          const item = filteredSeriesData.find((data) => data.name === name);
          if (item) {
            const percentage =
              totalValue > 0 ? ((item.value / totalValue) * 100).toFixed(1) : 0;
            return `${name} (${percentage}%)`;
          }
          return name;
        },
      },
    ],
    series: [
      {
        name: "Portfolio Breakdown",
        type: "pie",
        radius: ["45%", "65%"],
        center: ["50%", "40%"],
        itemStyle: {
          borderRadius: 0,
          borderColor: "#fdfdfdc2",
          borderWidth: 2,
        },
        label: {
          show: true,
          formatter: (params) => {
            const item = filteredSeriesData.find(
              (data) => data.name === params.name
            );
            return item ? `{symbol|${item.symbol}}` : "";
          },
          rich: {
            symbol: {
              fontSize: 11,
              color: "#124882",
            },
          },
          position: "outside",
          distanceToLabelLine: 10,
        },
        data: filteredSeriesData,
        color: colors,
      },
    ],
  };

  return <ReactEcharts option={option} />;
}

function Summary({ balanceCash }) {
  const cashEuro = balanceCash.EUR || 0;
  const cashUSD = (balanceCash.USD || 0) * window.__USD_RATE__;
  const cashGBP = (balanceCash.GBP || 0) * window.__GBP_RATE__;

  const assetsObject = useSelector((state) => state.assets.assets);
  const assets = Object.values(assetsObject);

  const { assetsEuro, assetsUSD, assetsGBP } = getAssetsTotals(assets);

  const totalCash =
    cashEuro + cashUSD + cashGBP + assetsEuro + assetsUSD + assetsGBP;

  return (
    <div className="summary-block">
      <div className="cash">€{formatNumber(totalCash)}</div>
      <div className="after-costs">
        <div>€2.000</div>
        <div style={{ fontSize: 10 }}>(after costs)</div>
      </div>
      <div className="cash-details-container">
        {balanceCash.EUR > 0 && (
          <div className="cash-details">
            <div className="cash-symbol">€</div>
            <div>{formatNumber(balanceCash.EUR)}</div>
          </div>
        )}
        {balanceCash.USD > 0 && (
          <div className="cash-details">
            <div className="cash-symbol">$</div>
            <div>{formatNumber(balanceCash.USD)}</div>
          </div>
        )}
        {balanceCash.GBP > 0 && (
          <div className="cash-details">
            <div className="cash-symbol">£</div>
            <div>{formatNumber(balanceCash.GBP)}</div>
          </div>
        )}
      </div>
      <div style={{ width: "100%", margin: "0 auto" }}>
        <BalanceChart2
          cashEuro={cashEuro}
          cashUSD={cashUSD}
          cashGBP={cashGBP}
          assetsEuro={assetsEuro}
          assetsUSD={assetsUSD}
          assetsGBP={assetsGBP}
        />
      </div>
    </div>
  );
}

function Chart() {}

function Asset({ assetInfo, index }) {
  const dispatch = useDispatch();
  const {
    asset,
    id,
    net_quantity: amount,
    price,
    currency,
    type,
    ticker,
    price_opening: opening,
    price_begin_week: beginWeek,
    live_trackable: trackable,
    total_spent: invested,
    sell_cost: cost
  } = assetInfo;
  console.log(cost)
  const [currentPrice, setCurrentPrice] = useState(price);
  const totalEquity = amount * currentPrice;
  const isSHort = amount < 0;

  const totalReturn = totalEquity - invested;
  const returnPercentage =
    invested !== 0 ? totalReturn / Math.abs(invested) : 0;

  useEffect(() => {
    const fetchPrice = () => {
      dispatch(fetchAssetPrice(id));
    };
    const interval = setInterval(fetchPrice, 120000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    setCurrentPrice(price);
  }, [price]);

  const [showTooltip, setShowTooltip] = useState(false);

  const handleMouseEnter = () => {
    setShowTooltip(true);
  };

  const handleMouseLeave = () => {
    setShowTooltip(false);
  };

  return (
    <tr key={id} style={{ backgroundColor: isSHort ? "#fffcfc" : "#fcfffc" }}>
      <td
        className="units"
        style={{
          color: isSHort ? "red" : "green",
          textShadow: isSHort
            ? "0 0 5px rgba(255, 0, 0, 0.3), 0 0 50px rgba(255, 0, 0, 0.1)"
            : "0 0 5px rgba(0, 255, 0, 0.3), 0 0 50px rgba(0, 255, 0, 0.1)",
        }}>
        {amount}
      </td>
      <td className="asset-name-container">
        <div
          className="ticker"
          style={{ display: "flex", gap: 5, alignItems: "center" }}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}>
          <div
            style={{
              fontWeight: "bold",
              overflow: "hidden",
              textOverflow: "ellipsis",
            }}>
            {ticker}
          </div>
          {(type == "Option" || type == "GovernmentBill") && (
            <Fragment>
              <div style={{ width: "fit-content" }}>-</div>
              <div style={{ fontSize: 12 }}>
                {type === "Option" && "opt"}
                {type === "GovernmentBill" && "bill"}
              </div>
            </Fragment>
          )}
        </div>
        {showTooltip && (
          <div className="tooltip">
            {asset} - {type}
          </div>
        )}
      </td>
      <td
        className="number-format"
        style={{
          color: !trackable && "lightgray",
          fontStyle: !trackable && "italic",
          fontWeight: trackable && "bold",
        }}>
        {getSymbol(currency)}
        {formatNumber(currentPrice)}
      </td>
      <td className="change number-format" style={{ color: "#8c8c8c" }}>
        {opening ? renderChange(price, opening) : "-"}
      </td>
      <td className="change number-format" style={{ color: "#8c8c8c" }}>
        {beginWeek ? renderChange(price, beginWeek) : "-"}
      </td>
      <td className="number-format return">
        <div>{formatNumber(totalReturn)}</div>
        <div className="percentage">
          <Percentage value={returnPercentage} />
        </div>
      </td>
    </tr>
  );
}

function Holdings() {
  const assetsObject = useSelector((state) => state.assets.assets);
  const assets = Object.values(assetsObject);

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

export function PortfolioContainer({ balance }) {
  const balanceCash = balance.balances;
  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-xl-8 col-lg-12 col-12 p-2">
          <div></div>
          <div>
            <Holdings />
          </div>
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
