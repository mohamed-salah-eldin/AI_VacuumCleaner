Vacuum Cleaner Agent Simulator

Simple Reflex vs Model-Based Agent

A Python simulation that compares two classical AI agent architectures operating in the same grid environment.
The project focuses on decision logic, memory, and performance comparison rather than robotics.

Project Overview

The simulator models an 8×8 environment where cells may contain dirt.
An agent starts at position (0,0) and repeatedly decides whether to clean the current cell or move.

Two different agents are implemented and evaluated under identical conditions.

The project includes:

• Environment simulation
• Agent behavior logic
• Step-by-step animation
• Quantitative performance comparison

Environment Design

The environment is represented as a grid.

• Each cell is either clean or dirty
• Dirt is randomly generated using a probability value
• The simulation ends when all dirt is cleaned or a step limit is reached

Key environment features:

• Grid size control
• Dirt density control
• Real-time dirt tracking

Implemented Agents
1. Simple Reflex Agent

This agent reacts only to what it senses at the current position.

Behavior:

• If the current cell is dirty → clean
• Otherwise → move randomly
• No memory of past states

Characteristics:

• Stateless
• Rule-based
• Fast decisions

Limitations:

• Repeats visits
• Wastes moves
• No awareness of explored areas

2. Model-Based Agent

This agent maintains an internal representation of the environment.

Behavior:

• Updates a memory grid for visited cells
• Prefers unvisited locations
• Falls back to random movement when needed

Characteristics:

• Stateful
• Context aware
• More structured exploration

Advantages:

• Fewer redundant moves
• Higher efficiency
• Better space coverage

Simulation and Visualization

The project provides real-time visualization using Matplotlib.

Displayed elements:

• Grid state
• Agent position
• Cleaning progress
• Efficiency over time
• Remaining dirt ratio

Each agent is visualized independently to allow direct observation of behavioral differences.

Performance Comparison

Multiple simulation runs are executed to reduce randomness.

Metrics measured:

• Total moves
• Cells cleaned
• Cleaning efficiency

Results are summarized using a comparison bar chart that shows:

• Average moves per agent
• Average efficiency per agent

This allows objective evaluation rather than visual judgment alone.

What This Project Taught Me

Working on this project clarified the impact of memory and state tracking on decision quality.

While studying cybersecurity and SOC analysis, this helped me understand why:

• Stateless rules are simple but noisy
• Context reduces unnecessary actions
• History improves decision confidence

Even though this is an AI simulation, the same thinking applies when analyzing sequences of events instead of isolated signals.

It improved how I reason about:

• Repeated events
• Pattern formation
• Efficiency vs simplicity

How to Run

Requirements:

• Python 3
• NumPy
• Matplotlib

Run:

python AI_Project.py


The script will:

Visualize the Simple Reflex Agent

Visualize the Model-Based Agent

Display a performance comparison

Key Takeaway

Adding memory changes behavior more than adding rules.

That insight applies far beyond this project.
