// mobile-app/src/hooks/useMobileTelemetry.js
import { useEffect, useState } from 'react';
import { mobileTelemetryService } from '../services/telemetrySocket';

export const useMobileTelemetry = (serverIp = 'localhost') => {
  const [telemetry, setTelemetry] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // تحديد رابط الاتصال بناءً على عنوان السيرفر
    const wsUrl = `ws://${serverIp}:8000/ws/telemetry`;
    mobileTelemetryService.connect(wsUrl);

    const unsubscribeMessage = mobileTelemetryService.subscribeMessage((data) => {
      setTelemetry(data);
    });

    const unsubscribeStatus = mobileTelemetryService.subscribeStatus((status) => {
      setIsConnected(status);
    });

    return () => {
      unsubscribeMessage();
      unsubscribeStatus();
      mobileTelemetryService.disconnect();
    };
  }, [serverIp]);

  return { telemetry, isConnected };
};