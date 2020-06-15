import random
import numpy as np
import time
from seeker import Seeker
from config import Config

config = Config()


class SOA:
    def __init__(self, model):
        self.S = [Seeker(config.n, i) for i in range(config.pop_size)]
        self.g_best = None
        self.g_best_y = None
        self.model = model
        self.h=[]
        self.u_p=[]

    def run(self):
        t = 0
        for seeker in self.S:
            seeker.x.append(np.array([random.uniform(config.x_min[_], config.x_max[_]) for _ in range(config.n)]))

        cur_time = time.time()
        while t < config.generation_num:
            current_y = []
            g_avg = np.array([0.0 for _ in range(config.n)])

            for seeker in self.S:
                g_avg += seeker.x[t]
                seeker.y.append(self.model.objective_func(seeker.x[t]))
                current_y.append(seeker.y[t])
                if seeker.p_best is None or self.model.better(seeker.y[t], seeker.p_best_y):
                    seeker.p_best = seeker.x[t].copy()
                    seeker.p_best_y = seeker.y[t]
                if self.g_best is None or self.model.better(seeker.y[t], self.g_best_y):
                    self.g_best = seeker.x[t].copy()
                    self.g_best_y = seeker.y[t]

            g_avg /= config.pop_size
            omega = 0.9 - (0.9 - 0.1) / config.generation_num * t
            _omega = 0.9 - (0.9 - 0.1) / config.generation_num * t
            delta = _omega * np.abs(np.array(self.g_best - g_avg))
            phi_1 = random.random()
            phi_2 = random.random()
            I = np.argsort(current_y)
            I = [index + 1 for index in I]
            mu = []

            for i, seeker in enumerate(self.S):
                seeker.d_ego = seeker.p_best - seeker.x[t]
                seeker.d_alt = self.g_best - seeker.x[t]
                t1 = t2 = t
                if t >= 2:
                    temp_y = seeker.y[t - 2:t + 1]  # t-2, t-1, t
                    temp_index = np.argsort(temp_y)  # 0, 1, 2
                    t1 = t - 2 + temp_index[0]  # best
                    t2 = t - 2 + temp_index[2]  # worst
                elif t == 1:
                    temp_y = seeker.y  # t-1, t
                    temp_index = np.argsort(temp_y)  # 0, 1
                    t1 = temp_index[0]  # best
                    t2 = temp_index[1]  # worst
                # get d
                seeker.d_pro = seeker.x[t1] - seeker.x[t2]
                seeker.d = np.sign(omega*seeker.d_pro + phi_1*seeker.d_ego + phi_2*seeker.d_alt)

                # get alpha
                mu.append(config.mu_max - (config.pop_size-I[i])/(config.pop_size-1) * (config.mu_max-config.mu_min))
                seeker.mu = np.array([random.uniform(mu[i], 1) for _ in range(seeker.M)])
                seeker.alpha = np.array([delta[j]*np.sqrt(-np.log(seeker.mu[j])) for j in range(seeker.M)])
                seeker.alpha[seeker.alpha < 0] = 0
                seeker.alpha[seeker.alpha > 3*delta] = 3*delta[seeker.alpha > 3*delta]

                # update position
                new_x = seeker.x[t]+seeker.alpha*seeker.d
                new_x = np.array([min(new_x[i],config.x_max[i]) for i in range(len(new_x))])
                new_x = np.array([max(new_x[i], config.x_min[i]) for i in range(len(new_x))])

                seeker.x.append(new_x)

            if t % 10 == 0:
                # print("generation", t, "done", self.g_best_y, time.time()-cur_time)
                cur_time = time.time()
            t += 1
            self.h.append(self.g_best[0])
            self.u_p.append(self.g_best[1])


