"""Simple Rock Paper Scissors library and CLI.

Usage:
- Import `decide(player, computer)` from `rps.rps` for programmatic use.
- Run the CLI with `python -m rps`.
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, Tuple

CHOICES: Tuple[str, ...] = ("rock", "paper", "scissors")
_WIN_MATRIX = {
    ("rock", "scissors"): True,
    ("scissors", "paper"): True,
    ("paper", "rock"): True,
}

DATA_DIR = Path.home() / ".rps"
CONFIG_PATH = DATA_DIR / "config.json"
SCORE_PATH = DATA_DIR / "score.json"

DEFAULT_CONFIG: Dict[str, object] = {
    "win_reward": 100,
    "lose_reward": 10,
    "tie_reward": 20,
    "win_message": "🎉 You won the series!",
    "lose_message": "😞 You lost the series.",
    "tie_message": "🤝 The series is a tie.",
}


def decide(player: str, computer: str) -> str:
    """Decide the outcome from the player's perspective: 'win', 'lose' or 'draw'.

    Both inputs are normalized (strip + lower). Raises ValueError for invalid choices.
    """
    p = player.strip().lower()
    c = computer.strip().lower()
    if p not in CHOICES or c not in CHOICES:
        raise ValueError("Choices must be one of: rock, paper, scissors")
    if p == c:
        return "draw"
    return "win" if _WIN_MATRIX.get((p, c), False) else "lose"


def random_choice() -> str:
    return random.choice(CHOICES)


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, object]:
    ensure_data_dir()
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            # restore defaults on error
            save_config(DEFAULT_CONFIG)
            return dict(DEFAULT_CONFIG)
    save_config(DEFAULT_CONFIG)
    return dict(DEFAULT_CONFIG)


def save_config(conf: Dict[str, object]) -> None:
    ensure_data_dir()
    CONFIG_PATH.write_text(json.dumps(conf, indent=2))


def load_stats() -> Dict[str, int]:
    ensure_data_dir()
    default = {
        "points": 0,
        "player_wins": 0,
        "computer_wins": 0,
        "draws": 0,
        "rounds_played": 0,
    }
    if SCORE_PATH.exists():
        try:
            data = json.loads(SCORE_PATH.read_text())
            for k, v in default.items():
                data.setdefault(k, v)
            # ensure ints
            return {k: int(data.get(k, v)) for k, v in default.items()}
        except Exception:
            save_stats(default)
            return dict(default)
    save_stats(default)
    return dict(default)


def save_stats(stats: Dict[str, int]) -> None:
    ensure_data_dir()
    SCORE_PATH.write_text(json.dumps(stats, indent=2))


def load_score() -> int:
    return int(load_stats().get("points", 0))


def save_score(points: int) -> None:
    stats = load_stats()
    stats["points"] = int(points)
    save_stats(stats)


def award_points(points: int) -> int:
    stats = load_stats()
    stats["points"] = stats.get("points", 0) + int(points)
    save_stats(stats)
    return stats["points"]


def update_stats(player_wins: int, computer_wins: int, draws: int, rounds_played: int) -> None:
    stats = load_stats()
    stats["player_wins"] = stats.get("player_wins", 0) + int(player_wins)
    stats["computer_wins"] = stats.get("computer_wins", 0) + int(computer_wins)
    stats["draws"] = stats.get("draws", 0) + int(draws)
    stats["rounds_played"] = stats.get("rounds_played", 0) + int(rounds_played)
    save_stats(stats)


def format_pct(part: int, total: int) -> str:
    if int(total) <= 0:
        return "0.00%"
    return f"{(int(part) / int(total) * 100):.2f}%"


def alltime_percentages() -> Dict[str, object]:
    s = load_stats()
    total = s.get("rounds_played", 0)
    return {
        "you": format_pct(s.get("player_wins", 0), total),
        "computer": format_pct(s.get("computer_wins", 0), total),
        "draws": format_pct(s.get("draws", 0), total),
        "rounds": str(total),
        "points": str(s.get("points", 0)),
    }


def answer_question(q: str) -> None:
    ql = q.strip().lower()
    if any(k in ql for k in ("help", "h")):
        print("\nYou can ask questions like:")
        print("  - 'how do I win' (tips and rules)")
        print("  - 'what are the rules' (game rules)")
        print("  - 'how are points awarded' (rewards and scoring)")
        print("Or type 'play' to start, 'score' to view points, or 'config' to change rewards.\n")
        return
    if "how" in ql and "win" in ql:
        print("\nTips to win:")
        print("  - Rock beats scissors, scissors beats paper, and paper beats rock.")
        print("  - There's no guaranteed move against a random opponent, but looking for patterns can help.")
        print("  - Play enough rounds to let statistics matter; your all-time percentages are tracked under 'score'.\n")
        return
    if any(k in ql for k in ("rules", "what", "rule")):
        print("\nRules:")
        print("  - Each round, choose 'rock', 'paper' or 'scissors'.")
        print("  - Rock beats scissors, scissors beats paper, paper beats rock. Same move is a draw.\n")
        return
    if any(k in ql for k in ("point", "reward")):
        conf = load_config()
        print("\nRewards:")
        print(f"  - Win a series: {conf.get('win_reward', 100)} points")
        print(f"  - Tie a series: {conf.get('tie_reward', 20)} points")
        print(f"  - Lose a series: {conf.get('lose_reward', 10)} points")
        print("You can change these under 'config'.\n")
        return
    print("\nSorry, I don't know that one. Try: 'how do I win', 'what are the rules', 'how are points awarded', or type 'help' to see more options.\n")


def play_series(rounds: int) -> Tuple[int, int, int]:
    player_wins = computer_wins = draws = 0
    for r in range(1, rounds + 1):
        try:
            player = input(f"Round {r}/{rounds} - Your choice (rock/paper/scissors): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye — thanks for playing!")
            return player_wins, computer_wins, draws
        if player in ("quit", "q", "exit"):
            print("Series ended early — returning to the main menu.")
            return player_wins, computer_wins, draws
        if player not in CHOICES:
            print("Invalid choice; try again.")
            continue
        computer = random_choice()
        result = decide(player, computer)
        if result == "win":
            player_wins += 1
        elif result == "lose":
            computer_wins += 1
        else:
            draws += 1
        print(f"You chose {player}, computer chose {computer}. Result: {result}")
    return player_wins, computer_wins, draws


def play_best_of(n: int) -> Tuple[int, int, int, int]:
    needed = n // 2 + 1
    player_wins = computer_wins = draws = rounds_played = 0
    r = 0
    while player_wins < needed and computer_wins < needed and r < n:
        r += 1
        rounds_played += 1
        try:
            player = input(f"Round {r}/{n} - Your choice (rock/paper/scissors): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye — thanks for playing!")
            return player_wins, computer_wins, draws, rounds_played
        if player in ("quit", "q", "exit"):
            print("Series ended early — returning to the main menu.")
            return player_wins, computer_wins, draws, rounds_played
        if player not in CHOICES:
            print("Invalid choice; try again.")
            continue
        computer = random_choice()
        result = decide(player, computer)
        if result == "win":
            player_wins += 1
        elif result == "lose":
            computer_wins += 1
        else:
            draws += 1
        print(f"You chose {player}, computer chose {computer}. Result: {result}")
    return player_wins, computer_wins, draws, rounds_played


def interactive_config() -> None:
    conf = load_config()
    print("Current configuration:")
    for k, v in conf.items():
        print(" ", k, ":", v)
    print("Press Enter to keep the current value.")
    try:
        win = input(f"win_reward (current={conf['win_reward']}): ").strip()
        tie = input(f"tie_reward (current={conf['tie_reward']}): ").strip()
        lose = input(f"lose_reward (current={conf['lose_reward']}): ").strip()
        win_msg = input(f"win_message (current={conf['win_message']}): ").strip()
        tie_msg = input(f"tie_message (current={conf['tie_message']}): ").strip()
        lose_msg = input(f"lose_message (current={conf['lose_message']}): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        return
    if win and win.isdigit():
        conf['win_reward'] = int(win)
    elif win:
        print('Invalid win_reward; keeping current value.')
    if tie and tie.isdigit():
        conf['tie_reward'] = int(tie)
    elif tie:
        print('Invalid tie_reward; keeping current value.')
    if lose and lose.isdigit():
        conf['lose_reward'] = int(lose)
    elif lose:
        print('Invalid lose_reward; keeping current value.')
    if win_msg:
        conf['win_message'] = win_msg
    if tie_msg:
        conf['tie_message'] = tie_msg
    if lose_msg:
        conf['lose_message'] = lose_msg
    save_config(conf)
    print('Configuration saved.')


def handle_series_result(p_w: int, c_w: int, d: int, rounds_played: int) -> None:
    conf = load_config()
    print('\n--- Series Summary ---')
    print(f"You {p_w} - Computer {c_w} (Draws: {d})")
    print(f"Series percentages: You: {format_pct(p_w, rounds_played)}   Computer: {format_pct(c_w, rounds_played)}   Draws: {format_pct(d, rounds_played)}")
    at = alltime_percentages()
    print('\n--- All-time ---')
    print(f"Points: {at['points']} | Rounds: {at['rounds']} | You: {at['you']} | Computer: {at['computer']} | Draws: {at['draws']}\n")
    if p_w > c_w:
        pts = int(conf.get('win_reward', 100))
        new_total = award_points(pts)
        print(conf.get('win_message', 'You won!'), f"Reward: {pts} points. Total: {new_total}")
        return
    if p_w < c_w:
        pts = int(conf.get('lose_reward', 10))
        new_total = award_points(pts)
        print(conf.get('lose_message', 'You lost.'), f"Consolation: {pts} points. Total: {new_total}")
        return
    pts = int(conf.get('tie_reward', 20))
    new_total = award_points(pts)
    print(conf.get('tie_message', 'Tie.'), f"Shared reward: {pts} points. Total: {new_total}")


def demo_run() -> None:
    """Run a short demo that shows a single decisive outcome (win or lose).

    This picks random moves until a non-draw occurs (bounded attempts), then
    updates stats and awards the appropriate reward while printing a concise
    message.
    """
    print('Running automated demo (single decisive outcome)')
    max_attempts = 10
    p_w = c_w = d = 0
    player = computer = None
    result = 'draw'
    for _ in range(max_attempts):
        player = random_choice()
        computer = random_choice()
        result = decide(player, computer)
        if result in ('win', 'lose'):
            break
    else:
        # Fallback: force a win scenario
        player, computer, result = 'rock', 'scissors', 'win'
    # Print concise outcome
    print(f"Demo outcome: You {player} vs Computer {computer} -> {result}")
    # Update stats and award points for a single decisive round
    rounds_played = 1
    if result == 'win':
        p_w = 1
        c_w = 0
    else:
        p_w = 0
        c_w = 1
    d = 0
    update_stats(p_w, c_w, d, rounds_played)
    conf = load_config()
    if p_w > c_w:
        pts = int(conf.get('win_reward', 100))
        new_total = award_points(pts)
        print(conf.get('win_message', 'You won!'), f"Reward: {pts} points. Total: {new_total}")
    else:
        pts = int(conf.get('lose_reward', 10))
        new_total = award_points(pts)
        print(conf.get('lose_message', 'You lost.'), f"Consolation: {pts} points. Total: {new_total}")


def print_menu() -> None:
    print('\n=== Welcome to Rock Paper Scissors! ===')
    print('What would you like to do?')
    print("  1) play   - Start a friendly series of rounds")
    print("  2) demo   - Watch a short demo (random moves)")
    print("  3) score  - View your points and all-time stats")
    print("  4) config - Change reward amounts and messages")
    print("  5) reset  - Reset your points and stats")
    print("  6) quit   - Exit the game")
    print("  7) help   - Ask a quick question (e.g., 'how do I win')")


def main() -> None:
    print_menu()
    conf = load_config()
    while True:
        try:
            action = input("What would you like to do? ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye")
            return
        num_map = {
            '1': 'play', 'play': 'play', '2': 'demo', 'demo': 'demo', '3': 'score', 'score': 'score',
            '4': 'config', 'config': 'config', '5': 'reset', 'reset': 'reset', '6': 'quit', 'quit': 'quit',
            '7': 'help', 'help': 'help'
        }
        if action in num_map:
            action = num_map[action]
        if action in ('help',) or action.startswith(('how', 'what', 'why', 'where', 'when')) or '?' in action:
            answer_question(action)
            continue
        if action in ('quit', 'q', 'exit'):
            print('\nGoodbye')
            return
        if action in ('score', 's'):
            at = alltime_percentages()
            print('\n--- Your Stats ---')
            print('Points: ' + at['points'])
            print('Rounds played: ' + at['rounds'])
            print('You: ' + at['you'] + '   Computer: ' + at['computer'] + '   Draws: ' + at['draws'])
            print('\n')
            continue
        if action == 'reset':
            save_stats({'points': 0, 'player_wins': 0, 'computer_wins': 0, 'draws': 0, 'rounds_played': 0})
            print('\nAll set — your points and stats are now reset. Good luck!\n')
            print_menu()
            continue
        if action == 'config':
            interactive_config()
            conf = load_config()
            print_menu()
            continue
        if action == 'demo':
            demo_run()
            print()
            print_menu()
            continue
        if action == 'play':
            mode = input("Play mode ('rounds' or 'best-of'): ").strip().lower()
            if mode in ('quit', 'q', 'exit'):
                continue
            mode_clean = ''.join(ch for ch in mode if ch.isalpha())
            if mode_clean.startswith('r'):
                chosen_mode = 'rounds'
            elif mode_clean.startswith('b'):
                chosen_mode = 'bestof'
            else:
                print("Please enter 'rounds' or 'best-of'.")
                continue
            if chosen_mode == 'rounds':
                rounds_input = input('How many rounds would you like to play? Enter a whole number (e.g., 3): ').strip()
                if rounds_input in ('quit', 'q', 'exit'):
                    print('Cancelled — returning to the main menu.')
                    continue
                if not rounds_input.isdigit() or int(rounds_input) <= 0:
                    print('Please enter a whole number greater than zero.')
                    continue
                rounds = int(rounds_input)
                p_w, c_w, d = play_series(rounds)
                rounds_played = p_w + c_w + d
                handle_series_result(p_w, c_w, d, rounds_played)
                last_mode, last_param = 'rounds', rounds
            else:
                n_input = input('Best-of N — enter an odd number (e.g., 3 or 5): ').strip()
                if n_input in ('quit', 'q', 'exit'):
                    print('Cancelled — returning to the main menu.')
                    continue
                if not n_input.isdigit():
                    print('Please enter a positive integer.')
                    continue
                n = int(n_input)
                if n <= 0:
                    print('Number must be greater than zero.')
                    continue
                if n % 2 == 0:
                    print("Please enter an odd number (e.g., 3 or 5) so there's a clear winner.")
                    continue
                p_w, c_w, d, rounds_played = play_best_of(n)
                handle_series_result(p_w, c_w, d, rounds_played)
                last_mode, last_param = 'bestof', n
            # post-series loop to play again / change number omitted for brevity
            continue
        print("Invalid input; type 'play', 'demo', 'score', 'config', 'reset' or 'quit'.")


if __name__ == '__main__':
    main()
