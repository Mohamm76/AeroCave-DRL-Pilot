// mobile-app/App.js
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, Vibration, TextInput, TouchableOpacity, ScrollView, SafeAreaView } from 'react-native';
import { useMobileTelemetry } from './src/hooks/useMobileTelemetry';

export default function App() {
  // تم تعيين عنوان الـ IP الخاص بك مباشرة
  const [serverIp, setServerIp] = useState('192.168.8.6'); 
  const [activeIp, setActiveIp] = useState('192.168.8.6');
  const { telemetry, isConnected } = useMobileTelemetry(activeIp);

  const isCrashed = telemetry?.telemetry?.status === 'CRASHED';
  const battery = telemetry?.telemetry?.battery ?? 0;

  // 🔔 المهمة 7: تفعيل وحدة الاهتزاز (Vibration API) فور اكتشاف الخطر أو الاصطدام
  useEffect(() => {
    if (isCrashed) {
      // نمط اهتزاز طوارئ: (انتظار 0ms، اهتزاز 500ms، توقف 200ms، اهتزاز 500ms)
      Vibration.vibrate([0, 500, 200, 500]);
    }
  }, [isCrashed]);

  const handleConnect = () => {
    setActiveIp(serverIp);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        
        {/* الهيدر وعنوان التطبيق */}
        <Text style={styles.headerTitle}>🚁 AeroCave Pilot HUD</Text>
        <Text style={styles.headerSubtitle}>Field Emergency & Telemetry Monitor</Text>

        {/* إعدادات الاتصال بالسيرفر */}
        <View style={styles.ipContainer}>
          <TextInput
            style={styles.input}
            value={serverIp}
            onChangeText={setServerIp}
            placeholder="Enter Host IP (e.g. 192.168.8.6)"
            placeholderTextColor="#64748b"
            keyboardType="numeric"
          />
          <TouchableOpacity style={styles.connectBtn} onPress={handleConnect}>
            <Text style={styles.connectBtnText}>Connect</Text>
          </TouchableOpacity>
        </View>

        {/* مؤشر حالة الاتصال */}
        <View style={styles.statusBadge}>
          <Text style={[styles.statusText, { color: isConnected ? '#22c55e' : '#ef4444' }]}>
            {isConnected ? '🟢 LIVE CONNECTED' : '🔴 DISCONNECTED'}
          </Text>
        </View>

        {/* 🚨 المهمة 6 & 7: تنبيه الخطر الميداني عالي التباين */}
        {isCrashed && (
          <View style={styles.dangerBanner}>
            <Text style={styles.dangerText}>🚨 CRASH WARNING 🚨</Text>
            <Text style={styles.dangerSubtext}>IMPACT DETECTED IN CAVE SYSTEM</Text>
          </View>
        )}

        {/* كروت البيانات الميدانية عالية التباين (High-Contrast Field UI) */}
        {telemetry ? (
          <View style={styles.grid}>
            
            {/* بطاقة الإحداثيات */}
            <View style={styles.card}>
              <Text style={styles.cardTitle}>📍 POSITION (METERS)</Text>
              <Text style={styles.metricText}>X: <Text style={styles.valueText}>{telemetry.position?.x?.toFixed(2)}</Text></Text>
              <Text style={styles.metricText}>Y: <Text style={styles.valueText}>{telemetry.position?.y?.toFixed(2)}</Text></Text>
              <Text style={styles.metricText}>Z: <Text style={styles.valueText}>{telemetry.position?.z?.toFixed(2)}</Text></Text>
            </View>

            {/* بطاقة البطارية والحالة */}
            <View style={styles.card}>
              <Text style={styles.cardTitle}>⚡ SYSTEM STATUS</Text>
              <Text style={styles.metricText}>Status: 
                <Text style={{ color: isCrashed ? '#ef4444' : '#22c55e', fontWeight: 'bold' }}> {telemetry.telemetry?.status}</Text>
              </Text>
              <Text style={styles.metricText}>Battery: <Text style={styles.valueText}>{battery}%</Text></Text>
              <Text style={styles.metricText}>Reward: <Text style={styles.valueText}>{telemetry.telemetry?.reward?.toFixed(2)}</Text></Text>
            </View>

            {/* بطاقة الليدار الرادارية */}
            <View style={styles.card}>
              <Text style={styles.cardTitle}>📡 LIDAR PROXIMITY</Text>
              <Text style={styles.metricText}>Top: <Text style={styles.valueText}>{telemetry.sensors?.dist_top?.toFixed(2)} m</Text></Text>
              <Text style={styles.metricText}>Bottom: <Text style={styles.valueText}>{telemetry.sensors?.dist_bottom?.toFixed(2)} m</Text></Text>
              <Text style={styles.metricText}>Left: <Text style={styles.valueText}>{telemetry.sensors?.dist_left?.toFixed(2)} m</Text></Text>
              <Text style={styles.metricText}>Right: <Text style={styles.valueText}>{telemetry.sensors?.dist_right?.toFixed(2)} m</Text></Text>
            </View>

          </View>
        ) : (
          <Text style={styles.waitingText}>⏳ Press Connect to stream field data...</Text>
        )}

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#030712',
  },
  scrollContent: {
    padding: 20,
    paddingTop: 40,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#38bdf8',
    textAlign: 'center',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#94a3b8',
    textAlign: 'center',
    marginBottom: 15,
  },
  ipContainer: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 15,
  },
  input: {
    flex: 1,
    backgroundColor: '#0f172a',
    color: '#fff',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  connectBtn: {
    backgroundColor: '#0284c7',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 8,
    justifyContent: 'center',
  },
  connectBtnText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  statusBadge: {
    alignItems: 'center',
    marginBottom: 15,
  },
  statusText: {
    fontWeight: 'bold',
    fontSize: 14,
  },
  dangerBanner: {
    backgroundColor: '#7f1d1d',
    padding: 15,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#ef4444',
    marginBottom: 20,
    alignItems: 'center',
  },
  dangerText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 18,
  },
  dangerSubtext: {
    color: '#fecaca',
    fontSize: 12,
    marginTop: 4,
  },
  grid: {
    gap: 15,
  },
  card: {
    backgroundColor: '#0f172a',
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#1e293b',
  },
  cardTitle: {
    color: '#38bdf8',
    fontSize: 12,
    fontWeight: 'bold',
    marginBottom: 8,
    letterSpacing: 1,
  },
  metricText: {
    color: '#94a3b8',
    fontSize: 15,
    marginBottom: 4,
  },
  valueText: {
    color: '#f8fafc',
    fontWeight: 'bold',
  },
  waitingText: {
    color: '#64748b',
    textAlign: 'center',
    marginTop: 40,
  },
});