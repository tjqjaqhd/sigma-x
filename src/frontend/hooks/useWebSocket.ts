// SIGMA React Dashboard용 WebSocket Hook
// `docs/4_development/module_specs/interfaces/ReactDashboard_UseWebSocket_Spec.md` 사양을 따른다.

import { useEffect, useRef } from "react";

export function useWebSocket(url: string) {
  const wsRef = useRef<WebSocket | null>(null);

  const connect = () => {
    if (wsRef.current) return;
    wsRef.current = new WebSocket(url);
  };

  const disconnect = () => {
    wsRef.current?.close();
    wsRef.current = null;
  };

  const onMessage = (handler: (data: any) => void) => {
    if (!wsRef.current) return;
    wsRef.current.onmessage = (ev) => {
      try {
        handler(JSON.parse(ev.data));
      } catch {
        console.error("invalid ws message", ev.data);
      }
    };
  };

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [url]);

  return { connect, disconnect, onMessage };
}
