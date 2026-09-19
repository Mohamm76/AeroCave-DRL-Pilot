// mobile-app/src/services/telemetrySocket.js

class MobileTelemetryService {
  constructor(url = 'ws://10.0.2.2:8000/ws/telemetry') {
    // ملاحظة: 10.0.2.2 مخصص لمشارك محاكي Android Studio للاتصال بـ localhost
    // إذا كنت تستخدم هاتف حقيقي عبر WiFi، استبدلها بـ IP جهازك (مثال: ws://192.168.1.5:8000/ws/telemetry)
    this.url = url;
    this.socket = null;
    this.onMessageCallbacks = [];
    this.onStatusCallbacks = [];
    this.reconnectInterval = 3000;
    this.isIntentionalClose = false;
  }

  connect(customUrl = null) {
    if (customUrl) this.url = customUrl;
    this.isIntentionalClose = false;

    try {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        console.log('⚡ [Mobile WS] Connected to Telemetry Stream');
        this.notifyStatus(true);
      };

      this.socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          this.notifyMessage(payload);
        } catch (err) {
          console.error('❌ [Mobile WS] JSON Parse Error:', err);
        }
      };

      this.socket.onerror = (error) => {
        console.error('⚠️ [Mobile WS] Error:', error.message);
      };

      this.socket.onclose = () => {
        console.warn('🔌 [Mobile WS] Connection Closed');
        this.notifyStatus(false);

        if (!this.isIntentionalClose) {
          setTimeout(() => this.connect(), this.reconnectInterval);
        }
      };
    } catch (e) {
      console.error('❌ [Mobile WS] Connection Exception:', e);
    }
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

export const mobileTelemetryService = new MobileTelemetryService();