# 🐢 Turtle Grand Prix - Championship Racing Game

A feature-packed, arcade-inspired **Turtle Racing Game** built with Python's built-in `turtle` graphics module and standard library. Place strategic bets, watch dynamic nitro boosts, track live commentary, and compete for the championship title!

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Standard%20Library)-brightgreen)

---

## ✨ Features & Enhancements

- 🏎️ **F1 Grand Prix Race Track** — Asphalt racing surface, Formula 1 alternating red-and-white curbs, distance markers (25%, 50%, 75%), starting grid, and double-checkered finish line.
- 🐢 **6 Unique Racers with Traits & Odds**:
  - 🔴 **Crimson Flash** (`3.0x`) — High top speed, aggressive accelerator.
  - 🔵 **Azure Torrent** (`2.6x`) — Consistent cruiser, steady pace.
  - 🟢 **Emerald Viper** (`3.5x`) — Nitro addict with frequent turbo bursts.
  - 🟡 **Volt Spark** (`2.8x`) — Rocket starter with rapid early acceleration.
  - 🟣 **Shadow Void** (`4.0x`) — Comeback king, gains speed boost when trailing.
  - 🟠 **Solar Blaze** (`4.5x`) — Chaos wildcard with unpredictable sprint surges.
- 💰 **Economy & Betting System**:
  - Start with **100 Coins** in your wallet.
  - Payout odds calculated per racer.
  - Win streak tracker and round counter.
  - Stimulus package if you ever go bankrupt!
- ⚡ **Dynamic In-Race Mechanics**:
  - Real-time **Nitro Boosts** with visual particle spark trails.
  - **Live Commentary Ticker** tracking lead overtakes and nitro activations.
- 🏆 **Podium & Finish Camera**:
  - Full finish rankings (1st, 2nd, 3rd) with precise finish timestamps.
  - Confetti victory celebration burst at the finish line.
  - Profit/loss financial ledger after each race.
- 🔊 **Dynamic Audio & Sound FX**:
  - Countdown beeps, nitro woosh, select clicks, and win/loss fanfares (using Python standard library on Windows).
  - Press `M` anytime to mute/unmute.
- 🎮 **Full Keyboard & Mouse Controls**:
  - Click on any lane to select that racer, or press keys `1` through `6`.
  - Adjust bets with `[↑]` / `[↓]`, go `[A]`ll-in, or hit `[SPACE]` to start.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8** or higher (all modules used are built into Python's standard library: `turtle`, `random`, `time`, `threading`, and `winsound`).
- No `pip install` required!

### Run the Game

```bash
python app.py
```

---

## 🎮 Controls

| Action | Controls |
| :--- | :--- |
| **Select Racer** | Keys `1` to `6` or **Click directly on any lane** |
| **Adjust Bet** | `[↑]` to increase / `[↓]` to decrease |
| **All-In Bet** | `[A]` key |
| **Start Race / Next Round** | `[SPACE]`, `[Enter]`, or **Click Start Button** |
| **Toggle Sound** | `[M]` key |
| **Quit Game** | `[Q]` or `[Escape]` |

---

## 📁 Project Structure

```
Turtle_Racing/
├── app.py          # Main game engine & graphics
└── README.md       # Project documentation
```

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Author

Made with ❤️ by **[Omrawat11](https://github.com/Omrawat11)**
