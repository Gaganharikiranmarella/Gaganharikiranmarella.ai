# Likelihood channels: YES=1, NO=2, UNKNOWN=3
answers <- c(YES=1L, NO=2L, UNKNOWN=3L)  # R 1-based [web:24][web:45]

soft <- function(p, alpha=0.02, A=3L) {
  (p + alpha) / (1 + A*alpha)
}  # Laplace smoothing for noise robustness [web:45][web:24]

update_belief <- function(belief, q, a, L, alpha=0.02, eps=1e-12) {
  like <- soft(L[q, , a], alpha)
  b <- pmax(eps, belief * like)
  b / sum(b)
}  # Bayes update normalized [web:45][web:24]

entropy <- function(b) {
  nz <- b[b > 0]
  -sum(nz * log2(nz))
}  # Shannon entropy [web:45][web:24]

expected_entropy <- function(belief, q, L, alpha=0.02) {
  E <- 0
  for (a in 1:3) {
    pa <- sum(belief * soft(L[q, , a], alpha))
    if (pa <= 1e-15) next
    post <- belief * soft(L[q, , a], alpha)
    post <- post / sum(post)
    E <- E + pa * entropy(post)
  }
  E
}  # expected posterior entropy for q [web:45][web:24]

select_question_entropy <- function(belief, asked, Q, L) {
  best_q <- NA_integer_; best <- Inf
  for (q in 1:Q) {
    if (q %in% asked) next
    sc <- expected_entropy(belief, q, L)
    if (sc < best) { best <- sc; best_q <- q }
  }
  best_q
}  # greedy entropy minimization baseline [web:24][web:45]

# Map five UI buttons to a soft mixture over the three channels
map_button_to_channel <- function(btn) {
  if (btn == "YES")      c(YES=1, NO=0, UNKNOWN=0)
  else if (btn == "NO")  c(YES=0, NO=1, UNKNOWN=0)
  else if (btn == "IDK") c(YES=0, NO=0, UNKNOWN=1)
  else if (btn == "PROB") c(YES=.6, NO=0, UNKNOWN=.4)
  else if (btn == "PNOT") c(YES=0, NO=.6, UNKNOWN=.4)
  else c(YES=0, NO=0, UNKNOWN=1)
}  # “Probably” softens yes/no, consistent with common usage [web:66][web:9]

apply_answer <- function(belief, q, btn, L, alpha=0.02) {
  w <- map_button_to_channel(btn)
  post <- rep(0, length(belief))
  for (a in 1:3) {
    if (w[a] <= 0) next
    like <- soft(L[q, , a], alpha)
    tmp <- belief * like
    s <- sum(tmp)
    if (s > 0) tmp <- tmp / s
    post <- post + w[a] * tmp
  }
  post / sum(post)
}  # mixture posterior respects five-button semantics [web:45][web:24]
