// frontend-web/src/hooks/useTelemetry.js
import { useEffect, useState } from 'react';
import { telemetryService } from '../services/telemetrySocket';

export const useTelemetry = () => {
  const [telemetry, setTelemetry] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    telemetryService.connect();

    const unsubscribeMessage = telemetryService.subscribeMessage((data) => {
      setTelemetry(data);
    });

    const unsubscribeStatus = telemetryService.subscribeStatus((status) => {
      setIsConnected(status);
    });

    return () => {
      unsubscribeMessage();
      unsubscribeStatus();
      telemetryService.disconnect();
    };
  }, []);

  return { telemetry, isConnected };
};