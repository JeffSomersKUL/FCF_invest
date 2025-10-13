import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { AppDispatch } from "../../general/store";
import { fetchAssetValue } from "../slice/portfolioSlice";

export function usePrice({ assetId, name }) {
  const dispatch = useDispatch<AppDispatch>();
  useEffect(() => {
    dispatch(fetchAssetValue(assetId));
  }, [assetId]);
}
