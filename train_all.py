"""
Smart Route - Complete Training & Output Generation
Trains PPO, DQN, A2C agents and generates all output files for submission.
"""
import os
import sys
import csv
import json
import time
import warnings
warnings.filterwarnings("ignore")

# Set SUMO_HOME
if "SUMO_HOME" not in os.environ:
    os.environ["SUMO_HOME"] = r"C:\Program Files (x86)\SUMO"

from sumo_rl import SumoEnvironment
from stable_baselines3 import PPO, DQN, A2C
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np

# ---- Configuration ----
NET_FILE = os.path.join("sumo_env", "cross_2lanes.net.xml")
ROUTE_FILE = os.path.join("sumo_env", "cross_2lanes.rou.xml")
TOTAL_TIMESTEPS = 50_000
NUM_SECONDS = 3600
DELTA_TIME = 5

os.makedirs("models", exist_ok=True)
os.makedirs("runs", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("outputs/plots", exist_ok=True)
os.makedirs("outputs/csv", exist_ok=True)
os.makedirs("outputs/logs", exist_ok=True)

# ---- Custom Callback to log episode rewards ----
class MetricsCallback(BaseCallback):
    def __init__(self, algo_name, verbose=0):
        super().__init__(verbose)
        self.algo_name = algo_name
        self.episode_rewards = []
        self.episode_lengths = []
        self.timestep_log = []
        self.current_ep_reward = 0
        self.current_ep_len = 0

    def _on_step(self) -> bool:
        reward = self.locals.get("rewards", [0])[0]
        self.current_ep_reward += reward
        self.current_ep_len += 1

        done = self.locals.get("dones", [False])[0]
        if done:
            self.episode_rewards.append(self.current_ep_reward)
            self.episode_lengths.append(self.current_ep_len)
            self.timestep_log.append({
                "timestep": self.num_timesteps,
                "episode": len(self.episode_rewards),
                "reward": self.current_ep_reward,
                "length": self.current_ep_len
            })
            print(f"  [{self.algo_name}] Episode {len(self.episode_rewards):>3d} | "
                  f"Reward: {self.current_ep_reward:>8.2f} | "
                  f"Length: {self.current_ep_len:>5d} | "
                  f"Timesteps: {self.num_timesteps:>7d}")
            self.current_ep_reward = 0
            self.current_ep_len = 0
        return True


def make_env():
    return SumoEnvironment(
        net_file=NET_FILE,
        route_file=ROUTE_FILE,
        use_gui=False,
        num_seconds=NUM_SECONDS,
        delta_time=DELTA_TIME,
        single_agent=True,
        sumo_warnings=False
    )


def train_algorithm(algo_class, algo_name, timesteps):
    """Train a single RL algorithm and return metrics."""
    print(f"\n{'='*60}")
    print(f"  Training {algo_name} for {timesteps} timesteps...")
    print(f"{'='*60}")

    env = DummyVecEnv([make_env])
    callback = MetricsCallback(algo_name)

    if algo_name == "DQN":
        model = algo_class(
            "MlpPolicy", env, verbose=0,
            tensorboard_log="runs",
            learning_starts=1000,
            buffer_size=50000
        )
    else:
        model = algo_class(
            "MlpPolicy", env, verbose=0,
            tensorboard_log="runs"
        )

    start_time = time.time()
    model.learn(total_timesteps=timesteps, callback=callback)
    training_time = time.time() - start_time

    # Save model
    model_path = f"models/{algo_name.lower()}_cross"
    model.save(model_path)
    print(f"  Model saved to {model_path}.zip")
    print(f"  Training time: {training_time:.1f}s")

    env.close()
    return callback, model, training_time


def evaluate_model(model, algo_name, num_episodes=5):
    """Evaluate a trained model and return per-episode metrics."""
    print(f"\n  Evaluating {algo_name} over {num_episodes} episodes...")
    results = []

    for ep in range(num_episodes):
        env = SumoEnvironment(
            net_file=NET_FILE,
            route_file=ROUTE_FILE,
            use_gui=False,
            num_seconds=NUM_SECONDS,
            delta_time=DELTA_TIME,
            single_agent=True,
            sumo_warnings=False
        )
        obs, info = env.reset()
        total_reward = 0
        steps = 0
        done = False

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated

        results.append({
            "episode": ep + 1,
            "total_reward": total_reward,
            "steps": steps,
            "avg_reward_per_step": total_reward / max(steps, 1)
        })
        print(f"    Episode {ep+1}: Reward={total_reward:.2f}, Steps={steps}")
        env.close()

    return results


def save_csv(data, filename, fieldnames):
    """Save a list of dicts to CSV."""
    filepath = os.path.join("outputs", "csv", filename)
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"  Saved: {filepath}")


def main():
    print("=" * 60)
    print("  SMART ROUTE - FULL TRAINING PIPELINE")
    print("  AI-Powered Traffic Signal Optimization System")
    print("=" * 60)

    all_callbacks = {}
    all_models = {}
    all_eval_results = {}
    training_times = {}

    # ---- Train all 3 algorithms ----
    for algo_class, algo_name in [(PPO, "PPO"), (DQN, "DQN"), (A2C, "A2C")]:
        cb, model, t_time = train_algorithm(algo_class, algo_name, TOTAL_TIMESTEPS)
        all_callbacks[algo_name] = cb
        all_models[algo_name] = model
        training_times[algo_name] = t_time

    # ---- Evaluate all models ----
    for algo_name, model in all_models.items():
        all_eval_results[algo_name] = evaluate_model(model, algo_name, num_episodes=5)

    # ---- Save Training Logs CSV ----
    for algo_name, cb in all_callbacks.items():
        if cb.timestep_log:
            save_csv(
                cb.timestep_log,
                f"training_log_{algo_name.lower()}.csv",
                ["timestep", "episode", "reward", "length"]
            )

    # ---- Save Evaluation Results CSV ----
    eval_rows = []
    for algo_name, results in all_eval_results.items():
        for r in results:
            eval_rows.append({"algorithm": algo_name, **r})
    save_csv(eval_rows, "evaluation_results.csv",
             ["algorithm", "episode", "total_reward", "steps", "avg_reward_per_step"])

    # ---- Save Comparison Summary CSV ----
    comparison = []
    for algo_name in ["PPO", "DQN", "A2C"]:
        cb = all_callbacks[algo_name]
        evals = all_eval_results[algo_name]
        avg_eval_reward = np.mean([e["total_reward"] for e in evals])
        std_eval_reward = np.std([e["total_reward"] for e in evals])
        avg_train_reward = np.mean(cb.episode_rewards) if cb.episode_rewards else 0
        comparison.append({
            "algorithm": algo_name,
            "training_episodes": len(cb.episode_rewards),
            "training_timesteps": TOTAL_TIMESTEPS,
            "training_time_sec": round(training_times[algo_name], 1),
            "avg_training_reward": round(avg_train_reward, 2),
            "avg_eval_reward": round(avg_eval_reward, 2),
            "std_eval_reward": round(std_eval_reward, 2),
            "best_eval_reward": round(max(e["total_reward"] for e in evals), 2),
            "worst_eval_reward": round(min(e["total_reward"] for e in evals), 2)
        })
    save_csv(comparison, "algorithm_comparison.csv",
             ["algorithm", "training_episodes", "training_timesteps",
              "training_time_sec", "avg_training_reward", "avg_eval_reward",
              "std_eval_reward", "best_eval_reward", "worst_eval_reward"])

    # ---- Save JSON summary ----
    summary = {
        "project": "Smart Route - AI-Powered Traffic Signal Optimization",
        "simulation": {
            "simulator": "SUMO 1.28.0",
            "network": "cross_2lanes (4-way intersection, 2 lanes per direction)",
            "duration_seconds": NUM_SECONDS,
            "delta_time": DELTA_TIME,
            "vehicles": "1200 mixed vehicles"
        },
        "training": {
            "total_timesteps": TOTAL_TIMESTEPS,
            "algorithms": comparison
        },
        "files_generated": [
            "models/ppo_cross.zip",
            "models/dqn_cross.zip",
            "models/a2c_cross.zip",
            "outputs/csv/training_log_ppo.csv",
            "outputs/csv/training_log_dqn.csv",
            "outputs/csv/training_log_a2c.csv",
            "outputs/csv/evaluation_results.csv",
            "outputs/csv/algorithm_comparison.csv",
            "outputs/training_summary.json",
            "runs/ (TensorBoard logs)"
        ]
    }
    with open("outputs/training_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved: outputs/training_summary.json")

    # ---- Print Final Summary ----
    print("\n" + "=" * 60)
    print("  TRAINING & EVALUATION COMPLETE")
    print("=" * 60)
    print(f"\n  {'Algorithm':<10} {'Train Time':<12} {'Avg Eval Reward':<18} {'Episodes'}")
    print(f"  {'-'*55}")
    for c in comparison:
        print(f"  {c['algorithm']:<10} {c['training_time_sec']:>8.1f}s   {c['avg_eval_reward']:>14.2f}   {c['training_episodes']:>8d}")
    print(f"\n  All output files saved in: outputs/")
    print(f"  All models saved in: models/")
    print(f"  TensorBoard logs in: runs/")
    print("=" * 60)


if __name__ == "__main__":
    main()
