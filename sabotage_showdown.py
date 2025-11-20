# sabotage_showdown.py – ПЕРФЕКТНА ВЕРСИЯ (червеното се вижда идеално)
import torch
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from gravopt import GravOptAdaptiveE_QV

shared_param = torch.nn.Parameter(torch.tensor([0.15]))
grav_opt = GravOptAdaptiveE_QV([shared_param], lr=0.035)

def loss_fn(p):
    θ = p[0]
    return 0.5 * (1 - torch.cos(θ)) + 0.35 * torch.sin(2*θ)**2 + 0.1 * torch.cos(3*θ)

exact_energy = -0.85

energies = []
sabotage_level = []          # само текущата сила, не се натрупва!

fig, ax = plt.subplots(figsize=(13, 8))
line_energy, = ax.plot([], [], '#00ff41', linewidth=6, label='Energy under attack')
line_sabotage, = ax.plot([], [], 'red', linewidth=5, alpha=0.8, label='Sabotage attack 😈')
ax.axhline(y=exact_energy, color='white', linestyle='--', linewidth=3, label='Exact ground state')
ax.set_xlim(0, 130)
ax.set_ylim(-1.2, 1.8)        # перфектни лимити
ax.set_title('⚔️ GRAVOPT UNDER ATTACK ⚔️\nAnti-GravOpt sabotages in real time!', 
             fontsize=22, fontweight='bold', color='white', backgroundcolor='#000000', pad=20)
ax.set_xlabel('Step', fontsize=14, color='white')
ax.set_ylabel('Energy', fontsize=14, color='white')
ax.legend(fontsize=14, loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')
ax.grid(True, alpha=0.3, color='gray')
ax.set_facecolor('#0e0e0e')
fig.set_facecolor('#000000')
ax.tick_params(colors='white')

def animate(frame):
    # GravOpt стъпка
    shared_param.grad = None
    loss = loss_fn(shared_param)
    loss.backward()
    grav_opt.step()
    energies.append(loss.item())

    # САБОТАЖ!
    current_sabotage = 0.0
    if frame % 3 == 0 or frame % 5 == 0:
        noise = torch.randn_like(shared_param.data) * (0.07 + 0.0007*frame)
        pull = torch.tensor([0.12 + 0.0012*frame])
        shared_param.data.add_(noise + pull)
        current_sabotage = pull.item() + noise.abs().item()

    sabotage_level.append(current_sabotage)   # само текущата атака

    # Update
    x = list(range(len(energies)))
    line_energy.set_data(x, energies)
    line_sabotage.set_data(x, sabotage_level)
    return line_energy, line_sabotage

print("Starting the perfect sabotage battle…")
ani = FuncAnimation(fig, animate, frames=130, interval=180, repeat=False)
ani.save('gravopt_under_attack.gif', writer='pillow', fps=9)
print("DONE! gravopt_under_attack.gif – red line is perfect now 😈")