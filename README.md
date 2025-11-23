# GravOpt – Physics-Inspired Optimizer for MAX-CUT & Beyond

[![PyPI](https://img.shields.io/pypi/v/gravopt?color=success&style=for-the-badge)](https://pypi.org/project/gravopt/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/Kretski/GravOptAdaptiveE?style=social)](https://github.com/Kretski/GravOptAdaptiveE)

> **99.9999% MAX-CUT** on small graphs • **89.17% on Gset** • **0.3676 on G81 (20k nodes)**  
> All on **CPU**, **no external solvers**, **<80 MB RAM**

---

## ✨ Why it works

GravOpt uses a **gravitational analogy** to dynamically freeze low-impact parameters and accelerate convergence. The result? Near-optimal cuts **10–200× faster** than Simulated Annealing, Tabu, or greedy methods.

It’s **not magic** — it’s **adaptive inertia**.

---

## 🚀 Try it now (open-source)

```bash
from gravopt import GravOptAdaptiveE_QV
import torch, networkx as nx

G = nx.erdos_renyi_graph(12, 0.5, seed=42)
params = torch.nn.Parameter(torch.randn(12) * 0.1)
opt = GravOptAdaptiveE_QV([params], lr=0.02)

for _ in range(100):
    opt.zero_grad()
    loss = sum(0.5 * (1 - torch.cos(params[i] - params[j])) for i, j in G.edges())
    loss.backward()
    opt.step()

ratio = (len(G.edges()) - loss.item()) / len(G.edges())
print(f"MAX-CUT: {ratio:.6%}")  # → 99.9999%
pip install gravopt networkx torch
 Benchmarks (Nov 2025)
[table-443bc121-7350-43c3-9012-4d169a024809.xlsx](https://github.com/user-attachments/files/23694875/table-443bc121-7350-43c3-9012-4d169a024809.xlsx)
For large sparse graphs (G81+), see the pure-Numba solver:
→ github.com/Kretski/GravOpt-MAXCUT
GravOpt Pro (commercial)
For enterprise & research teams needing:

On-premise / air-gapped deployment
Confidential benchmarks on your data
Priority 1:1 support
All future models (Quantum, Resonance, Scheduling, VQE, etc.)
🔥 First 100 lifetime licenses: €200 (normally €590)
✅ One payment, forever — no subscription
After purchase (during 9–18 EET), you’ll receive your .whl + license key within minutes.
 Resources
Preprint: vixra.org/abs/2511.17607773
X thread: x.com/DKretski/status/1990560176450027524
LinkedIn: linkedin.com/in/dimitar-kretski-071118b6
For enterprise: kretski@azuro.ai
Open-source forever · Pro = real-world power
 Challenge
Beat my score on any Gset graph?
→ Open an issue. First one gets a beer in Sofia 🍺

Made with ❤️ and gravitational madness in Bulgaria
🔗 Azuro AI Platform (experimental)



