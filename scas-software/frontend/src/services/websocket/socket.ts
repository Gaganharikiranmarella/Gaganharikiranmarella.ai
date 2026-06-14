let socket: WebSocket | null = null;

export function createSocket() {

  if (socket) {
    return socket;
  }

  socket = new WebSocket(
    "ws://localhost:8000/ws"
  );

  return socket;
}