import { useState, useEffect } from "react";

export async function handleFetch(url, options = {}, returnOn400, errorMsg) {
  let response;
  let errorMessageResponse;
  try {
    response = await fetch(url, options);
  } catch (error) {
    console.log(error);
    return;
  }
  if (response.status >= 300 && !(response.status == 400 && returnOn400)) {
    const responseText = await response.text();
    try {
      const jsonResponse = JSON.parse(responseText);
      errorMessageResponse = jsonResponse.error.message;
    } catch (error) {
      errorMessageResponse = responseText;
    }
    console.log(errorMessageResponse);
    alert(
      `${errorMsg}\n\n${errorMessageResponse}\n\n--status: ${response.status}`
    );
    return;
  }
  let json;
  try {
    const headers = options?.headers;
    if (headers?.["Content-type"] == "text/html") {
      json = await response.text();
    } else {
      json = await response.json();
    }
  } catch (error) {
    console.log(error);
    alert(`${errorMsg} (${error})`)
    return;
  }
  return json;
}

export function useFetch({
  url,
  errorMsg,
  initData = null,
  rerequest = 1,
  skip = false,
  params = {},
  returnOn400 = false,
  setBackToInitOnRefresh = true,
}) {
  const [data, setData] = useState(initData);
  const [isLoading, setIsLoading] = useState(true);
  const [version, setVersion] = useState(0);

  const [controllerFetch, setControllerFetch] = useState(null);

  const newFetchSignal = () => {
    if (controllerFetch) {
      controllerFetch.abort();
    }
    const newFetchController = new AbortController();
    setControllerFetch(newFetchController);
    return newFetchController.signal;
  };

  const fetchData = async () => {
    setIsLoading(true);
    if (skip) {
      setIsLoading(false);
      return;
    }

    if (setBackToInitOnRefresh) {
      setData(initData);
    }

    params["signal"] = newFetchSignal();
    const result = await handleFetch(url, params, returnOn400, errorMsg);
    if (result) {
      setData(result);
      setIsLoading(false);
      setVersion((prevVersion) => prevVersion + 1);
    } else {
      console.log(
        "Cannot return fetched data as the component is no longer mounted"
      );
    }
  };

  useEffect(() => {
    fetchData();
    return () => controllerFetch?.abort();
  }, [url, rerequest]);

  return { data, isLoading, version };
}
