````markdown
# AeroCave-DRL-Pilot: Autonomous Drone Navigation in Turbulent Caverns 🚀

An end-to-end Deep Reinforcement Learning (DRL) framework developed using **Stable-Baselines3** and **Gym** to train autonomous drone agents in continuous control navigation tasks. The framework features a custom-engineered 3D physics cave environment built to simulate dynamic atmospheric anomalies and complex aerodynamic boundary limitations.

---

## 🔬 System Architecture & Physics Simulation

The drone operates within a continuous action space and experiences real-time physical perturbations within highly restrictive cavern profiles.

- **Action Space ($A$):** Continuous inputs controlling continuous vertical thrust and multi-axis horizontal accelerations: $\mathcal{A} \in [-1, 1]^3$.
- **Observation Space ($S$):** A 7-dimensional telemetry vector mapping spatial tracking:
  $$S = [x, y, v_x, v_y, d_{\text{wall}}, d_{\text{top}}, d_{\text{base}}]$$
- **Dynamic Anomalies:** Local gravity is modeled fluidly to simulate cave wind shears via:
  $$g_{\text{eff}} = g_{\text{base}} + \sin(0.5t) \cdot \cos(v_y)$$
- **Wall Drag Effect:** Proximity to cavern boundaries induces exponential aerodynamic pull modeled by:
  $$F_{\text{drag}} = \alpha \cdot e^{-\beta \cdot d_{\text{wall}}}$$

---

## 📊 Reward Function Design

To enforce safe navigation and optimal velocity convergence, the agent is trained under a multi-objective reward formulation:

$$R_t = w_1 \cdot R_{\text{progress}} - w_2 \cdot P_{\text{proximity}} - w_3 \cdot P_{\text{collision}}$$

| Component             | Target Objective                             | Mathematical Formulation                                                      |
| :-------------------- | :------------------------------------------- | :---------------------------------------------------------------------------- |
| **Progress Reward**   | Maximize forward velocity along the track    | $R_{\text{progress}} = v_x \cdot \cos(\theta)$                                |
| **Proximity Penalty** | Discourage flying close to cavern walls      | $P_{\text{proximity}} = \exp(- \gamma \cdot d_{\text{wall}})$                 |
| **Collision Penalty** | Strict terminal penalty upon boundary impact | $P_{\text{collision}} = -100 \quad (\text{if } d_{\text{wall}} \le \epsilon)$ |

---

## 💻 Project Structure

```bash
├── evaluate_agent.py        # Evaluation pipeline for trained DRL policies
├── test_env.py             # Sandbox for verifying physical constraints
├── ppo_cave_pilot_final.zip # Serialized trained PPO model weights
├── requirements.txt         # Managed dependencies list
└── README.md                # System documentation
```
````

---

## ⚡ Quick Start & Evaluation

1. **Clone the repository:**

```bash
git clone [https://github.com/Mohamm76/AeroCave-DRL-Pilot.git](https://github.com/Mohamm76/AeroCave-DRL-Pilot.git)
cd AeroCave-DRL-Pilot

```

2. **Install dependencies:**

```bash
pip install -r requirements.txt

```

3. **Run the evaluation script:**

```bash
python evaluate_agent.py

```
