# akinatoresque (R Shiny)

Path: D:/Gaganharikiranmarella.ai/akinatoresque

Run:
1) Open R/RStudio.
2) Ensure user library is writable. If needed:
   dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE)
   .libPaths(Sys.getenv("R_LIBS_USER"))
3) install.packages(c("shiny"))
4) setwd("D:/Gaganharikiranmarella.ai/akinatoresque")
5) shiny::runApp(".")

Gameplay:
- 25-question cap, five buttons (Yes/Probably/Don't know/Probably not/No).
- Entropy-based question selection with Bayesian belief updates.
- Reveal when max belief ≥ 0.85 or after 25 questions.

Data:
- data/entities.csv — 40 rows across {vg_char, place, fiction_obj, real_obj}
- data/questions.csv — ~100–150 questions
- data/likelihood.rds — array(Q,E,3) for YES/NO/UNKNOWN

Notes:
- To edit look-and-feel, change www/styles.css and mascot.png.
- Optional RL: see R/rl.R for a simulator + shaped reward scaffold.
