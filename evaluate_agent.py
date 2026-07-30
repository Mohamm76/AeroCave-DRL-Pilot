# evaluate_agent.py
import sys
import os
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

# إضافة مجلد env للمسار
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from env.drone_cave_env import DroneCaveEnv
from stable_baselines3 import PPO

def main():
    print("🎬 جاري تحميل النموذج المدرب وتقييم أداء الطائرة البصري...")
    
    # 1. تحميل البيئة والنموذج
    env = DroneCaveEnv()
    model = PPO.load("ppo_cave_pilot_final")
    
    obs, info = env.reset()
    done = False
    
    # مصفوفات لتسجيل مسار الطيران والرسم البياني
    x_history = []
    y_history = []
    gravity_history = []
    
    # 2. تشغيل المحاكاة
    while not done:
        # جعل النموذج الذكي يختار الفعل الأفضل بناءً على الحساسات الحالية
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        # تسجيل إحداثيات الطائرة وقيمة الجاذبية في هذه اللحظة
        x_history.append(obs[0])
        y_history.append(obs[1])
        gravity_history.append(obs[6])
        
        done = terminated or truncated

    print(f"🏁 انتهت الرحلة! المسافة المقطوعة للأمام: {x_history[-1]:.2f} متر.")
    if x_history[-1] >= env.cave_length:
        print("🏆 مبروك! الطائرة نجحت في عبور النفق بالكامل دون أي اصطدام!")
    else:
        print("💥 الطائرة اصطدمت بالجدار قبل الوصول للنهاية.")

    # 3. رسم مسار الرحلة فيزيائياً باستخدام Matplotlib
    plt.figure(figsize=(12, 6))
    
    # رسم السقف والأرضية للنفق
    plt.axhline(y=env.cave_height, color='r', linestyle='--', label='Cave Ceiling (السقف)')
    plt.axhline(y=0, color='r', linestyle='--', label='Cave Floor (الأرضية)')
    
    # رسم مسار الطائرة
    plt.plot(x_history, y_history, color='b', linewidth=2, label='Drone Flight Path (مسار الطائرة)')
    plt.scatter(x_history[0], y_history[0], color='g', marker='o', s=100, label='Start Point (البداية)')
    plt.scatter(x_history[-1], y_history[-1], color='black', marker='x', s=100, label='End Point (النهاية)')
    
    plt.title("CavePilot-AMD: Autonomous Drone Navigation in Turbulent Cavern")
    plt.xlabel("Horizontal Distance (m) / المسافة الأفقية")
    plt.ylabel("Flight Altitude (m) / الارتفاع")
    plt.ylim(-1, env.cave_height + 1)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    
    # عرض الرسم البياني
    plt.show()

if __name__ == "__main__":
    main()