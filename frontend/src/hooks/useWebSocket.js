import { useEffect, useState, useCallback } from 'react';

/**
 * Custom hook for WebSocket connection
 * @param {number} projectId - The project ID to subscribe to
 * @param {function} onMessage - Callback function to handle incoming messages
 * @returns {object} - { sendMessage, connected, error }
 */
const useWebSocket = (projectId, onMessage) => {
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState(null);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    // For demo purposes, we are not using authentication token in development
    // In production, you would get the token from context or localStorage
    const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/${projectId}`);

    ws.onopen = () => {
      setConnected(true);
      setError(null);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (e) {
        console.error('Error parsing WebSocket message:', e);
      }
    };

    ws.onerror = (event) => {
      setError(event);
      console.error('WebSocket error:', event);
    };

    ws.onclose = () => {
      setConnected(false);
      setWs(null);
    };

    setWs(ws);

    // Cleanup on unmount or when projectId changes
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [projectId, onMessage]);

  const sendMessage = useCallback((message) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected.');
    }
  }, [ws]);

  return { sendMessage, connected, error };
};

export default useWebSocket;