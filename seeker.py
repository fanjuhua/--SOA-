
class Seeker:
    def __init__(self, M, i):
        self.M = M
        self.i = i
        self.x = []
        self.y = []
        self.p_best = None
        self.p_best_y = None
        self.d_ego = None
        self.d_alt = None
        self.d_pro = None
        self.d = None
        self.mu = None
        self.alpha = None
