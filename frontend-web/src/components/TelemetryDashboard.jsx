// frontend-web/src/components/TelemetryDashboard.jsx
import React from 'react';

export default function TelemetryDashboard({ telemetry }) {
  if (!telemetry) return null;

  const { position, telemetry: stats, sensors } = telemetry;
  const isCrashed = stats?.status === 'CRASHED';
  const battery = stats?.battery ?? 0;

  // تحديد لون البطارية
  const getBatteryColor = (level) => {
    if (level > 50) return '#22c55e'; // أخضر
    if (level > 20) return '#eab308'; // أصفر
    return '#ef4444'; // أحمر
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
      
      {/* ⚠️ تنبيه الخطر في حال الاصطدام */}
      {isCrashed && (
        <div style={alertStyle}>
          🚨 WARNING: DRONE CRASH DETECTED! IMMEDIATE ATTENTION REQUIRED
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '15px' }}>
        
        {/* 1. بطاقة الموقع والإحداثيات */}
        <div style={cardStyle}>
          <h3 style={cardTitleStyle}>📍 3D Coordinates</h3>
          <div style={rowStyle}><span>X-Axis:</span> <strong>{position?.x?.toFixed(2)} m</strong></div>
          <div style={rowStyle}><span>Y-Axis:</span> <strong>{position?.y?.toFixed(2)} m</strong></div>
          <div style={rowStyle}><span>Z-Altitude:</span> <strong>{position?.z?.toFixed(2)} m</strong></div>
        </div>

        {/* 2. بطاقة الطاقة والمكافأة */}
        <div style={cardStyle}>
          <h3 style={cardTitleStyle}>⚡ System Performance</h3>
          
          <div style={{ marginBottom: '10px' }}>
            <div style={rowStyle}>
              <span>Battery Level:</span>
              <strong>{battery}%</strong>
            </div>
            {/* شريط البطارية */}
            <div style={barBackgroundStyle}>
              <div style={{ ...barFillStyle, width: `${battery}%`, backgroundColor: getBatteryColor(battery) }} />
            </div>
          </div>

          <div style={rowStyle}>
            <span>Flight Status:</span>
            <strong style={{ color: isCrashed ? '#ef4444' : '#22c55e' }}>{stats?.status}</strong>
          </div>
          <div style={rowStyle}>
            <span>RL Reward:</span>
            <strong>{stats?.reward?.toFixed(4)}</strong>
          </div>
        </div>

        {/* 3. رادار حساسات الليدار (LiDAR) */}
        <div style={cardStyle}>
          <h3 style={cardTitleStyle}>📡 LiDAR Distance Proximity</h3>
          
          <SensorBar label="Top" distance={sensors?.dist_top} maxDist={15} />
          <SensorBar label="Bottom" distance={sensors?.dist_bottom} maxDist={15} />
          <SensorBar label="Left" distance={sensors?.dist_left} maxDist={15} />
          <SensorBar label="Right" distance={sensors?.dist_right} maxDist={15} />
        </div>

      </div>
    </div>
  );
}

// مكوّن فرعي لشريط مسافة الحساسات
function SensorBar({ label, distance = 0, maxDist = 15 }) {
  const percentage = Math.min(Math.max((distance / maxDist) * 100, 0), 100);
  const isClose = distance < 1.5;

  return (
    <div style={{ marginBottom: '8px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '2px' }}>
        <span>{label}</span>
        <span style={{ color: isClose ? '#ef4444' : '#94a3b8' }}>{distance?.toFixed(2)} m</span>
      </div>
      <div style={barBackgroundStyle}>
        <div style={{ ...barFillStyle, width: `${percentage}%`, backgroundColor: isClose ? '#ef4444' : '#38bdf8' }} />
      </div>
    </div>
  );
}

// التنسيقات
const cardStyle = {
  backgroundColor: '#1e293b',
  padding: '16px',
  borderRadius: '10px',
  border: '1px solid #334155'
};

const cardTitleStyle = {
  marginTop: 0,
  marginBottom: '12px',
  fontSize: '15px',
  color: '#38bdf8',
  borderBottom: '1px solid #334155',
  paddingBottom: '6px'
};

const rowStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  marginBottom: '6px',
  fontSize: '13px'
};

const barBackgroundStyle = {
  width: '100%',
  height: '8px',
  backgroundColor: '#0f172a',
  borderRadius: '4px',
  overflow: 'hidden'
};

const barFillStyle = {
  height: '100%',
  transition: 'width 0.1s ease-in-out'
};

const alertStyle = {
  backgroundColor: '#7f1d1d',
  color: '#fecaca',
  padding: '12px',
  borderRadius: '8px',
  border: '1px solid #ef4444',
  fontWeight: 'bold',
  textAlign: 'center',
  animation: 'pulse 1s infinite'
};