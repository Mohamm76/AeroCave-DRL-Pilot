```markdown
# AeroCave-DRL-Pilot: Autonomous Drone Navigation in Turbulent Caverns 🚀

An end-to-end Deep Reinforcement Learning (DRL) framework developed using **Stable-Baselines3** and **Gymnasium** to train an autonomous drone to navigate through narrow, turbulent subterranean environments. 

The environment simulates complex atmospheric and physical anomalies, including **variable dynamic gravity** and **wall-bounded aerodynamic drag**.

---

## 🛠️ System Architecture & Physics Simulation

The drone operates within a custom continuous action space and experiences real-time physical perturbations:

*   **Action Space:** Continuous inputs controlling vertical thrust and horizontal acceleration: $\mathcal{A} \in [-1, 1]^2$.
*   **Observation Space:** A 7-dimensional telemetry vector: $[x, y, v_x, v_y, \text{dist}_{\text{top}}, \text{dist}_{\text{bottom}}, g_{\text{current}}]$.
*   **Dynamic Anomalies:** Local gravity behaves fluidly via $g_{\text{eff}} = g_{\text{base}} + \sin(0.1x) \cdot 2$.
*   **Wall Drag Effect:** Proximity to boundaries induces exponential aerodynamic pull modeled by:
    $$\text{Force}_{\text{drag}} = \frac{0.5}{d^2}$$

---

## 🚀 Getting Started

### 1. Installation & Environment Setup
Clone the repository and install the verified dependencies inside your virtual environment:

```bash
git clone [https://github.com/YOUR_USERNAME/AeroCave-DRL-Pilot.git](https://github.com/YOUR_USERNAME/AeroCave-DRL-Pilot.git)
cd AeroCave-DRL-Pilot
pip install -r requirements.txt

```

### 2. Training the PPO Agent

To train the neural network policy under the advanced shaped reward function, execute:

```bash
python agents/train_agent.py

```

### 3. Evaluation & Visualization

To run a deterministic evaluation loop and plot the flight path against the cavern boundaries:

```bash
python evaluate_agent.py

```

---

## 📊 Performance & Optimization Results

Through rigorous reward reshaping, the agent successfully eliminated **Reward Hacking** behaviors (high-speed ceiling collisions) by incorporating a strict center-line tracking penalty.

* **Algorithm:** Proximal Policy Optimization (PPO)
* **Policy Network:** Multi-Layer Perceptron (MlpPolicy)
* **Success Rate:** 100% stable transit across a 100-meter cavern obstacle course.
* **Mean Episode Reward:** ~ $+1,920$

```
