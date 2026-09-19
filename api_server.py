# api_server.py
import asyncio
import json
import os
import numpy as np
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from stable_baselines3 import PPO

from env.drone_cave_3d_env import AdvancedDroneCave3DEnv
from agents.comparison_agents import DummySACAgent, DummyDQNAgent

# ---------------------------------------------------------
# 0. تحميل متغيرات البيئة من ملف .env
# ---------------------------------------------------------
load_dotenv()

app = FastAPI(title="AeroCave-DRL-Pilot Telemetry Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 1. إعدادات قاعدة البيانات (PostgreSQL Dynamic & Secure Config)
# ---------------------------------------------------------
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "cavepilot_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

def save_log_to_db(session_id, step, x, y, z, vx, vy, vz, battery, algo, status, reward):
    """حفظ سجل الطيران في PostgreSQL مع حماية كاملة"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
        INSERT INTO flight_logs 
        (session_id, step_number, pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, battery_level, current_algorithm, status, reward)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (session_id, step, x, y, z, vx, vy, vz, battery, algo, status, reward))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ DB Logging Notice: {e}")

# ---------------------------------------------------------
# 2. نمط التصميم (Factory Pattern)
# ---------------------------------------------------------
def get_agent(algo_name: str):
    algo_name = algo_name.upper()
    if algo_name == "PPO":
        try:
            if os.path.exists("ppo_cave_pilot_final.zip"):
                print("📦 تم تحميل نموذج PPO النهائي بنجاح!")
                return PPO.load("ppo_cave_pilot_final.zip")
            elif os.path.exists("models/PPO_3D/ppo_drone_cave_3d_100000_steps.zip"):
                print("📦 تم تحميل نموذج PPO ذو 100k خطوة!")
                return PPO.load("models/PPO_3D/ppo_drone_cave_3d_100000_steps.zip")
            else:
                print("⚠️ لم يتم العثور على ملف النموذج، يتم استخدام Dummy Agent...")
                return DummySACAgent()
        except Exception as e:
            print(f"⚠️ خطأ أثناء تحميل PPO: {e}. سيتم استخدام Dummy Agent.")
            return DummySACAgent()
    elif algo_name == "SAC":
        return DummySACAgent()
    elif algo_name == "DQN":
        return DummyDQNAgent()
    else:
        return DummySACAgent()

def np_random_id():
    import random
    return random.randint(1000, 9999)

# ---------------------------------------------------------
# 3. WebSocket للبث الحي والتفاعلي
# ---------------------------------------------------------
@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    print("⚡ تم اتصال عميل جديد بـ WebSocket Telemetry!")
    
    try:
        env = AdvancedDroneCave3DEnv()
        obs, _ = env.reset()
    except Exception as e:
        print(f"❌ خطأ أثناء تهيئة البيئة: {e}")
        await websocket.close()
        return

    current_algo = "PPO"
    agent = get_agent(current_algo)
    session_id = f"SESSION_{np_random_id()}"
    step_count = 0
    battery = 100.0
    
    try:
        while True:
            # 1. التنبؤ بالفصل الحركي مع تكييف أبعاد الملاحظة (Observation Guard)
            try:
                if hasattr(agent, "observation_space") and hasattr(agent.observation_space, "shape") and agent.observation_space.shape[0] == 7:
                    action, _ = agent.predict(obs[:7], deterministic=True)
                else:
                    action, _ = agent.predict(obs, deterministic=True)
            except Exception as e:
                action = np.array([0.1, 0.0, 0.5])

            # 2. حماية وتكييف أبعاد الفعل (Action Guard) لتوافق الـ 3D Env
            action = np.array(action).flatten()
            if len(action) < 3:
                # إذا كان النموذج يُنتج بعدين فقط، نكمل المحور الثالث بـ 0.5 لتوازن الطائرة
                action = np.pad(action, (0, 3 - len(action)), mode='constant', constant_values=0.5)

            # 3. خطوة البيئة
            try:
                obs, reward, terminated, truncated, _ = env.step(action)
                x, y, z, vx, vy, vz, dist_top, dist_bottom, dist_left, dist_right, gravity = obs
            except Exception as e:
                print(f"❌ خطأ في خطوة البيئة (env.step): {e}")
                break

            step_count += 1
            battery = max(0.0, battery - 0.05)
            
            flight_status = "FLYING"
            if terminated:
                flight_status = "FINISHED" if x >= env.cave_length else "CRASHED"

            telemetry_payload = {
                "step": step_count,
                "session_id": session_id,
                "algorithm": current_algo,
                "position": {"x": float(x), "y": float(y), "z": float(z)},
                "velocity": {"vx": float(vx), "vy": float(vy), "vz": float(vz)},
                "sensors": {
                    "dist_top": float(dist_top),
                    "dist_bottom": float(dist_bottom),
                    "dist_left": float(dist_left),
                    "dist_right": float(dist_right)
                },
                "environment": {"gravity": float(gravity)},
                "telemetry": {"battery": round(battery, 2), "status": flight_status, "reward": round(float(reward), 4)}
            }
            
            # إرسال الحزمة عبر WebSocket
            await websocket.send_json(telemetry_payload)
            
            # حفظ السجل في قاعدة البيانات دون تعطيل الـ Loop
            asyncio.create_task(asyncio.to_thread(
                save_log_to_db, session_id, step_count, float(x), float(y), float(z), 
                float(vx), float(vy), float(vz), round(battery, 2), 
                current_algo, flight_status, float(reward)
            ))
            
            if terminated or truncated:
                obs, _ = env.reset()
                battery = 100.0
                session_id = f"SESSION_{np_random_id()}"
                step_count = 0
                await asyncio.sleep(1.0)
                
            await asyncio.sleep(0.05)

    except WebSocketDisconnect:
        print("🔌 تم قطع الاتصال بالعميل.")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

@app.get("/")
def root():
    return {"message": "AeroCave Telemetry Engine Active", "status": "Running"}