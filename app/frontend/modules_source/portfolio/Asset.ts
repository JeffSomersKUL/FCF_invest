type Currency = "EUR" | "USD" | "GBP";
type AssetType = "stock" | "option" | "custom" | "bill";

export interface IBaseAsset {
  assetId: number;
  type: AssetType;
}

interface ITradableAsset extends IBaseAsset {
  ticker: string;
  name?: string;
  currency: Currency;
  exchange?: string;
  industry?: string;
}

export interface IStock extends ITradableAsset {
  type: "stock";
}

export interface IOptions extends ITradableAsset {
  type: "option";
}

export interface ICustomStock extends ITradableAsset {
  type: "custom";
}

export interface IGovBill extends IBaseAsset {
  type: "bill";
  issuer: string;
  faceValue: number;
  maturityDate: string;
  discountRate: number;
}

export type Asset = IStock | IOptions | ICustomStock | IGovBill;

export interface IAssetHolding<T extends Asset = Asset> {
  asset: T;
  quantity: number;
}

export interface IAssetValue {
  price: number;
  trackable: boolean
}
