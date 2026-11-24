import os
import sys
import time

# Ensure SUMO_HOME is set
if "SUMO_HOME" not in os.environ:
    os.environ["SUMO_HOME"] = r"C:\Program Files (x86)\SUMO"

from sumo_rl import SumoEnvironment
from stable_baselines3 import PPO

NET_FILE = os.path.join("sumo_env", "cross_2lanes.net.xml")
ROUTE_FILE = os.path.join("sumo_env", "cross_2lanes.rou.xml")
MODEL_PATH = os.path.join("models", "ppo_cross")

def run_simulation():
    print("=" * 60)
    print("Smart Route - RL Simulation Viewer")
    print("=" * 60)

    # 1. Start simulation environment
    env = SumoEnvironment(
        net_file=NET_FILE,
        route_file=ROUTE_FILE,
        use_gui=True,
        num_seconds=1800,
        delta_time=5,
        single_agent=True
    )

    if os.path.exists(MODEL_PATH + ".zip"):
        print(f"Loaded trained model: {MODEL_PATH}.zip")
        model = PPO.load(MODEL_PATH, env=env)
    else:
        model = PPO("MlpPolicy", env, verbose=1)

    obs, info = env.reset()
    done = False
    step_num = 0

    print("\nSimulation is RUNNING! Watch the SUMO window.")
    print("Auto-pacing enabled: 0.15s per step so you can easily observe the cars.")

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        step_num += 1

        # Pause 150ms per decision step so it doesn't instantly finish
        time.sleep(0.15)

        if step_num % 10 == 0:
            print(f"Step {step_num} | Current Reward: {reward:.2f} | Info: {info}")

    print("\nSimulation finished!")
    env.close()

if __name__ == "__main__":
    run_simulation()
