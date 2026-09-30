"""
🐢 TURTLE GRAND PRIX - Championship Racing Game
A feature-rich, high-performance Turtle Racing game built with Python's built-in turtle module.

Features:
- 🏎️ Grand Prix Track with F1-style curbs, distance markers & checkered finish
- 🐢 6 Unique Racers with distinct personalities, stats, odds & nitro mechanics
- 💰 Interactive Economy & Betting System (Wallet, odds payout, win streaks)
- ⚡ In-race Nitro boosts, speed trails & live race commentary ticker
- 🎊 Confetti victory celebration, finish-line camera & podium ceremony
- 🔊 Dynamic sound effects with non-blocking audio (toggle with 'M')
- 🎮 Full keyboard + mouse support (click lanes, adjust bets, space to race)
"""

import math
import random
import sys
import threading
import time
import turtle

# Optional Windows sound support (zero external dependencies)
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


# ==============================================================================
#                                CONSTANTS
# ==============================================================================

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 720

# Track coordinates
TRACK_LEFT = -480
TRACK_RIGHT = 480
TRACK_TOP = 205
TRACK_BOTTOM = -215
TRACK_WIDTH = TRACK_RIGHT - TRACK_LEFT
TRACK_HEIGHT = TRACK_TOP - TRACK_BOTTOM

START_X = -380
FINISH_X = 400

# 6 Lanes centered cleanly across track height
LANE_Y = [160, 95, 30, -35, -100, -165]
NUM_RACERS = 6

# Color Palette (Modern Cyber/Arcade Dark Theme)
BG_COLOR = "#0f141d"
TRACK_BG = "#1e272e"
TRACK_BORDER = "#2f3640"
CURB_RED = "#eb4d4b"
CURB_WHITE = "#f5f6fa"
TEXT_PRIMARY = "#f1f2f6"
TEXT_MUTED = "#a4b0be"
ACCENT_GOLD = "#f1c40f"
ACCENT_GREEN = "#2ed573"
ACCENT_RED = "#ff4757"

# Racer Profiles: Personalities, Traits & Dynamic Racing Stats
RACER_DATA = [
    {
        "id": 0,
        "name": "Crimson Flash",
        "color": "#ff4757",
        "secondary": "#ff6b81",
        "badge": "🔴 1",
        "trait": "Top Speed Demon",
        "odds": 3.0,
        "speed_min": 2,
        "speed_max": 8,
        "nitro_chance": 0.08,
    },
    {
        "id": 1,
        "name": "Azure Torrent",
        "color": "#00d2d3",
        "secondary": "#48dbfb",
        "badge": "🔵 2",
        "trait": "Steady Cruiser",
        "odds": 2.6,
        "speed_min": 3,
        "speed_max": 6,
        "nitro_chance": 0.05,
    },
    {
        "id": 2,
        "name": "Emerald Viper",
        "color": "#10ac84",
        "secondary": "#1dd1a1",
        "badge": "🟢 3",
        "trait": "Nitro Addict",
        "odds": 3.5,
        "speed_min": 1,
        "speed_max": 7,
        "nitro_chance": 0.16,
    },
    {
        "id": 3,
        "name": "Volt Spark",
        "color": "#ffa502",
        "secondary": "#ffc048",
        "badge": "🟡 4",
        "trait": "Rocket Starter",
        "odds": 2.8,
        "speed_min": 3,
        "speed_max": 7,
        "nitro_chance": 0.07,
    },
    {
        "id": 4,
        "name": "Shadow Void",
        "color": "#9b59b6",
        "secondary": "#a55eea",
        "badge": "🟣 5",
        "trait": "Comeback King",
        "odds": 4.0,
        "speed_min": 2,
        "speed_max": 6,
        "nitro_chance": 0.10,
    },
    {
        "id": 5,
        "name": "Solar Blaze",
        "color": "#ff7f50",
        "secondary": "#ff6348",
        "badge": "🟠 6",
        "trait": "Chaos Wildcard",
        "odds": 4.5,
        "speed_min": 1,
        "speed_max": 9,
        "nitro_chance": 0.12,
    },
]


# ==============================================================================
#                               AUDIO MANAGER
# ==============================================================================

class SoundManager:
    """Non-blocking audio engine using Python standard library winsound."""
    def __init__(self):
        self.enabled = HAS_WINSOUND

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def play(self, sound_name):
        if not self.enabled or not HAS_WINSOUND:
            return

        def _sound_worker():
            try:
                if sound_name == "tick":
                    winsound.Beep(587, 80)
                elif sound_name == "go":
                    winsound.Beep(1174, 250)
                elif sound_name == "select":
                    winsound.Beep(880, 50)
                elif sound_name == "nitro":
                    winsound.Beep(980, 70)
                elif sound_name == "win":
                    for freq in [523, 659, 784, 1046]:
                        winsound.Beep(freq, 90)
                elif sound_name == "lose":
                    for freq in [440, 370, 311]:
                        winsound.Beep(freq, 120)
            except Exception:
                pass

        threading.Thread(target=_sound_worker, daemon=True).start()


# ==============================================================================
#                               RACER CLASS
# ==============================================================================

class Racer:
    """Encapsulates racer state, physics, traits, and visuals."""
    def __init__(self, data, lane_y):
        self.id = data["id"]
        self.name = data["name"]
        self.color = data["color"]
        self.secondary = data["secondary"]
        self.badge = data["badge"]
        self.trait = data["trait"]
        self.odds = data["odds"]
        self.speed_min = data["speed_min"]
        self.speed_max = data["speed_max"]
        self.nitro_chance = data["nitro_chance"]
        self.lane_y = lane_y

        # Turtle instance
        self.turtle = turtle.Turtle(shape="turtle")
        self.turtle.shapesize(1.6, 1.6)
        self.turtle.color(self.color)
        self.turtle.penup()
        self.turtle.speed(0)

        # Race state
        self.finished = False
        self.finish_time = 0.0
        self.finish_rank = 0
        self.is_nitro = False

    def reset_position(self):
        self.finished = False
        self.finish_time = 0.0
        self.finish_rank = 0
        self.is_nitro = False
        self.turtle.goto(START_X, self.lane_y)
        self.turtle.setheading(0)
        self.turtle.showturtle()

    def update_physics(self, current_rank):
        """Calculate step distance considering personality traits and nitro."""
        if self.finished:
            return 0, False

        step = random.randint(self.speed_min, self.speed_max)
        nitro_triggered = False

        # Trait: Volt Spark rocket launch early in race
        if self.name == "Volt Spark" and self.turtle.xcor() < -150:
            step += random.randint(1, 2)

        # Trait: Shadow Void comeback surge when in the back half
        if self.name == "Shadow Void" and current_rank >= 4:
            step += random.randint(1, 3)

        # Trait: Nitro boost chance
        if random.random() < self.nitro_chance:
            step += random.randint(7, 12)
            nitro_triggered = True
            self.is_nitro = True
        else:
            self.is_nitro = False

        self.turtle.forward(step)
        return step, nitro_triggered


# ==============================================================================
#                               TRACK RENDERER
# ==============================================================================

def create_layer_drawer():
    """Create a dedicated fast drawer turtle for layer rendering."""
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    return t


def draw_race_track(drawer):
    """Render the asphalt track, curbs, dashed lanes, and checkered finish."""
    drawer.clear()

    # --- 1. Asphalt Main Surface ---
    drawer.goto(TRACK_LEFT, TRACK_BOTTOM)
    drawer.color(TRACK_BG)
    drawer.begin_fill()
    for _ in range(2):
        drawer.forward(TRACK_WIDTH)
        drawer.left(90)
        drawer.forward(TRACK_HEIGHT)
        drawer.left(90)
    drawer.end_fill()

    # --- 2. Track Outer Borders ---
    drawer.pensize(2)
    drawer.color(TRACK_BORDER)
    drawer.goto(TRACK_LEFT, TRACK_BOTTOM)
    drawer.pendown()
    for _ in range(2):
        drawer.forward(TRACK_WIDTH)
        drawer.left(90)
        drawer.forward(TRACK_HEIGHT)
        drawer.left(90)
    drawer.penup()

    # --- 3. Grand Prix Alternating Curbs (Top & Bottom) ---
    curb_seg_width = 30
    curb_height = 8
    num_curb_segs = int(TRACK_WIDTH / curb_seg_width)

    for curb_y in [TRACK_TOP, TRACK_BOTTOM - curb_height]:
        for i in range(num_curb_segs):
            x = TRACK_LEFT + i * curb_seg_width
            drawer.color(CURB_RED if i % 2 == 0 else CURB_WHITE)
            drawer.goto(x, curb_y)
            drawer.begin_fill()
            for _ in range(2):
                drawer.forward(curb_seg_width)
                drawer.left(90)
                drawer.forward(curb_height)
                drawer.left(90)
            drawer.end_fill()

    # --- 4. Dashed Lane Dividers ---
    drawer.pensize(1)
    drawer.color("#34495e")
    lane_dividers_y = [127, 62, -2, -67, -132]
    for dy in lane_dividers_y:
        drawer.goto(TRACK_LEFT + 15, dy)
        drawer.pendown()
        for _ in range(35):
            drawer.forward(14)
            drawer.penup()
            drawer.forward(12)
            drawer.pendown()
        drawer.penup()

    # --- 5. Distance Milestone Markers (25%, 50%, 75%) ---
    milestones = [
        (START_X + (FINISH_X - START_X) * 0.25, "25%"),
        (START_X + (FINISH_X - START_X) * 0.50, "50%"),
        (START_X + (FINISH_X - START_X) * 0.75, "75%"),
    ]
    drawer.color("#485460")
    for mx, label in milestones:
        drawer.pensize(1)
        drawer.goto(mx, TRACK_BOTTOM + 8)
        drawer.pendown()
        drawer.goto(mx, TRACK_TOP - 8)
        drawer.penup()
        drawer.goto(mx, TRACK_TOP + 12)
        drawer.write(label, align="center", font=("Courier", 9, "bold"))

    # --- 6. Starting Grid Boxes ---
    drawer.pensize(2)
    drawer.color("#7f8c8d")
    drawer.goto(START_X - 10, TRACK_BOTTOM + 5)
    drawer.pendown()
    drawer.goto(START_X - 10, TRACK_TOP - 5)
    drawer.penup()

    # --- 7. Checkered Finish Line ---
    sq = 16
    cols = 2
    rows = int(TRACK_HEIGHT / sq)
    for r in range(rows):
        for c in range(cols):
            x = FINISH_X + c * sq
            y = TRACK_BOTTOM + r * sq
            drawer.color("white" if (r + c) % 2 == 0 else "black")
            drawer.goto(x, y)
            drawer.begin_fill()
            for _ in range(4):
                drawer.forward(sq)
                drawer.left(90)
            drawer.end_fill()

    # --- 8. Overhead Finish Banner ---
    drawer.color(ACCENT_GOLD)
    drawer.goto(FINISH_X + 16, TRACK_TOP + 12)
    drawer.write("🏁 FINISH", align="center", font=("Courier", 11, "bold"))


# ==============================================================================
#                               GAME CONTROLLER
# ==============================================================================

class TurtleGrandPrix:
    """Main Game Engine managing state, UI layers, input, and races."""
    def __init__(self):
        # Window & Canvas Setup
        self.screen = turtle.Screen()
        self.screen.title("🐢 TURTLE GRAND PRIX - Championship Racing")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor(BG_COLOR)
        self.screen.tracer(0)

        # Dedicated Layer Turtles
        self.track_drawer = create_layer_drawer()
        self.hud_drawer = create_layer_drawer()
        self.commentary_drawer = create_layer_drawer()
        self.banner_drawer = create_layer_drawer()
        self.fx_drawer = create_layer_drawer()

        # Audio Manager
        self.sound = SoundManager()

        # Racers
        self.racers = [Racer(data, LANE_Y[i]) for i, data in enumerate(RACER_DATA)]

        # Player State / Economy
        self.wallet = 100
        self.current_bet = 25
        self.selected_racer_id = 0
        self.win_streak = 0
        self.round_num = 1
        self.total_races_won = 0

        # Race runtime state
        self.is_running = True
        self.race_in_progress = False
        self.waiting_for_input = True
        self.start_race_flag = False

        # Setup Keybindings & Mouse Clicks
        self.bind_controls()

    def bind_controls(self):
        """Register keyboard and mouse event listeners."""
        self.screen.listen()

        # Lane / Racer selection keys 1 - 6
        for i in range(NUM_RACERS):
            key = str(i + 1)
            self.screen.onkeypress(lambda idx=i: self.select_racer(idx), key)

        # Betting adjustments
        self.screen.onkeypress(self.increase_bet, "Up")
        self.screen.onkeypress(self.decrease_bet, "Down")
        self.screen.onkeypress(self.all_in_bet, "a")
        self.screen.onkeypress(self.all_in_bet, "A")

        # Sound & Game controls
        self.screen.onkeypress(self.toggle_audio, "m")
        self.screen.onkeypress(self.toggle_audio, "M")
        self.screen.onkeypress(self.on_space_pressed, "space")
        self.screen.onkeypress(self.on_space_pressed, "Return")
        self.screen.onkeypress(self.quit_game, "q")
        self.screen.onkeypress(self.quit_game, "Q")
        self.screen.onkeypress(self.quit_game, "Escape")

        # Mouse clicks on track lanes or start button
        self.screen.onclick(self.handle_mouse_click)

    def toggle_audio(self):
        enabled = self.sound.toggle()
        self.show_commentary(f"🔊 Sound FX {'ENABLED' if enabled else 'MUTED'}")
        self.render_hud()
        self.screen.update()

    def select_racer(self, index):
        if self.race_in_progress:
            return
        if 0 <= index < NUM_RACERS:
            self.selected_racer_id = index
            self.sound.play("select")
            self.render_hud()
            self.screen.update()

    def increase_bet(self):
        if self.race_in_progress:
            return
        step = 10 if self.wallet >= 50 else 5
        if self.current_bet + step <= self.wallet:
            self.current_bet += step
            self.sound.play("select")
            self.render_hud()
            self.screen.update()

    def decrease_bet(self):
        if self.race_in_progress:
            return
        step = 10 if self.wallet >= 50 else 5
        if self.current_bet - step >= 5:
            self.current_bet -= step
            self.sound.play("select")
            self.render_hud()
            self.screen.update()

    def all_in_bet(self):
        if self.race_in_progress:
            return
        if self.wallet > 0:
            self.current_bet = self.wallet
            self.sound.play("select")
            self.show_commentary(f"🔥 ALL-IN! Bet set to full wallet ({self.wallet} Coins)!")
            self.render_hud()
            self.screen.update()

    def handle_mouse_click(self, x, y):
        """Allow clicking on lanes to select racer or clicking bottom button to start."""
        if not self.waiting_for_input:
            return

        # Check if clicked inside a racer's lane
        if TRACK_LEFT - 100 <= x <= FINISH_X + 50:
            for i, ly in enumerate(LANE_Y):
                if ly - 30 <= y <= ly + 30:
                    self.select_racer(i)
                    return

        # Check if clicked on START RACE bottom area
        if -340 <= y <= -270 and -250 <= x <= 250:
            self.on_space_pressed()

    def on_space_pressed(self):
        if self.waiting_for_input:
            self.start_race_flag = True

    def quit_game(self):
        self.is_running = False
        try:
            self.screen.bye()
        except Exception:
            pass
        sys.exit(0)

    # --------------------------------------------------------------------------
    #                               HUD & UI RENDERING
    # --------------------------------------------------------------------------

    def render_hud(self):
        """Render Title, Wallet, Selection Card, Odds, and Controls."""
        self.hud_drawer.clear()

        # 1. Main Title
        self.hud_drawer.color(ACCENT_GOLD)
        self.hud_drawer.goto(0, 310)
        self.hud_drawer.write(
            "🏆  TURTLE  GRAND  PRIX  🏆",
            align="center",
            font=("Courier", 26, "bold"),
        )

        # 2. Economy & Stats Bar
        sound_status = "ON [M]" if self.sound.enabled else "MUTED [M]"
        self.hud_drawer.color(TEXT_PRIMARY)
        self.hud_drawer.goto(0, 275)
        self.hud_drawer.write(
            f"💰 Wallet: {self.wallet} Coins  |  🔥 Streak: {self.win_streak}  |  "
            f"🏁 Round: {self.round_num}  |  🔊 Sound: {sound_status}",
            align="center",
            font=("Arial", 12, "bold"),
        )

        # 3. Lane Cards & Selected Racer Highlight
        sel_racer = self.racers[self.selected_racer_id]

        for i, racer in enumerate(self.racers):
            ly = LANE_Y[i]
            is_selected = (i == self.selected_racer_id)

            # Lane badge on left of start line
            self.hud_drawer.goto(TRACK_LEFT - 15, ly - 8)
            self.hud_drawer.color(ACCENT_GOLD if is_selected else racer.color)
            prefix = "▶ " if is_selected else "  "
            self.hud_drawer.write(
                f"{prefix}{racer.badge}",
                align="right",
                font=("Courier", 11, "bold" if is_selected else "normal"),
            )

            # Lane selection arrow indicator
            if is_selected:
                self.hud_drawer.goto(TRACK_LEFT - 95, ly - 7)
                self.hud_drawer.color(ACCENT_GOLD)
                self.hud_drawer.write("🎯 BET", align="right", font=("Courier", 9, "bold"))

        # 4. Selected Bet Summary Bar (Above bottom controls)
        potential_win = int(self.current_bet * sel_racer.odds)
        profit = potential_win - self.current_bet

        self.hud_drawer.goto(0, -250)
        self.hud_drawer.color(TEXT_PRIMARY)
        self.hud_drawer.write(
            f"SELECTED: {sel_racer.name} ({sel_racer.trait})  •  "
            f"ODDS: {sel_racer.odds}x  •  BET: {self.current_bet} Coins  •  "
            f"POTENTIAL PROFIT: +{profit} Coins",
            align="center",
            font=("Courier", 12, "bold"),
        )

        # 5. Interactive Control Hints & Start Button
        self.hud_drawer.goto(0, -282)
        self.hud_drawer.color(TEXT_MUTED)
        self.hud_drawer.write(
            "[1-6 / Click Lane] Select Racer   •   [↑ / ↓] Bet +/- 10   •   [A] All-In   •   [Q] Quit",
            align="center",
            font=("Arial", 10, "normal"),
        )

        # Prominent Start Button Prompt
        self.hud_drawer.goto(0, -320)
        self.hud_drawer.color(ACCENT_GREEN)
        self.hud_drawer.write(
            "🟢  [ PRESS SPACE OR CLICK HERE TO RACE ]  🟢",
            align="center",
            font=("Courier", 14, "bold"),
        )

    def show_commentary(self, text, color=ACCENT_GOLD):
        """Render a live race commentary line below the stats bar."""
        self.commentary_drawer.clear()
        self.commentary_drawer.color(color)
        self.commentary_drawer.goto(0, 238)
        self.commentary_drawer.write(
            text,
            align="center",
            font=("Courier", 12, "bold"),
        )

    # --------------------------------------------------------------------------
    #                           COUNTDOWN & RACE LOOP
    # --------------------------------------------------------------------------

    def perform_countdown(self):
        """Animated 3 - 2 - 1 - GO sequence with audio beeps."""
        countdown_steps = [
            ("3", ACCENT_RED, "tick"),
            ("2", "#f39c12", "tick"),
            ("1", ACCENT_GREEN, "tick"),
            ("🏁 GO! 🏁", "#00ff88", "go"),
        ]

        for text, color, sound_type in countdown_steps:
            self.banner_drawer.clear()
            self.banner_drawer.color(color)
            self.banner_drawer.goto(0, -25)
            self.banner_drawer.write(
                text,
                align="center",
                font=("Courier", 52, "bold"),
            )
            self.sound.play(sound_type)
            self.screen.update()
            time.sleep(0.55)

        self.banner_drawer.clear()
        self.screen.update()

    def run_race_loop(self):
        """Execute the 60 FPS race loop with physics, nitro, and live ranks."""
        self.race_in_progress = True
        start_time = time.time()
        finished_racers = []
        last_leader_id = None
        frame_count = 0

        while len(finished_racers) < NUM_RACERS:
            frame_count += 1

            # Determine real-time positions for traits and commentary
            active_racers = sorted(
                self.racers,
                key=lambda r: (r.finished, r.turtle.xcor()),
                reverse=True,
            )

            # Check for lead change
            current_leader = active_racers[0]
            if current_leader.id != last_leader_id and not current_leader.finished:
                last_leader_id = current_leader.id
                self.show_commentary(f"⚡ {current_leader.name} takes the lead!", current_leader.color)

            # Update each racer
            for rank_idx, racer in enumerate(active_racers):
                if racer.finished:
                    continue

                step, nitro = racer.update_physics(rank_idx)

                # Nitro visual spark & sound
                if nitro:
                    self.sound.play("nitro")
                    self.show_commentary(f"🔥 {racer.name} activated NITRO BOOST!", racer.secondary)
                    # Draw subtle nitro trail spark
                    self.fx_drawer.goto(racer.turtle.xcor() - 25, racer.lane_y)
                    self.fx_drawer.color(racer.secondary)
                    self.fx_drawer.dot(8)

                # Check finish line crossing
                if racer.turtle.xcor() >= FINISH_X and not racer.finished:
                    racer.finished = True
                    racer.finish_time = round(time.time() - start_time, 2)
                    racer.finish_rank = len(finished_racers) + 1
                    finished_racers.append(racer)

                    # Winner announcement on first arrival
                    if len(finished_racers) == 1:
                        self.on_winner_crossed(racer)

            # Fade fx layer periodically to keep clean
            if frame_count % 15 == 0:
                self.fx_drawer.clear()

            self.screen.update()
            time.sleep(0.018)  # ~55-60 FPS smooth animation

        self.race_in_progress = False
        return finished_racers

    def on_winner_crossed(self, winner):
        """Trigger celebratory sound, commentary, and confetti blast."""
        user_won = (winner.id == self.selected_racer_id)
        self.sound.play("win" if user_won else "lose")

        # Confetti blast at finish line
        self.launch_confetti()

    def launch_confetti(self):
        """Draw a festive particle burst around the finish line."""
        colors = ["#f1c40f", "#e74c3c", "#2ecc71", "#3498db", "#9b59b6", "#e67e22", "#ffffff"]
        for _ in range(35):
            cx = FINISH_X + random.randint(-40, 50)
            cy = random.randint(TRACK_BOTTOM + 20, TRACK_TOP - 20)
            self.fx_drawer.goto(cx, cy)
            self.fx_drawer.color(random.choice(colors))
            self.fx_drawer.dot(random.randint(5, 11))

    # --------------------------------------------------------------------------
    #                           PODIUM & RESULTS
    # --------------------------------------------------------------------------

    def display_results(self, finished_racers):
        """Display podium ceremony, profit calculations, and replay prompt."""
        winner = finished_racers[0]
        user_won = (winner.id == self.selected_racer_id)

        # Economic calculation
        if user_won:
            payout = int(self.current_bet * winner.odds)
            profit = payout - self.current_bet
            self.wallet += profit
            self.win_streak += 1
            self.total_races_won += 1
        else:
            self.wallet -= self.current_bet
            self.win_streak = 0
            profit = -self.current_bet

        # Semi-transparent Result Card
        card_w = 540
        card_h = 240
        cx = -card_w / 2
        cy = -card_h / 2

        self.banner_drawer.clear()
        self.banner_drawer.goto(cx, cy)
        self.banner_drawer.color("#1a252f" if not user_won else "#1b3a2a")
        self.banner_drawer.begin_fill()
        for _ in range(2):
            self.banner_drawer.forward(card_w)
            self.banner_drawer.left(90)
            self.banner_drawer.forward(card_h)
            self.banner_drawer.left(90)
        self.banner_drawer.end_fill()

        # Border
        self.banner_drawer.pensize(3)
        self.banner_drawer.color(ACCENT_GREEN if user_won else ACCENT_RED)
        self.banner_drawer.goto(cx, cy)
        self.banner_drawer.pendown()
        for _ in range(2):
            self.banner_drawer.forward(card_w)
            self.banner_drawer.left(90)
            self.banner_drawer.forward(card_h)
            self.banner_drawer.left(90)
        self.banner_drawer.penup()
        self.banner_drawer.pensize(1)

        # Header Text
        self.banner_drawer.color(ACCENT_GREEN if user_won else ACCENT_RED)
        self.banner_drawer.goto(0, cy + card_h - 40)
        header_msg = "🎉  VICTORY! YOUR TURTLE WON!  🎉" if user_won else "💀  RACE OVER - YOU LOST  💀"
        self.banner_drawer.write(header_msg, align="center", font=("Courier", 18, "bold"))

        # Payout Summary
        self.banner_drawer.color(TEXT_PRIMARY)
        self.banner_drawer.goto(0, cy + card_h - 75)
        res_summary = (
            f"Profit: +{profit} Coins  |  Balance: {self.wallet} Coins"
            if user_won
            else f"Loss: -{self.current_bet} Coins  |  Balance: {self.wallet} Coins"
        )
        self.banner_drawer.write(res_summary, align="center", font=("Arial", 13, "bold"))

        # Top 3 Podium Standings
        self.banner_drawer.color(ACCENT_GOLD)
        self.banner_drawer.goto(0, cy + card_h - 110)
        p1 = finished_racers[0]
        p2 = finished_racers[1]
        p3 = finished_racers[2]
        self.banner_drawer.write(
            f"🥇 1st: {p1.name} ({p1.finish_time}s)   🥈 2nd: {p2.name}   🥉 3rd: {p3.name}",
            align="center",
            font=("Courier", 12, "bold"),
        )

        # Stimulus / Bankruptcy Check
        if self.wallet <= 0:
            self.wallet = 50
            self.banner_drawer.color(ACCENT_GOLD)
            self.banner_drawer.goto(0, cy + card_h - 150)
            self.banner_drawer.write(
                "💸 BANKRUPT! Commission granted +50 emergency coins!",
                align="center",
                font=("Arial", 11, "italic"),
            )

        # Next Race Instructions
        self.banner_drawer.color(TEXT_MUTED)
        self.banner_drawer.goto(0, cy + 25)
        self.banner_drawer.write(
            "Press [SPACE] or Click to Start Next Round  •  Press [Q] to Quit",
            align="center",
            font=("Arial", 11, "bold"),
        )

        # Keep current bet within wallet limits
        if self.current_bet > self.wallet:
            self.current_bet = max(5, self.wallet)

        self.round_num += 1
        self.render_hud()
        self.screen.update()

    # --------------------------------------------------------------------------
    #                           MAIN GAME ORCHESTRATION
    # --------------------------------------------------------------------------

    def run(self):
        """Master game loop maintaining persistent rounds and state."""
        try:
            # Draw static track once
            draw_race_track(self.track_drawer)

            while self.is_running:
                # Reset racers to starting line
                for racer in self.racers:
                    racer.reset_position()

                self.fx_drawer.clear()
                self.banner_drawer.clear()
                self.show_commentary("🏁 Championship Open! Select your turtle & place your bet.")
                self.render_hud()
                self.screen.update()

                # Await player starting signal (Space, Enter, or Click)
                self.waiting_for_input = True
                self.start_race_flag = False

                while not self.start_race_flag and self.is_running:
                    self.screen.update()
                    time.sleep(0.03)

                if not self.is_running:
                    break

                self.waiting_for_input = False
                self.banner_drawer.clear()

                # Countdown
                self.show_commentary("🚦 RACERS TO YOUR MARKS...", ACCENT_GOLD)
                self.perform_countdown()

                # Run Race
                finished_racers = self.run_race_loop()

                # Announce & Podium
                self.display_results(finished_racers)

                # Wait for player to proceed to next race
                self.waiting_for_input = True
                self.start_race_flag = False

                while not self.start_race_flag and self.is_running:
                    self.screen.update()
                    time.sleep(0.03)

        except (turtle.Terminator, Exception) as e:
            # Clean exit on window closure
            pass


# ==============================================================================
#                                ENTRY POINT
# ==============================================================================

def main():
    game = TurtleGrandPrix()
    game.run()


if __name__ == "__main__":
    main()