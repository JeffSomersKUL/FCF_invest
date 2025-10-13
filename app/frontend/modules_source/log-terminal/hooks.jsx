import { useFetch } from "../general/fetch";

export function useLogs({ refetch }) {
  const { data, isLoading } = useFetch({
    url: window.__ENDPOINT_CONTENT__,
    errorMsg: "Could not load the logs",
    rerequest: refetch,
    setBackToInitOnRefresh: false,
  });

  var logs = data?.logs;

  if (!logs) {
    logs = undefined;
  }

  return { logs: logs, isLoading: isLoading };
}
