import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import axios from "axios";
import { IAssetValue, Asset, IBaseAsset } from "../Asset";

export const fetchAssetValue = createAsyncThunk<
  { assetId: IBaseAsset["assetId"] } & IAssetValue,
  IBaseAsset["assetId"],
  { rejectValue: string }
>("assets/fetchAssetValue", async (assetId, { rejectWithValue }) => {
  try {
    const response = await axios.get<{
      status: string;
      asset_id: number;
      price: number;
      live_trackable: boolean;
      message?: string;
    }>(`/portfolio/asset/${assetId}`);

    if (response.data.status !== "success") {
      return rejectWithValue(
        response.data.message || "Invalid response from server"
      );
    }

    return {
      assetId: response.data.asset_id,
      price: response.data.price,
      trackable: response.data.live_trackable,
    };
  } catch (error: any) {
    return rejectWithValue(
      error.response?.data?.message || `Failed to fetch asset price`
    );
  }
});

const initialState = {
  assets: [] as Asset[],
  assetHoldings: {} as Record<IBaseAsset["assetId"], IAssetValue>,
  loadingAssetPrices: [] as IBaseAsset["assetId"][],
  ratesToEUR: {
    USD: 1,
    GBP: 1,
  },
  balance: 0 as number,
};

const assetsSlice = createSlice({
  name: "assets",
  initialState,
  reducers: {
    setAssets(state, action: PayloadAction<Asset[]>) {
      const assetsArray = action.payload;
      state.assets = assetsArray.reduce((acc, asset) => {
        acc[asset.id] = asset;
        return acc;
      }, {});
    },
    setRatesToEUR(state, action: PayloadAction<{ USD: number; GBP: number }>) {
      state.ratesToEUR = action.payload;
    },
    setBalance(state, action: PayloadAction<number>) {
      state.balance = action.payload;
    },
    updateAsset(state, action: PayloadAction<{ id: number; newData: Asset }>) {
      const { id, newData } = action.payload;
      if (state.assets[id]) {
        state.assets[id] = {
          ...state.assets[id],
          ...newData,
        };
      }
    },
  },
  extraReducers: (builder) => {
    builder.addCase(fetchAssetValue.pending, (state, action) => {
      const assetId = action.meta.arg;
      state.loadingAssetPrices.push(assetId);
    });
    builder.addCase(fetchAssetValue.fulfilled, (state, action) => {
      const { assetId, price, trackable } = action.payload;
      state.assetHoldings[assetId] = { price, trackable };
      state.loadingAssetPrices = state.loadingAssetPrices.filter(
        (id) => id !== assetId
      );
    });
    builder.addCase(fetchAssetValue.rejected, (state, action) => {
      const assetId = action.meta.arg;
      state.loadingAssetPrices = state.loadingAssetPrices.filter(
        (id) => id !== assetId
      );
    });
  },
});

export const { setAssets, updateAsset } = assetsSlice.actions;
export default assetsSlice.reducer;
