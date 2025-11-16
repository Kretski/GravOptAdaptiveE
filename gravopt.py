import torch
from torch.optim import Optimizer

class GravOptAdaptiveE_QV(Optimizer):
    def __init__(self, params, lr=0.02, alpha=0.05, c=0.8, M_max=1.8,
                 beta=0.01, freeze_percentile=25, unfreeze_gain=1.0,
                 momentum=0.9, h_decay=0.95, warmup_steps=20, update_every=1):
        if isinstance(params, torch.Tensor):
            params = [params]
        defaults = dict(lr=lr, alpha=alpha, c=c, M_max=M_max, beta=beta,
                        freeze_percentile=freeze_percentile, unfreeze_gain=unfreeze_gain,
                        momentum=momentum, h_decay=h_decay, warmup_steps=warmup_steps,
                        update_every=update_every)
        super().__init__(params, defaults)
        self.global_step = 0
        self._step_calls = 0
        self.quantum_calls = 0

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            loss = closure()

        self.global_step += 1
        self._step_calls += 1

        do_update = True
        for group in self.param_groups:
            update_every = group.get('update_every', 1)
            do_update = (self._step_calls % update_every) == 0
            break

        all_grads = []
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is not None:
                    g = p.grad
                    if torch.is_complex(g):
                        g = g.real
                    all_grads.append(g.detach().abs().flatten())
        if len(all_grads) == 0:
            return loss
        all_grads = torch.cat(all_grads)
        median_grad = torch.median(all_grads).item()

        for group in self.param_groups:
            lr = group['lr']
            alpha = group['alpha']
            c = group['c']
            M_max = group['M_max']
            beta = group['beta']
            unfreeze_gain = group['unfreeze_gain']
            momentum = group['momentum']
            h_decay = group['h_decay']
            warmup_steps = group['warmup_steps']
            freeze_percentile = group['freeze_percentile']

            adaptive_thr = 0.0 if self.global_step <= warmup_steps else max(median_grad * (freeze_percentile / 100.0), 1e-12)
            alpha_t = alpha / (1 + beta * self.global_step)

            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad.real if torch.is_complex(p.grad) else p.grad
                st = self.state[p]
                if 'exp_avg' not in st:
                    st['exp_avg'] = torch.zeros_like(p, memory_format=torch.preserve_format)
                    st['h'] = torch.ones_like(p, memory_format=torch.preserve_format) * 2.0
                    st['last_update'] = torch.full_like(p, self.global_step, dtype=torch.long)

                exp_avg = st['exp_avg']
                exp_avg.mul_(momentum).add_(grad, alpha=1.0 - momentum)
                grad_abs = grad.abs()
                h = st['h'] * h_decay

                if self.global_step > warmup_steps:
                    freeze_mask = grad_abs < adaptive_thr
                    h = torch.where(freeze_mask, torch.clamp(h - 0.05, min=0.0), h)

                unfreeze_factor = torch.tanh(unfreeze_gain * grad_abs / (adaptive_thr + 1e-12))
                h = torch.clamp(h + unfreeze_factor, min=0.0, max=2.5)

                delta_w = -lr * exp_avg
                delta_t = torch.clamp(self.global_step - st['last_update'], min=1)
                M = 1.0 + alpha_t * (c ** 2) * h / (delta_t.float().sqrt() + 1e-12)
                M = torch.clamp(M, max=M_max)

                if do_update:
                    update_mask = h > 0.05
                    if update_mask.any():
                        full_delta = torch.zeros_like(p)
                        full_delta[update_mask] = (delta_w * M)[update_mask]
                        p.add_(full_delta)
                        st['last_update'][update_mask] = self.global_step

                st['h'] = h

        return loss
    
