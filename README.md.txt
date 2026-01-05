🪨📄✂️ Rock Paper Scissors (CLI)

A feature-rich command-line Rock Paper Scissors game written in Python.
Play against the computer in rounds or best-of mode, earn points, track all-time statistics, and view win-rate percentages across sessions.

✨ Features

Interactive CLI menu

Two play modes:

Rounds (fixed number of rounds)

Best-of (first to majority wins)

Random computer choices

Persistent score & stats (saved locally)

Series win-rate percentages

All-time win-rate percentages

Configurable rewards and messages

Demo mode

Help / Q&A system

📜 Rules

Choose one of: rock, paper, scissors

Rock beats scissors

Scissors beats paper

Paper beats rock

Same choice results in a draw

🎮 Game Modes
🔁 Rounds Mode

Play a fixed number of rounds.

All rounds are played.

Final series results and percentages are shown.

🏆 Best-Of Mode

Choose an odd number (e.g. 3, 5).

First player to reach the majority of wins wins the series.

Draws do not count toward wins.

▶️ How to Play

Run the game:

python main_rock_paper_scissors_demo.py


You’ll see the main menu:

=== Welcome to Rock Paper Scissors! ===
What would you like to do?
  1) play   - Start a friendly series of rounds
  2) demo   - Watch a short demo (random moves)
  3) score  - View your points and all-time stats
  4) config - Change reward amounts and messages
  5) reset  - Reset your points and stats
  6) quit   - Exit the game
  7) help   - Ask a quick question

🧮 Example Gameplay Output
Round 2/5 - Your choice (rock/paper/scissors): rock
You chose rock, computer chose scissors. Result: win

📊 Series Summary & Percentages

After a series ends:

--- Series Summary ---
You 3 - Computer 1 (Draws: 1)
Series percentages: You: 60.00%   Computer: 20.00%   Draws: 20.00%

--- All-time ---
Points: 230 | Rounds: 12 | You: 50.00% | Computer: 33.33% | Draws: 16.67%

🎉 You won the series! Reward: 100 points. Total: 230


Percentages are calculated using:

Series results

All-time results (rounds_played)

💾 Persistent Stats

Stats are saved automatically in:

~/.rps/
 ├── config.json
 └── score.json


Tracked values:

Player wins

Computer wins

Draws

Rounds played

Total points

Stats persist even after closing the game.

⚙️ Configuration

You can customize:

Win reward

Tie reward

Lose reward

Win / tie / lose messages

From the menu:

config - Change reward amounts and messages

🧪 Demo Mode

Demo mode plays a single decisive round automatically:

Running automated demo (single decisive outcome)
Demo outcome: You rock vs Computer scissors -> win


Rewards and stats are applied normally.

❓ Help System

Ask natural questions like:

how do I win
what are the rules
how are points awarded


Or type help from the menu.

🛠️ Technologies Used

Python 3

Standard library only (random, json, pathlib)

📄 License

Open-source and free to use for learning and personal projects.