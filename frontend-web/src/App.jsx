// frontend-web/src/App.jsx
import React from 'react';
import { useTelemetry } from './hooks/useTelemetry';
import DroneCanvas from './components/DroneCanvas';
import TelemetryDashboard from './components/TelemetryDashboard';

function App() {
  const { telemetry, isConnected } = useTelemetry();

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace', backgroundColor: '#0f172a', color: '#f8fafc', minHeight: '100vh' }}>
      
      {/* الهيدر الرئيسي */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
        <h1 style={{ margin: 0, fontSize: '22px' }}>🚁 AeroCave-DRL-Pilot | Real-Time Dashboard</h1>
        <div>
          <strong style={{ color: isConnected ? '#22c55e' : '#ef4444', padding: '6px 12px', backgroundColor: '#1e293b', borderRadius: '6px', border: '1px solid #334155' }}>
            {isConnected ? '🟢 STREAMING (20 FPS)' : '🔴 DISCONNECTED'}
          </strong>
        </div>
      </header>

      {/* شاشة العرض ثلاثي الأبعاد */}
      <div style={{ marginBottom: '20px' }}>
        <DroneCanvas position={telemetry?.position} />
      </div>

      {/* لوحة المؤشرات والإنذارات */}
      <TelemetryDashboard telemetry={telemetry} />
    </div>
  );
}

export default App;