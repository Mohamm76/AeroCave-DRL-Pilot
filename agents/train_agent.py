# agents/train_agent.py
import sys
import os
import gymnasium as gym

# إضافة المجلد الرئيسي للنظام ليتعرف بايثون على بيئتنا المخصصة
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.drone_cave_env import DroneCaveEnv
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback

def main():
    print("🚀 بدء تهيئة بيئة التدريب الذكي لـ CavePilot-AMD...")
    
    # 1. إنشاء البيئة الفيزيائية
    env = DroneCaveEnv()
    
    # 2. إعداد خوارزمية PPO
    # استخدمنا هندسة شبكة عصبية متناسقة (MlpPolicy) بحجم طبقات [64, 64] لتناسب سرعة التدريب المحلي
    model = PPO(
        "MlpPolicy", 
        env, 
        verbose=1, 
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        tensorboard_log="./tensorboard_logs/"
    )
    
    # 3. إعداد نظام حفظ تلقائي للنموذج (Checkpoint) كل 20,000 خطوة
    checkpoint_callback = CheckpointCallback(
        save_freq=20000, 
        save_path='./models/',
        name_prefix='ppo_drone_cave'
    )
    
    # 4. بدء التدريب
    total_timesteps = 100000
    print(f"🏋️‍♂️ سيبدأ تدريب الطائرة الآن على {total_timesteps} خطوة فيزيائية...")
    model.learn(total_timesteps=total_timesteps, callback=checkpoint_callback)
    
    # 5. حفظ النموذج النهائي
    model.save("ppo_cave_pilot_final")
    print("🎉 انتهى التدريب بنجاح! تم حفظ النموذج النهائي باسم 'ppo_cave_pilot_final'")

if __name__ == "__main__":
    main()