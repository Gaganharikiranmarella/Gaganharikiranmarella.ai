library(shiny)  # UI + reactivity [web:24][web:45]

# Model utilities
source("R/logic.R")  # belief update, entropy selection, button mapping [web:24][web:45]

# Load in-memory dataset (no DB)
entities  <- read.csv("data/entities.csv", stringsAsFactors = FALSE)  # 40 total [web:24][web:45]
questions <- read.csv("data/questions.csv", stringsAsFactors = FALSE) # ~100–150 [web:24][web:45]
L <- readRDS("data/likelihood.rds")                                   # array(Q, E, 3) [web:45][web:24]

E <- nrow(entities); Q <- nrow(questions)

ui <- fluidPage(
  tags$head(tags$link(rel="stylesheet", href="styles.css")),
  div(class="app",
      div(class="container",
          div(class="hero", img(src="mascot.png", alt="Genie")),
          div(class="stage",
              uiOutput("progressUI"),
              uiOutput("questionUI"),
              div(class="answers",
                  actionButton("btn_yes",  "Yes",            class="btn yes"),
                  actionButton("btn_prob", "Probably",       class="btn prob"),
                  actionButton("btn_idk",  "Don't know",     class="btn idk"),
                  actionButton("btn_pnot", "Probably not",   class="btn pnot"),
                  actionButton("btn_no",   "No",             class="btn no")
              ),
              uiOutput("top5UI")
          )
      )
  ),
  uiOutput("revealModal")
)

server <- function(input, output, session) {
  rv <- reactiveValues(
    belief = rep(1/E, E),
    asked = integer(0),
    turn = 0L,
    current_q = NA_integer_,
    done = FALSE,
    guess_idx = NA_integer_
  )

  select_next_question <- function() {
    select_question_entropy(rv$belief, rv$asked, Q, L)  # entropy baseline [web:24][web:45]
  }

  ask_or_reveal <- function() {
    if (rv$done) return()
    if (is.na(rv$current_q)) rv$current_q <- select_next_question()
    if (max(rv$belief) >= 0.85 || rv$turn >= 25) {
      rv$done <- TRUE
      rv$guess_idx <- which.max(rv$belief)
    }
  }

  observe({ if (rv$turn == 0) ask_or_reveal() })

  handle_answer <- function(btn) {
    req(!rv$done, !is.na(rv$current_q))
    rv$belief <- apply_answer(rv$belief, rv$current_q, btn, L, alpha=0.02)  # five→three channel [web:66][web:9]
    rv$asked <- c(rv$asked, rv$current_q)
    rv$turn  <- rv$turn + 1L
    rv$current_q <- select_next_question()
    ask_or_reveal()
  }

  observeEvent(input$btn_yes,  handle_answer("YES"))
  observeEvent(input$btn_no,   handle_answer("NO"))
  observeEvent(input$btn_idk,  handle_answer("IDK"))
  observeEvent(input$btn_prob, handle_answer("PROB"))
  observeEvent(input$btn_pnot, handle_answer("PNOT"))

  output$progressUI <- renderUI({
    pct <- paste0(round(100*min(rv$turn,25)/25), "%")
    tagList(
      div(class="progress", div(class="bar", style=paste0("width:", pct, ";"))),
      tags$span(paste0("Question ", min(rv$turn+1,25), " of 25"))
    )  # pacing cues [web:59][web:60]
  })

  output$questionUI <- renderUI({
    if (rv$done) h1(class="question", "Let's see the guess…")
    else {
      req(!is.na(rv$current_q))
      h1(class="question", questions$text[rv$current_q])
    }
  })

  output$top5UI <- renderUI({
    b <- rv$belief; ord <- order(b, decreasing = TRUE)[1:5]
    div(class="top5",
        tags$div("Top candidates:"),
        tags$ul(lapply(ord, function(i) tags$li(sprintf("%s (%.1f%%)", entities$name[i], 100*b[i]))))
    )  # transparency of belief [web:24][web:45]
  })

  output$revealModal <- renderUI({
    req(rv$done)
    idx <- rv$guess_idx
    showModal(modalDialog(
      title = "Is this your choice?",
      tagList(
        tags$h2(entities$name[idx]),
        tags$p(sprintf("Confidence: %.1f%%", 100*rv$belief[idx]))
      ),
      footer = tagList(
        modalButton("That's wrong"),
        actionButton("btn_right", "That's right!", class="btn primary")
      ),
      easyClose = TRUE
    ))
    NULL
  })

  observeEvent(input$btn_right, {
    removeModal()
    showModal(modalDialog(
      title = "Yay!", tags$p("Want to play again?"),
      footer = tagList(actionButton("btn_again", "Play again"), modalButton("Close")),
      easyClose = TRUE
    ))
  })

  observeEvent(input$btn_again, {
    removeModal()
    rv$belief <- rep(1/E, E)
    rv$asked  <- integer(0)
    rv$turn   <- 0L
    rv$current_q <- NA_integer_
    rv$done <- FALSE
    rv$guess_idx <- NA_integer_
    ask_or_reveal()
  })
}

shinyApp(ui, server)
