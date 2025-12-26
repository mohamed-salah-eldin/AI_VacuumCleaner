import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

MAX_STEPS = 200 

class VacuumEnvironment:
    """Grid environment with dirt"""
    def __init__(self, size=8, dirt_probability=0.3):
        self.size = size
        self.grid = np.random.choice([0, 1], size=(size, size), 
                                     p=[1-dirt_probability, dirt_probability])
        self.initial_dirt = np.sum(self.grid)
        
    def is_dirty(self, x, y):
        return self.grid[y, x] == 1
    
    def clean(self, x, y):
        if self.grid[y, x] == 1:
            self.grid[y, x] = 0
            return True
        return False
    
    def get_total_dirt(self):
        return np.sum(self.grid)

class SimpleReflexAgent:
    """Simple reflex agent - reacts only to current perception"""
    def __init__(self, env):
        self.env = env
        self.x = 0
        self.y = 0
        self.moves = 0
        self.cleaned = 0
        
    def perceive(self):
        return self.env.is_dirty(self.x, self.y)
    
    def act(self):
        if self.moves >= MAX_STEPS:
            return None
        self.moves += 1
        
        if self.perceive():
            if self.env.clean(self.x, self.y):
                self.cleaned += 1
            return 'CLEAN'
        
        possible_moves = []
        if self.x < self.env.size - 1: possible_moves.append(('RIGHT', self.x + 1, self.y))
        if self.x > 0:                 possible_moves.append(('LEFT', self.x - 1, self.y))
        if self.y < self.env.size - 1: possible_moves.append(('DOWN', self.x, self.y + 1))
        if self.y > 0:                 possible_moves.append(('UP', self.x, self.y - 1))
        
        direction, new_x, new_y = random.choice(possible_moves)
        self.x, self.y = new_x, new_y
        return direction
    
    def get_stats(self):
        return {
            'type': 'Simple Reflex',
            'moves': self.moves,
            'cleaned': self.cleaned,
            'efficiency': self.cleaned / self.moves if self.moves > 0 else 0
        }

class ModelBasedAgent:
    """Model-based agent - maintains internal map of environment"""
    def __init__(self, env):
        self.env = env
        self.x = 0
        self.y = 0
        self.moves = 0
        self.cleaned = 0
        self.memory = np.full((env.size, env.size), -1) 
        self.memory[0, 0] = 0
        
    def perceive(self):
        is_dirty = self.env.is_dirty(self.x, self.y)
        self.memory[self.y, self.x] = 1 if is_dirty else 0
        return is_dirty
    
    def act(self):
        if self.moves >= MAX_STEPS:
            return None
        self.moves += 1
        
        if self.perceive():
            if self.env.clean(self.x, self.y):
                self.cleaned += 1
                self.memory[self.y, self.x] = 0
            return 'CLEAN'
        
        possible_moves = []
        if self.x < self.env.size - 1: possible_moves.append(('RIGHT', self.x + 1, self.y))
        if self.x > 0:                 possible_moves.append(('LEFT', self.x - 1, self.y))
        if self.y < self.env.size - 1: possible_moves.append(('DOWN', self.x, self.y + 1))
        if self.y > 0:                 possible_moves.append(('UP', self.x, self.y - 1))
        
        unvisited = [(d, x, y) for d, x, y in possible_moves 
                     if self.memory[y, x] == -1]
        
        if unvisited:
            direction, new_x, new_y = random.choice(unvisited)
        else:
            direction, new_x, new_y = random.choice(possible_moves)
        
        self.x, self.y = new_x, new_y
        return direction
    
    def get_stats(self):
        return {
            'type': 'Model-Based',
            'moves': self.moves,
            'cleaned': self.cleaned,
            'efficiency': self.cleaned / self.moves if self.moves > 0 else 0
        }

def run_simulation(agent_class, max_steps):
    """Run simulation and return agent stats"""
    env = VacuumEnvironment(size=8, dirt_probability=0.3)
    agent = agent_class(env)
    
    steps = 0
    while steps < max_steps:
        if env.get_total_dirt() == 0:
            break
        agent.act()
        steps += 1

    return agent.get_stats(), env.initial_dirt

def visualize_agent(agent_class, agent_name, max_steps):
    """Visualize agent performance with animation"""
    env = VacuumEnvironment(size=8, dirt_probability=0.3)
    agent = agent_class(env)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    im = ax1.imshow(env.grid, cmap='YlOrBr', vmin=0, vmax=1)
    agent_marker = ax1.plot(agent.x, agent.y, 'bo', markersize=20, 
                           markeredgecolor='darkblue', markeredgewidth=2)[0]
    ax1.set_title(f'{agent_name} Agent', fontsize=14, fontweight='bold')
    ax1.set_xticks(range(env.size))
    ax1.set_yticks(range(env.size))
    ax1.grid(True, alpha=0.3)
    
    stats_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes,
                         verticalalignment='top', fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Steps', fontsize=12)
    ax2.set_ylabel('Metrics', fontsize=12)
    ax2.set_title('Performance Metrics', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    steps_list = []
    efficiency_list = []
    dirt_list = []
    
    eff_line, = ax2.plot([], [], 'b-', label='Efficiency', linewidth=2)
    dirt_line, = ax2.plot([], [], 'r-', label='Dirt Remaining', linewidth=2)
    ax2.legend(loc='upper right')
    
    def animate(frame):
        if frame >= max_steps or env.get_total_dirt() == 0:
            return im, agent_marker, stats_text, eff_line, dirt_line
        
        agent.act()
        
        im.set_data(env.grid)
        agent_marker.set_data([agent.x], [agent.y])
        
        stats = agent.get_stats()
        stats_text.set_text(
            f"Moves: {stats['moves']}\n"
            f"Cleaned: {stats['cleaned']}/{env.initial_dirt}\n"
            f"Efficiency: {stats['efficiency']:.2%}\n"
            f"Dirt Left: {env.get_total_dirt()}"
        )
        
        steps_list.append(frame)
        efficiency_list.append(stats['efficiency'])
        dirt_list.append(env.get_total_dirt() / env.initial_dirt)
        
        eff_line.set_data(steps_list, efficiency_list)
        dirt_line.set_data(steps_list, dirt_list)
        
        if frame > 90:
            ax2.set_xlim(0, frame + 20)
        
        return im, agent_marker, stats_text, eff_line, dirt_line
    
    anim = FuncAnimation(fig, animate, frames=max_steps, interval=10, blit=True, repeat=False)
    plt.tight_layout()
    plt.show()

def compare_agents(num_trials=20):
    """Generates ONLY the Average Performance Comparison bar chart."""
    print(f"Running comparison with {num_trials} trials...")
    reflex_stats = []
    model_stats = []
    
    for _ in range(num_trials):
        reflex, dirt = run_simulation(SimpleReflexAgent, MAX_STEPS)
        model, _ = run_simulation(ModelBasedAgent, MAX_STEPS)
        reflex_stats.append(reflex)
        model_stats.append(model)
    
    reflex_moves = [s['moves'] for s in reflex_stats]
    model_moves = [s['moves'] for s in model_stats]
    reflex_eff = [s['efficiency'] for s in reflex_stats]
    model_eff = [s['efficiency'] for s in model_stats]
    
    avg_reflex_moves = np.mean(reflex_moves)
    avg_model_moves = np.mean(model_moves)
    avg_reflex_eff = np.mean(reflex_eff)
    avg_model_eff = np.mean(model_eff)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x = np.arange(2)
    width = 0.35
    
    ax.bar(x - width/2, [avg_reflex_moves, avg_model_moves], 
           width, label='Avg Moves', color='skyblue')
    ax.set_ylabel('Avg Moves', color='skyblue', fontweight='bold', fontsize=12)
    ax.tick_params(axis='y', labelcolor='skyblue')
    
    ax_twin = ax.twinx()
    ax_twin.bar(x + width/2, [avg_reflex_eff * 100, avg_model_eff * 100], 
                width, label='Avg Efficiency (%)', color='orange', alpha=0.7)
    ax_twin.set_ylabel('Avg Efficiency (%)', color='orange', fontweight='bold', fontsize=12)
    ax_twin.tick_params(axis='y', labelcolor='orange')
    
    ax.set_xticks(x)
    ax.set_xticklabels(['Reflex', 'Model-Based'], fontsize=10)
    ax.set_title('Average Performance Comparison', fontsize=14, fontweight='bold')
    
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_twin.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, 1.15))
    ax.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*60)
    print("NUMBERS USED FOR THE BAR CHART")
    print("="*60)
    print(f"Simple Reflex Agent: Avg Moves = {avg_reflex_moves:.1f}, Avg Efficiency = {avg_reflex_eff:.2%}")
    print(f"Model-Based Agent: Avg Moves = {avg_model_moves:.1f}, Avg Efficiency = {avg_model_eff:.2%}")
    print("="*60)

if __name__ == "__main__":
    print("Vacuum Cleaner Agent Simulator")
    print("="*60)
    
    print("\n1. Visualizing Simple Reflex Agent...")
    visualize_agent(SimpleReflexAgent, "Simple Reflex", MAX_STEPS)
    
    print("\n2. Visualizing Model-Based Agent...")
    visualize_agent(ModelBasedAgent, "Model-Based", MAX_STEPS)
    
    print("\n3. Comparing Agent Performance...")
    compare_agents(num_trials=20)