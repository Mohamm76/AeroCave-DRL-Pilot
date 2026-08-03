# env/drone_cave_3d_env.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class AdvancedDroneCave3DEnv(gym.Env):
    """
    بيئة محاكاة متطورة ثلاثية الأبعاد (3D) لطائرة مسيرة تطير داخل نفق ديناميكي.
    تتأثر بقوى الجاذبية المتغيرة وقوى سحب الجدران الهوائية الأسيّة من السقف، الأرض، والجوانب.
    """
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        super(AdvancedDroneCave3DEnv, self).__init__()
        
        # 1. الأفعال ثلاثية الأبعاد: [الدفع العمودي (y)، الدفع الجانبي (z)، الدفع الأمامي (x)]
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(3,), dtype=np.float32)
        
        # 2. الملاحظات (11 بعداً): 
        # [x, y, z, vx, vy, vz, dist_top, dist_bottom, dist_left, dist_right, current_gravity]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(11,), dtype=np.float32)
        
        # أبعاد النفق ثلاثي الأبعاد
        self.cave_height = 10.0   # محور Y (الارتفاع)
        self.cave_width = 10.0    # محور Z (العرض الجانبي)
        self.cave_length = 100.0  # محور X (العمق/الأمام)
        
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # الحالة الابتدائية ثلاثية الأبعاد: [x, y, z, vx, vy, vz]
        # تبدأ الطائرة من المنتصف تماماً (y=5.0, z=5.0)
        self.state = np.array([0.0, 5.0, 5.0, 0.0, 0.0, 0.0], dtype=np.float32) 
        
        # توليد جاذبية أساسية متغيرة لكل شوط لمحاكاة الشذوذ الجاذبي
        self.current_gravity = np.random.uniform(7.0, 13.0)
        
        return self._get_obs(), {}

    def _get_obs(self):
        x, y, z, vx, vy, vz = self.state
        
        # حساب المسافات الفيزيائية للجدران الأربعة المحيطة
        dist_top = self.cave_height - y
        dist_bottom = y
        dist_left = z
        dist_right = self.cave_width - z
        
        return np.array([
            x, y, z, vx, vy, vz, 
            dist_top, dist_bottom, dist_left, dist_right, 
            self.current_gravity
        ], dtype=np.float32)

    def step(self, action):
        x, y, z, vx, vy, vz = self.state
        
        # تحجيم القوى الحركية لكل محور
        thrust_y = action[0] * 15.0
        thrust_z = action[1] * 5.0
        thrust_x = action[2] * 5.0 
        
        # 1. شذوذ الجاذبية الديناميكي المتغير مع التقدم في النفق
        gravity_effect = self.current_gravity + np.sin(x * 0.1) * 2.0
        
        # 2. تأثير السحب القريب من الجدران (Wall-Bounded Aerodynamic Drag) في 3D
        dist_bottom = max(y, 0.1)
        dist_top = max(self.cave_height - y, 0.1)
        dist_left = max(z, 0.1)
        dist_right = max(self.cave_width - z, 0.1)
        
        # قوى السحب العمودية والجانبية
        wall_pull_bottom = 0.5 / (dist_bottom ** 2)  
        wall_pull_top = 0.5 / (dist_top ** 2)        
        wall_pull_left = 0.5 / (dist_left ** 2)
        wall_pull_right = 0.5 / (dist_right ** 2)
        
        # صافي القوى الفيزيائية المؤثرة في الفضاء ثلاثي الأبعاد
        total_force_y = thrust_y - gravity_effect - wall_pull_bottom + wall_pull_top
        total_force_z = thrust_z - wall_pull_left + wall_pull_right
        total_force_x = thrust_x - (0.1 * vx)  # مقاومة الهواء الأمامية بسيطة
        
        # معادلات نيوتن للحركة وتحديث الفضاء الحركي 3D
        dt = 0.05
        vx += total_force_x * dt
        vy += total_force_y * dt
        vz += total_force_z * dt
        
        x += vx * dt
        y += vy * dt
        z += vz * dt
        
        self.state = np.array([x, y, z, vx, vy, vz], dtype=np.float32)
        
        # --- حساب المكافآت والعقوبات ثلاثية الأبعاد المطورة ---
        # 1. مكافأة للتقدم للأمام على محور X
        reward = vx * 0.5 
        
        # 2. عقوبة الاهتزازات العمودية والجانبية غير المستقرة
        reward -= 0.2 * (vy ** 2)
        reward -= 0.2 * (vz ** 2)
        
        # 3. هندسة الحفاظ على المركز ثلاثي الأبعاد (الابتعاد عن مركز النفق المتمثل في النقطة 5.0 و 5.0)
        distance_from_center_y = abs(y - 5.0)
        distance_from_center_z = abs(z - 5.0)
        reward -= 0.5 * (distance_from_center_y + distance_from_center_z)
        
        # 4. مكافأة البقاء على قيد الحياة
        reward += 0.1

        terminated = False
        truncated = False
        
        # شروط الاصطدام والنهاية في الـ 3D (الاصطدام بأي من الجدران الأربعة)
        if y <= 0.0 or y >= self.cave_height or z <= 0.0 or z >= self.cave_width:
            terminated = True
            reward = -200.0  # عقوبة اصطدام صارمة
        
        # شرط الفوز والوصول لنهاية النفق
        if x >= self.cave_length:
            terminated = True
            reward += 1000.0  
            
        return self._get_obs(), reward, terminated, truncated, {}