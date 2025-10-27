# Simple simulator + shaped reward (optional RL extension) [web:14][web:39]
simulate_episode <- function(L, entities, questions, max_q=25, thresh=0.85, alpha=0.02, noise=0.1) {
  E <- nrow(entities); Q <- nrow(questions)
  target <- sample.int(E, 1)
  belief <- rep(1/E, E)
  asked <- integer(0)
  for (t in 1:max_q) {
    q <- select_question_entropy(belief, asked, Q, L)  # bootstrap policy [web:24][web:45]
    asked <- c(asked, q)
    pa <- soft(L[q, target, ], alpha)
    pa <- (1-noise)*pa + noise*c(1/3, 1/3, 1/3)
    a <- sample(1:3, 1, prob=pa)
    belief <- update_belief(belief, q, a, L, alpha)
    if (max(belief) >= thresh) break
  }
  guess <- which.max(belief)
  reward <- if (guess == target) 1 - 0.04*length(asked) else -0.2  # shaped as in 20Q RL [web:14][web:39]
  list(asked=asked, reward=reward, guess=guess, target=target)
}
