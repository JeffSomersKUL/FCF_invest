import React from "react";
import { useSelector } from "react-redux";
import ReactEcharts from "echarts-for-react";

function formatNumber(number: number) {
  return new Intl.NumberFormat("de-DE", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(number);
}

function getAssetsTotals(assets: any[]) {
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
    assetsUSD: assetsUSD * (window.__USD_RATE__ || 1),
    assetsGBP: assetsGBP * (window.__GBP_RATE__ || 1),
  };
}

function BalanceChart2({
  cashEuro,
  cashUSD,
  cashGBP,
  assetsEuro,
  assetsUSD,
  assetsGBP,
}: {
  cashEuro: number;
  cashUSD: number;
  cashGBP: number;
  assetsEuro: number;
  assetsUSD: number;
  assetsGBP: number;
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
  const totalValue = filteredSeriesData.reduce((sum, item) => sum + item.value, 0);
  const assetLegendData = filteredSeriesData.filter((item) => item.category === "assets").map((item) => item.name);
  const cashLegendData = filteredSeriesData.filter((item) => item.category === "cash").map((item) => item.name);
  const colors = filteredSeriesData.map((item) => item.color);
  const option = {
    tooltip: {
      trigger: "item",
      formatter: function (params: any) {
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
        formatter: function (name: string) {
          const item = filteredSeriesData.find((data) => data.name === name);
          if (item) {
            const percentage = totalValue > 0 ? ((item.value / totalValue) * 100).toFixed(1) : 0;
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
        formatter: function (name: string) {
          const item = filteredSeriesData.find((data) => data.name === name);
          if (item) {
            const percentage = totalValue > 0 ? ((item.value / totalValue) * 100).toFixed(1) : 0;
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
          formatter: (params: any) => {
            const item = filteredSeriesData.find((data) => data.name === params.name);
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

export function Summary({ balanceCash }: { balanceCash: any }) {
  const cashEuro = balanceCash.EUR || 0;
  const cashUSD = (balanceCash.USD || 0) * (window.__USD_RATE__ || 1);
  const cashGBP = (balanceCash.GBP || 0) * (window.__GBP_RATE__ || 1);
  const assetsObject = useSelector((state: any) => state.assets.assets);
  const assets = Object.values(assetsObject);
  const { assetsEuro, assetsUSD, assetsGBP } = getAssetsTotals(assets);
  const totalCash = cashEuro + cashUSD + cashGBP + assetsEuro + assetsUSD + assetsGBP;
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
