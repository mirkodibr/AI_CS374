# Blackjack AI — PIMC vs Basic Strategy

A Blackjack simulation and interactive game that compares two decision-making agents: a **Perfect Information Monte Carlo (PIMC)** agent and a classic **Basic Strategy** agent.

Built for CS374 (Artificial Intelligence).

---

## Overview

The project implements a full 6-deck Blackjack environment (hit, stand, double down, split) and evaluates two AI agents against each other over thousands of simulated deals.

| Agent | Approach |
|---|---|
| **Basic Strategy** | Follows the standard S17 chart (pair splitting, soft totals, hard totals) |
| **PIMC** | Samples a predicted deck, runs Monte Carlo trials for each action, picks the highest expected reward |

---

## Project Structure

| File | Description |
|---|---|
| `environment.py` | Blackjack game engine — deck, scoring, actions, state |
| `basic_strategy.py` | Pure S17 basic strategy agent |
| `pimc.py` | PIMC agent using Monte Carlo simulation with basic strategy rollouts |
| `gui.py` | Tkinter GUI for interactive play |
| `testing.py` | Headless simulation runner for benchmarking both agents |
| `action_suggestions.py` | Action suggestion utilities |
| `bj_db.py` | Database utilities |

---

## Getting Started

### Requirements

- Python 3.10+
- `tkinter` (included with standard Python on Windows/macOS)

### Run the GUI

```bash
python gui.py
```

**Controls:**

| Input | Action |
|---|---|
| Click **Hit** | Draw a card |
| Click **Stand** | End your turn |
| Click **Double Down** | Double bet, draw one card |
| Click **Split** | Split a matching pair |
| `→` (Right Arrow) | Let the PIMC agent play one action |
| `←` (Left Arrow) | Let Basic Strategy play one action |

### Run the Benchmark

```bash
python testing.py
```

Simulates 5,000 deals for each agent and prints win rates, splits, and hand counts.

---

## How the PIMC Agent Works

1. **Guess the deck** — infers remaining cards by tracking all seen cards across the 6-deck shoe.
2. **Determine a state** — fills in the dealer's hidden card with a randomly drawn predicted card.
3. **Monte Carlo rollouts** — for each of the 4 possible actions (hit/stand/double/split), simulates `N` trials using basic strategy to play out the rest of the hand.
4. **Pick the best action** — selects the action with the highest average reward across trials.

The number of trials is configurable (`numberofTrials`, default `1000`).

---

## Test Results

Benchmark results from extended simulation runs are stored in the `.txt` and `.csv` files:

- `tests for 10,000 by 10 trials.txt`
- `tests for 10,000 by 100 trials.txt`
- `tests for 30,000 by 1000 trials.txt`
- `tests for 5000 deals by 10000 trials.txt`
- `win_rates_table.csv` through `win_rates_table_4.csv`

---

## Actions

| Code | Action |
|---|---|
| `0` | Hit |
| `1` | Stand |
| `2` | Double Down |
| `3` | Split |
