import { useState, useEffect, useRef, Fragment } from "react";
import { useLogs } from "./hooks";

const REFRESH_TIME = 5000; // 5 seconds

export const LogTerminal = ({ title }) => {
  const [logsVersion, setLogsVersion] = useState(1);
  const { logs, isLoading } = useLogs({ refetch: logsVersion });
  const logContainerRef = useRef(null);
  const [isAtBottom, setIsAtBottom] = useState(true);

  const isScrollAtBottom = () => {
    if (logContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = logContainerRef.current;
      return scrollTop + clientHeight >= scrollHeight - 5; // 5px margin of error
    }
    return false;
  };

  const handleScroll = () => {
    setIsAtBottom(isScrollAtBottom());
  };

  // Keep the scrollbar at the bottom if the user was at the bottom
  useEffect(() => {
    if (isAtBottom && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs, isAtBottom]);

  useEffect(() => {
    const interval = setInterval(() => {
      setLogsVersion((prevVersion) => prevVersion + 1);
    }, REFRESH_TIME);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="terminal">
      <div className="terminal-title">{title}</div>
      <div
        ref={logContainerRef}
        onScroll={handleScroll}
        className="terminal-output">
        <div>
          {isLoading && logs == undefined ? (
            <div className="w-100 text-center">Loading logs...</div>
          ) : (
            <Fragment>
              {logs && (
                <div className="log-content">
                  {logs.map((log, index) => (
                    <p key={index} style={{ margin: 0 }}>
                      {log}
                    </p>
                  ))}
                </div>
              )}
            </Fragment>
          )}
        </div>
      </div>
    </div>
  );
};
