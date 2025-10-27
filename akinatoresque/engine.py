import numpy as np

def soft(p, alpha=0.02, A=3): return (p + alpha) / (1 + A*alpha)

class Engine:
    def __init__(self, entities, questions, L, thresh=0.85, max_q=25, alpha=0.02):
        self.entities = entities
        self.questions = questions
        self.L = L.astype(np.float64)  # [Q,E,3]
        self.Q, self.E, _ = self.L.shape
        self.thresh, self.max_q, self.alpha = thresh, max_q, alpha
        self.reset()

    def reset(self):
        self.belief = np.ones(self.E) / self.E
        self.asked = set()
        self.turn = 0
        self.done = False
        self.current_q = None

    def entropy(self, b):
        nz = b[b > 0]; return float(-(nz*np.log2(nz)).sum())

    def expected_entropy(self, q):
        E = 0.0
        for a in range(3):
            pa = float((self.belief*soft(self.L[q,:,a], self.alpha)).sum())
            if pa <= 1e-15: continue
            post = self.belief*soft(self.L[q,:,a], self.alpha)
            post /= post.sum()
            E += pa * self.entropy(post)
        return E

    def select_question(self):
        best_q, best = None, float("inf")
        for q in range(self.Q):
            if q in self.asked: continue
            sc = self.expected_entropy(q)
            if sc < best: best, best_q = sc, q
        self.current_q = best_q
        return best_q

    def apply_answer(self, btn):
        maps = {
            "YES":  np.array([1.0,0.0,0.0]),
            "NO":   np.array([0.0,1.0,0.0]),
            "IDK":  np.array([0.0,0.0,1.0]),
            "PROB": np.array([0.6,0.0,0.4]),
            "PNOT": np.array([0.0,0.6,0.4]),
        }
        w = maps[btn]
        q = self.current_q
        post = np.zeros_like(self.belief)
        for a in range(3):
            if w[a] <= 0: continue
            like = soft(self.L[q,:,a], self.alpha)
            tmp = self.belief * like
            s = tmp.sum()
            if s > 0: tmp /= s
            post += w[a]*tmp
        self.belief = post / post.sum()
        self.asked.add(q)
        self.turn += 1
        if self.turn >= self.max_q or self.belief.max() >= self.thresh:
            self.done = True

    def guess(self):
        idx = int(self.belief.argmax())
        return idx, float(self.belief[idx])

    def topk(self, k=5):
        idx = np.argsort(-self.belief)[:k]
        return [(int(i), float(self.belief[i])) for i in idx]
