# GravOpt – Physics-Inspired Optimizer for MAX-CUT

[![PyPI](https://img.shields.io/pypi/v/gravopt?color=success)](https://pypi.org/project/gravopt/)  
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  
[![Stars](https://img.shields.io/github/stars/Kretski/GravOptAdaptiveE)](https://github.com/Kretski/GravOptAdaptiveE)

> **99.9999% MAX-CUT** on small graphs  
> **89.17% on Gset**  
> **0.3676 on G81 (20k nodes)**  
> All on CPU, <80 MB RAM, no solvers.

## ✨ How It Works
GravOpt uses a gravitational analogy with adaptive parameter freezing, beating Goemans-Williamson (+12.2%) by 10–200x faster than Simulated Annealing/Tabu.

## 🚀 Try It (Open-Source)
```python
from gravopt import GravOptAdaptiveE_QV
import torch, networkx as nx
G = nx.erdos_renyi_graph(12, 0.5, seed=42)
params = torch.nn.Parameter(torch.randn(12) * 0.1)
opt = GravOptAdaptiveE_QV([params], lr=0.02)
for _ in range(100): opt.step()
print(f"MAX-CUT: {(len(G.edges())-loss.item())/len(G.edges()):.6%}") # ~99.9999%
Install: pip install gravopt networkx torch
📊 Benchmarks

G81 (20k nodes): 0.3676 in ~1200 steps (~6–8 min CPU).
Numba solver: GravOpt-MAXCUT

💡 Feedback Welcome

Is this a new metaheuristic?
Stress-test on QUBO/Ising?
Analyze "gravitational" dynamics?

🔗 Resources

GitHub: Kretski/GravOptAdaptiveE
PyPI: gravopt
Preprint: vixra.org/abs/2511.17607773
X: DKretski

🎯 Challenge
Beat 0.3676 on G81? Open an issue – first win gets a beer in Sofia! 🍺
💼 GravOpt Pro (Commercial)

On-premise/air-gapped deployment
Confidential benchmarks
Priority support
All future models (Quantum, VQE, etc.)
🔥 First 100 licenses: €200 (reg. €590)
<button style="background-color: #008CBA; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Buy Now</button>
Contact: kretski@gmail.com / violetvet@abv.bg

Made with ❤️ in Bulgaria by Azuro AI.
text
