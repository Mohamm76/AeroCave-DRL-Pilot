// frontend-web/src/services/telemetrySocket.js

class TelemetrySocketService {
  constructor(url = 'ws://localhost:8000/ws/telemetry') {
    this.url = url;
    this.socket = null;
    this.onMessageCallbacks = [];
    this.onStatusCallbacks = [];
    this.reconnectInterval = 3000;
    this.isIntentionalClose = false;
  }

  connect() {
    this.isIntentionalClose = false;
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      console.log('⚡ [WebSocket] Connected to Telemetry Engine');
      this.notifyStatus(true);
    };

    this.socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        this.notifyMessage(payload);
      } catch (err) {
        console.error('❌ [WebSocket] Parsing error:', err);
      }
    };

    this.socket.onerror = (error) => {
      console.error('⚠️ [WebSocket] Error:', error);
    };

    this.socket.onclose = () => {
      console.warn('🔌 [WebSocket] Connection closed');
      this.notifyStatus(false);
      
      if (!this.isIntentionalClose) {
        console.log(`🔄 [WebSocket] Reconnecting in ${this.reconnectInterval / 1000}s...`);
        setTimeout(() => this.connect(), this.reconnectInterval);
      }
    };
  }

  disconnect() {
    this.isIntentionalClose = true;
    if (this.socket) {
      this.socket.close();
    }
  }

  subscribeMessage(callback) {
    this.onMessageCallbacks.push(callback);
    return () => {
      this.onMessageCallbacks = this.onMessageCallbacks.filter(cb => cb !== callback);
    };
  }

  subscribeStatus(callback) {
    this.onStatusCallbacks.push(callback);
    return () => {
      this.onStatusCallbacks = this.onStatusCallbacks.filter(cb => cb !== callback);
    };
  }

  notifyMessage(data) {
    this.onMessageCallbacks.forEach(cb => cb(data));
  }

  notifyStatus(connected) {
    this.onStatusCallbacks.forEach(cb => cb(connected));
  }
}

export const telemetryService = new TelemetrySocketService();