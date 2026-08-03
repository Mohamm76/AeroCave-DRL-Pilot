# agents/train_3d.py
import gymnasium as gym
from stable_baselines3 import PPO
from env.drone_cave_3d_env import AdvancedDroneCave3DEnv  # التعديل الصحيح للمسار
import os

# 1. تهيئة البيئة ثلاثية الأبعاد
env = AdvancedDroneCave3DEnv()

# 2. إعداد مجلدات حفظ النموذج والتقارير (مسارات نسبية متوافقة مع جذر المشروع)
models_dir = "models/PPO_3D"
log_dir = "tensorboard_logs/PPO_3d_runs"  # دمجناها مع مجلد الـ logs الخاص بك
os.makedirs(models_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# 3. بناء الوكيل الذكي (Hyperparameters محسنة للمساحات المستمرة)
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=0.0003,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    tensorboard_log=log_dir
)

# 4. تدريب الوكيل (بدءاً بـ 100 ألف خطوة زمنية كمرحلة أولى)
print("🚀 بدأ تدريب الطائرة المسيرة في البيئة ثلاثية الأبعاد الخطرة...")
TIMESTEPS = 20000
for i in range(1, 6):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO_3D_Run")
    model.save(f"{models_dir}/ppo_drone_cave_3d_{TIMESTEPS * i}_steps")
    print(f"✅ تم حفظ نسخة النموذج عند {TIMESTEPS * i} خطوة زمنية.")

print("🎉 اكتملت المرحلة الأولى من التدريب بنجاح!")