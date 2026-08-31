import turtle
import random
import time

# ========================== CONSTANTS ==========================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
TRACK_LEFT = -420
TRACK_RIGHT = 400
FINISH_X = 380
NUM_RACERS = 6
COLORS = ["red", "blue", "green", "yellow", "purple", "orange"]
COLOR_NAMES = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
Y_POSITIONS = [-150, -90, -30, 30, 90, 150]

# ========================== DRAWING HELPERS ==========================


def create_drawer():
    """Create a hidden turtle used only for drawing."""
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    return t


def draw_track(drawer):
    """Draw the race track background, lane lines, and finish line."""
    # --- Track background ---
    drawer.goto(TRACK_LEFT - 30, -200)
    drawer.color("#2c3e50")
    drawer.begin_fill()
    for _ in range(2):
        drawer.forward(TRACK_RIGHT - TRACK_LEFT + 80)
        drawer.left(90)
        drawer.forward(400)
        drawer.left(90)
    drawer.end_fill()

    # --- Lane dividers (dashed) ---
    drawer.pensize(1)
    drawer.color("#4a6274")
    for y in [-180, -120, -60, 0, 60, 120, 180]:
        drawer.goto(TRACK_LEFT - 20, y)
        drawer.pendown()
        for _ in range(40):
            drawer.forward(6)
            drawer.penup()
            drawer.forward(6)
            drawer.pendown()
        drawer.penup()

    # --- Finish line (checkered pattern) ---
    square_size = 14
    cols = 2
    rows = int(400 / square_size)
    for row in range(rows):
        for col in range(cols):
            x = FINISH_X + col * square_size
            y = -200 + row * square_size
            if (row + col) % 2 == 0:
                drawer.color("white")
            else:
                drawer.color("black")
            drawer.goto(x, y)
            drawer.begin_fill()
            for _ in range(4):
                drawer.forward(square_size)
                drawer.left(90)
            drawer.end_fill()

    # --- Start line ---
    drawer.color("white")
    drawer.pensize(3)
    drawer.goto(TRACK_LEFT, -200)
    drawer.pendown()
    drawer.goto(TRACK_LEFT, 200)
    drawer.penup()
    drawer.pensize(1)


def draw_lane_labels(drawer):
    """Draw color labels on the left side of each lane."""
    drawer.color("white")
    for i, name in enumerate(COLOR_NAMES):
        drawer.goto(TRACK_LEFT - 95, Y_POSITIONS[i] - 10)
        drawer.write(name, align="center", font=("Courier", 11, "bold"))


def draw_title(drawer):
    """Draw the game title at the top of the screen."""
    drawer.color("#f1c40f")
    drawer.goto(0, 250)
    drawer.write(
        "🐢  TURTLE  RACING  🐢",
        align="center",
        font=("Courier", 30, "bold"),
    )
    drawer.color("#bdc3c7")
    drawer.goto(0, 225)
    drawer.write(
        "Place your bet and watch them go!",
        align="center",
        font=("Arial", 12, "italic"),
    )


# ========================== GAME LOGIC ==========================


def create_racers():
    """Create and position all racer turtles."""
    racers = []
    for i in range(NUM_RACERS):
        racer = turtle.Turtle(shape="turtle")
        racer.shapesize(1.5, 1.5)
        racer.color(COLORS[i])
        racer.penup()
        racer.goto(TRACK_LEFT, Y_POSITIONS[i])
        racers.append(racer)
    return racers


def get_user_bet(screen):
    """Ask the user to place a bet via a dialog box."""
    bet = None
    while bet not in COLORS:
        bet = screen.textinput(
            "🐢 Place Your Bet!",
            "Which turtle will win the race?\n\n"
            "Choose a color:\n"
            "  red | blue | green\n"
            "  yellow | purple | orange\n",
        )
        if bet is None:
            # User cancelled — default to random
            bet = random.choice(COLORS)
        bet = bet.strip().lower()
    return bet


def show_bet(drawer, bet):
    """Display the user's bet on screen."""
    drawer.goto(0, -240)
    drawer.color("white")
    drawer.write(
        f"Your bet: {bet.upper()}",
        align="center",
        font=("Courier", 14, "bold"),
    )


def countdown(drawer):
    """Show a 3-2-1-GO countdown on screen."""
    messages = ["3", "2", "1", "🏁 GO!"]
    colors = ["#e74c3c", "#f39c12", "#2ecc71", "#00ff88"]
    for i, msg in enumerate(messages):
        drawer.goto(0, -10)
        drawer.color(colors[i])
        drawer.write(msg, align="center", font=("Courier", 50, "bold"))
        time.sleep(0.6)
        # Clear the countdown text
        drawer.color("#2c3e50")
        drawer.goto(-60, -15)
        drawer.begin_fill()
        for _ in range(2):
            drawer.forward(120)
            drawer.left(90)
            drawer.forward(70)
            drawer.left(90)
        drawer.end_fill()


def run_race(racers):
    """Run the race loop and return the winning turtle's color."""
    while True:
        for racer in racers:
            distance = random.randint(1, 10)
            racer.forward(distance)

            if racer.xcor() >= FINISH_X:
                return racer.pencolor()


def announce_winner(drawer, winner, user_bet):
    """Display the race result on screen."""
    won = winner == user_bet

    # Clear bet text area
    drawer.color("#2c3e50")
    drawer.goto(-250, -260)
    drawer.begin_fill()
    for _ in range(2):
        drawer.forward(500)
        drawer.left(90)
        drawer.forward(50)
        drawer.left(90)
    drawer.end_fill()

    # Result banner background
    banner_color = "#27ae60" if won else "#c0392b"
    drawer.color(banner_color)
    drawer.goto(-280, -20)
    drawer.begin_fill()
    for _ in range(2):
        drawer.forward(560)
        drawer.left(90)
        drawer.forward(100)
        drawer.left(90)
    drawer.end_fill()

    # Result text
    drawer.color("white")
    if won:
        drawer.goto(0, 45)
        drawer.write(
            "🎉  YOU  WIN!  🎉",
            align="center",
            font=("Courier", 28, "bold"),
        )
        drawer.goto(0, 5)
        drawer.write(
            f"The {winner.upper()} turtle crossed first!",
            align="center",
            font=("Arial", 14, "normal"),
        )
    else:
        drawer.goto(0, 45)
        drawer.write(
            "💀  YOU  LOST  💀",
            align="center",
            font=("Courier", 28, "bold"),
        )
        drawer.goto(0, 5)
        drawer.write(
            f"Winner: {winner.upper()}  |  Your bet: {user_bet.upper()}",
            align="center",
            font=("Arial", 14, "normal"),
        )

    # Replay prompt
    drawer.color("#bdc3c7")
    drawer.goto(0, -250)
    drawer.write(
        "Click anywhere to play again  •  Press 'Q' to quit",
        align="center",
        font=("Arial", 11, "italic"),
    )


# ========================== MAIN ==========================


def main():
    """Set up screen and run the game loop."""
    screen = turtle.Screen()
    screen.title("🐢 Turtle Racing Game")
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.bgcolor("#1a252f")
    screen.tracer(0)  # Manual screen updates for speed

    try:
        while True:
            screen.clear()
            screen.bgcolor("#1a252f")
            screen.tracer(0)

            drawer = create_drawer()

            # Draw environment
            draw_track(drawer)
            draw_lane_labels(drawer)
            draw_title(drawer)
            screen.update()

            # Get user bet
            user_bet = get_user_bet(screen)
            show_bet(drawer, user_bet)
            screen.update()

            # Create racers & countdown
            racers = create_racers()
            screen.update()
            screen.tracer(1)  # Turn on animation for countdown
            countdown(drawer)
            screen.tracer(0)

            # Run race with visible animation
            winner = None
            while winner is None:
                for racer in racers:
                    distance = random.randint(1, 5)
                    racer.forward(distance)
                    if racer.xcor() >= FINISH_X:
                        winner = racer.pencolor()
                        break
                screen.update()
                time.sleep(0.03)  # ~30ms per frame for a smooth, visible race

            # Announce result
            screen.tracer(1)
            announce_winner(drawer, winner, user_bet)
            screen.update()

            # Wait for replay or quit
            replay = [False]
            quit_game = [False]

            def on_click(x, y):
                replay[0] = True

            def on_quit():
                quit_game[0] = True

            screen.onclick(on_click)
            screen.onkeypress(on_quit, "q")
            screen.listen()

            # Wait for user decision
            while not replay[0] and not quit_game[0]:
                screen.update()
                time.sleep(0.05)

            screen.onclick(None)
            screen.onkeypress(None, "q")

            if quit_game[0]:
                break

        screen.bye()

    except turtle.Terminator:
        pass  # Window was closed by the user — exit silently


if __name__ == "__main__":
    main()