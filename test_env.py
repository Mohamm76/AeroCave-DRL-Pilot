# test_env.py
import sys
import os
# إضافة مجلد env إلى المسار لكي يتعرف بايثون على الاستيراد
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from env.drone_cave_env import DroneCaveEnv

try:
    env = DroneCaveEnv()
    obs, info = env.reset()
    print("\n✅ تم تحميل البيئة المخصصة بنجاح دون أي أخطاء!")
    print(f"📡 القراءات الأولية للحساسات: {obs}\n")
    
    # تجربة حركة عشوائية
    action = env.action_space.sample()
    next_obs, reward, terminated, truncated, info = env.step(action)
    print(f"⚙️ تم محاكاة خطوة فيزيائية بنجاح! المكافأة المبدئية المكتسبة: {reward:.4f}\n")
except Exception as e:
    print(f"❌ حدث خطأ أثناء تشغيل البيئة: {e}")