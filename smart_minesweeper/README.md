# Smart Minesweeper with Heuristic & Sub-Heuristic AI

Welcome to **Smart Minesweeper**, an intelligent twist on the classic Minesweeper game enhanced with layered heuristic AI decision-making!

---

## Project Overview

This project implements a **16x16 Minesweeper** game featuring:

- **3 randomly placed mines**
- **Heuristic values** assigned to tiles immediately around mines (values 1-3 by proximity)
- **Sub-Heuristic values** calculated for other tiles based on distance and neighboring heuristics
- **Interactive gameplay** with Reveal and Flag actions
- An **AI agent** that suggests intelligent moves using combined heuristic evaluations
- A modern, responsive **Streamlit** interface with live board visualization and dynamic coloring

---

## Features

- Minesweeper rules with classic tile elimination and mine defusal (flagging)
- Dual scoring system: **heuristic + sub-heuristic** layered evaluation for intelligent play
- AI-driven move suggestions based on probabilistic inference
- Responsive UI displaying heuristic intensities through a color gradient
- User-friendly controls for action selection and game management

---

## Installation & Setup

1. Clone the repository:

git clone https://github.com/Gaganharikiranmarella/Gaganharikiranmarella.ai/smart_minesweeper.git
cd smart_minesweeper


2. Install dependencies:

pip install -r requirements.txt


3. Run the Streamlit app:

streamlit run ui/streamlit_app.py


---

## Usage

- Choose between **Reveal** or **Flag** mode.
- Click on tiles to reveal or flag them.
- Tiles display heuristic or sub-heuristic values explaining mine likelihood.
- Use **AI Suggest Move** to get AI recommendations.
- Restart anytime to play a fresh game.

---

## Project Structure

smart_minesweeper/
├── ai/ # Core game logic and AI agent code
├── ui/ # Streamlit user interface
├── utils/ # Helper functions
├── tests/ # Unit tests
├── requirements.txt
└── README.md


---

## Contributing

Contributions, suggestions, and improvements are welcome! Feel free to fork the repo and submit pull requests.

---

## License

This project is open-source under the MIT License.

---

Enjoy playing Smart Minesweeper and exploring AI-powered gameplay!


