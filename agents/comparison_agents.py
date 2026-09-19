import numpy as np

class DummySACAgent:
    """وكيل وهمي/مستقبلي لخوارزمية SAC لضمان عمل Factory Pattern في الـ Backend"""
    def predict(self, observation, deterministic=True):
        # يرجع أفعال عشوائية آمنة في نطاق المساحة المستمرة [-1, 1]
        action = np.array([0.1, 0.0, 0.5], dtype=np.float32)
        return action, None

class DummyDQNAgent:
    """وكيل وهمي/مستقبلي لخوارزمية DQN لضمان عمل Factory Pattern في الـ Backend"""
    def predict(self, observation, deterministic=True):
        # يرجع أفعال موجهة للأمام
        action = np.array([0.0, 0.0, 0.8], dtype=np.float32)
        return action, None