# anti_gravopt.py
import torch
import random

class AntiGravOptAdaptiveE_QV(torch.optim.Optimizer):
    """Най-лошият оптимизатор на света – нарочно всичко наобратно"""
    def __init__(self, params, lr=0.07):
        defaults = dict(lr=lr)
        super().__init__(params, defaults)

    def step(self):
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad.data

                state = self.state[p]
                if len(state) == 0:
                    state['step'] = 0
                    state['h'] = torch.tensor(1.5)   # стартира с МАКСИМАЛНО h
                    state['M'] = torch.tensor(0.4)   # пълен хаос от начало

                state['step'] += 1

                # ANTI-ПРАВИЛАТА
                fake_grad = grad  # плюс вместо минус
                state['h'] = state['h'] * 1.12  # h расте с времето
                noise = torch.randn_like(p.data) * 0.15

                if random.random() > 0.7:
                    update = group['lr'] * state['h'] * state['M'] * (-fake_grad + noise)
                else:
                    update = group['lr'] * state['h'] * state['M'] * fake_grad + noise

                p.data.add_(update)  # без минус!