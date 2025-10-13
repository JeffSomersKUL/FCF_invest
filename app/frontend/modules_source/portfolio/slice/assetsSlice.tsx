import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import fetchAssetData from "../fetchData";

export const fetchAssetPrice = createAsyncThunk(
  "assets/fetchAssetPrice",
  async (assetId, { rejectWithValue }) => {
    try {
      const data = await fetchAssetData({
        url: `asset/${assetId}`,
        errorMsg: `Error fetching asset price for asset ID ${assetId}`,
      });

      return data;
    } catch (error) {
      console.error(`Failed to fetch asset price for ${assetId}:`, error);
      return rejectWithValue(error.message);
    }
  }
);

const initialState = {
  assets: {},
};

const assetsSlice = createSlice({
  name: "assets",
  initialState,
  reducers: {
    setAssets(state, action) {
      const assetsArray = action.payload;
      state.assets = assetsArray.reduce((acc, asset) => {
        acc[asset.id] = asset;
        return acc;
      }, {});
    },
    addAsset(state, action) {
      const newAsset = action.payload;
      state.assets[newAsset.id] = newAsset;
    },
    updateAsset(state, action) {
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
    builder.addCase(fetchAssetPrice.fulfilled, (state, action) => {
      const { asset_id, price, live_trackable } = action.payload;
      if (state.assets[asset_id]) {
        state.assets[asset_id].live_trackable = live_trackable;
        if (live_trackable) {
          state.assets[asset_id].price = price;
        }
      }
    });
  },
});

export const { setAssets, updateAsset, addAsset } = assetsSlice.actions;
export default assetsSlice.reducer;
