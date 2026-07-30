# env/drone_cave_env.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class DroneCaveEnv(gym.Env):
    """
    بيئة محاكاة مخصصة لطائرة مسيرة تطير داخل نفق ضيق
    تتأثر بقوى جاذبية متغيرة وقوى سحب فيزيائية عند الاقتراب من الجدران
    """
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        super(DroneCaveEnv, self).__init__()
        
        # الأفعال: [قوة الدفع العمودي، قوة الدفع الأفقي]
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        
        # الملاحظات (Sensors): [الوضع الأفقي، الوضع العمودي، السرعة الأفقية، السرعة العمودية، المسافة للسقف، المسافة للأرض، الجاذبية الحالية]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)
        
        # أبعاد النفق
        self.cave_height = 10.0
        self.cave_length = 100.0
        
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # نقطة البداية (x, y, vx, vy)
        self.state = np.array([0.0, 5.0, 0.0, 0.0], dtype=np.float32) 
        
        # توليد جاذبية أساسية متغير لكل شوط (محاكاة شذوذ الجاذبية)
        self.current_gravity = np.random.uniform(7.0, 13.0)
        
        return self._get_obs(), {}

    def _get_obs(self):
        x, y, vx, vy = self.state
        dist_top = self.cave_height - y
        dist_bottom = y
        return np.array([x, y, vx, vy, dist_top, dist_bottom, self.current_gravity], dtype=np.float32)

    def step(self, action):
        x, y, vx, vy = self.state
        thrust_y, thrust_x = action[0] * 15.0, action[1] * 5.0 
        
        # 1. تأثير الجاذبية الديناميكية المتغيرة طفيفاً مع التقدم
        gravity_effect = self.current_gravity + np.sin(x * 0.1) * 2.0
        
        # 2. تأثير السحب القريب من الجدران (Wall-Bounded Aerodynamic Drag)
        dist_bottom = max(y, 0.1)
        dist_top = max(self.cave_height - y, 0.1)
        
        wall_pull_bottom = 0.5 / (dist_bottom ** 2)  
        wall_pull_top = 0.5 / (dist_top ** 2)        
        
        # صافي القوى الفيزيائية المؤثرة
        total_force_y = thrust_y - gravity_effect - wall_pull_bottom + wall_pull_top
        total_force_x = thrust_x - (0.1 * vx)  
        
        # معادلات الحركة لنيوتن (تحديث الموقع والسرعة)
        dt = 0.05
        vx += total_force_x * dt
        vy += total_force_y * dt
        x += vx * dt
        y += vy * dt
        
        self.state = np.array([x, y, vx, vy], dtype=np.float32)
        
        # --- حساب المكافآت والعقوبات المطورة (Advanced Reward Function) ---
        # 1. مكافأة للتقدم للأمام
        reward = vx * 0.5 
        
        # 2. عقوبة قاسية للاهتزاز العمودي غير المستقر
        reward -= 0.2 * (vy ** 2)
        
        # 3. عقوبة الحفاظ على المركز (تُعاقب الطائرة كلما ابتعدت عن منتصف النفق عند الارتفاع 5.0)
        distance_from_center = abs(y - 5.0)
        reward -= 0.5 * distance_from_center
        
        # 4. مكافأة بقاء على قيد الحياة (Survival Reward) لتشجيعها على عدم الانتحار السريع
        reward += 0.1

        terminated = False
        truncated = False
        
        # شروط النهاية المحدثة
        if y <= 0.0 or y >= self.cave_height:
            terminated = True
            reward = -200.0  # ضاعفنا العقوبة لكي يرتعب الـ AI من الجدران
        
        if x >= self.cave_length:
            terminated = True
            reward += 1000.0  # ضاعفنا مكافأة الفوز والوصول للنهاية
            
        return self._get_obs(), reward, terminated, truncated, {}