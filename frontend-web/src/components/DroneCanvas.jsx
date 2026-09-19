// frontend-web/src/components/DroneCanvas.jsx
import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid } from '@react-three/drei';

// مجسم دروّن واضح مع 4 مراوح وإضاءة
function Drone({ position }) {
  const groupRef = useRef();

  useFrame(() => {
    if (groupRef.current && position) {
      // ضبط المقياس والموقع بحيث تظهر بوضوح وسط النفق
      // نضرب القيم في 0.5 إذا كانت المسافات بالخادم كبيرة، أو نضع الإحداثيات المباشرة
      const posX = typeof position.x === 'number' ? position.x : 0;
      const posY = typeof position.y === 'number' ? position.y : 0;
      const posZ = typeof position.z === 'number' ? position.z : 0;

      // ضبط المحاور الثلاثة
      groupRef.current.position.set(posX, posZ * 0.5, -posY * 0.5);
    }
  });

  return (
    <group ref={groupRef} position={[0, 1, 0]}>
      {/* جسم الطائرة الرئيسي - حجم أكبر ورؤية أوضح */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[1.5, 0.4, 1.5]} />
        <meshStandardMaterial color="#00f0ff" emissive="#003847" roughness={0.2} metalness={0.9} />
      </mesh>

      {/* الضوء الأمامي الاستكشافي */}
      <mesh position={[0, 0, -0.85]}>
        <sphereGeometry args={[0.25, 16, 16]} />
        <meshBasicMaterial color="#ef4444" />
      </mesh>
      <pointLight position={[0, 0, -1]} distance={5} intensity={4} color="#ef4444" />

      {/* المراوح الأربعة في الأطراف */}
      {[
        [-0.9, 0.2, -0.9],
        [0.9, 0.2, -0.9],
        [-0.9, 0.2, 0.9],
        [0.9, 0.2, 0.9],
      ].map((pos, idx) => (
        <group key={idx} position={pos}>
          <mesh>
            <cylinderGeometry args={[0.4, 0.4, 0.05, 16]} />
            <meshStandardMaterial color="#38bdf8" wireframe />
          </mesh>
        </group>
      ))}
    </group>
  );
}

// الشبكة والأرضية
function CaveTunnel() {
  return (
    <Grid
      position={[0, -1, 0]}
      args={[40, 100]}
      cellSize={1}
      cellThickness={1}
      cellColor="#1e293b"
      sectionSize={5}
      sectionThickness={1.5}
      sectionColor="#00f0ff"
      fadeDistance={60}
    />
  );
}

export default function DroneCanvas({ position }) {
  return (
    <div style={{ width: '100%', height: '420px', backgroundColor: '#030712', borderRadius: '12px', overflow: 'hidden', border: '1px solid #1e293b' }}>
      <Canvas camera={{ position: [0, 6, 12], fov: 55 }}>
        {/* إضاءة المشهد */}
        <ambientLight intensity={1.5} />
        <directionalLight position={[10, 20, 15]} intensity={2.0} />
        <pointLight position={[0, 8, 0]} intensity={2.5} color="#00f0ff" />

        {/* عناصر المشهد */}
        <CaveTunnel />
        <Drone position={position} />

        {/* التحكم بالماوس (إمكانية التكبير والتدوير) */}
        <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} target={[0, 1, 0]} />
      </Canvas>
    </div>
  );
}