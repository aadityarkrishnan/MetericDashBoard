// frontend/src/utils/websocket.js

export const createWebSocket = (onMessage) => {
    const socket = new WebSocket('ws://localhost:8000/ws/metrics/');
  
    socket.onopen = () => {
      console.log('WebSocket connection established');
    };
  
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };
  
    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  
    socket.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
      // Optionally implement reconnection logic here
    };
  
    return socket;
  };
  