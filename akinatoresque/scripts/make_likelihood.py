# scripts/make_likelihood.py
# Build likelihood.npy with shape [Q, E, 3] storing P(answer|entity,question)
# Answers are ordered: [YES, NO, UNKNOWN]
import json, numpy as np, os

ROOT = os.path.dirname(os.path.dirname(__file__)) if "__file__" in globals() else "."
ENT_PATH = os.path.join(ROOT, "data", "entities.json")
QUE_PATH = os.path.join(ROOT, "data", "questions.json")
OUT_PATH = os.path.join(ROOT, "data", "likelihood.npy")

with open(ENT_PATH, "r", encoding="utf-8") as f:
    entities = json.load(f)
with open(QUE_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

E, Q = len(entities), len(questions)
L = np.zeros((Q, E, 3), dtype=np.float32)

def setL(qid, eids, yes=0.9, no=0.05, unk=0.05):
    for e in eids:
        L[qid, e, 0] = yes
        L[qid, e, 1] = no
        L[qid, e, 2] = unk

# Index helpers by type
vg = [i for i,x in enumerate(entities) if x["type"]=="vg_char"]
pl = [i for i,x in enumerate(entities) if x["type"]=="place"]
fo = [i for i,x in enumerate(entities) if x["type"]=="fiction_obj"]
ro = [i for i,x in enumerate(entities) if x["type"]=="real_obj"]

# q0: Is it real?
for e in vg + fo: setL(0, [e], yes=0.05, no=0.9,  unk=0.05)
for e in ro:      setL(0, [e], yes=0.9,  no=0.05, unk=0.05)
for e in pl:      setL(0, [e], yes=0.95, no=0.03, unk=0.02)

# q1: Is it a person or character?
for e in vg:      setL(1, [e], yes=0.95, no=0.03, unk=0.02)
for e in ro + pl: setL(1, [e], yes=0.05, no=0.9,  unk=0.05)
for e in fo:      setL(1, [e], yes=0.1,  no=0.8,  unk=0.1)

# q2: Is it from a video game?
for e in vg:      setL(2, [e], yes=0.95, no=0.03, unk=0.02)

# q3: Is it a place?
for e in pl:      setL(3, [e], yes=0.97, no=0.02, unk=0.01)
for e in vg+fo+ro: setL(3, [e], yes=0.02, no=0.95, unk=0.03)

# q4: Is it an object you can hold?
for e in ro + fo: setL(4, [e], yes=0.9,  no=0.07, unk=0.03)
for e in pl:      setL(4, [e], yes=0.02, no=0.96, unk=0.02)
for e in vg:      setL(4, [e], yes=0.15, no=0.75, unk=0.10)

# Fill remaining questions (if any) with neutral priors
for q in range(Q):
    for e in range(E):
        if L[q, e].sum() == 0:
            L[q, e] = np.array([0.33, 0.33, 0.34], dtype=np.float32)

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
np.save(OUT_PATH, L)
print(f"Saved {OUT_PATH} with shape {L.shape}")
