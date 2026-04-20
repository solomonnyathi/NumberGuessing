from py_compile import main
import random
import sys

DIFFICULTIES = {
    "1": ("EASY", 1 , 50 , 8), # Level 1: guess a number between 1 and 50, 8 tries
    "2": ("MEDIUM", 1 , 100 , 10), # Level 2: guess a number between 1 and 100, 10 tries
    "3": ("HARD", 1 , 200 , 12) # Level 3: guess a number between 1 and 200, 12 tries
}

def hot_cold_hit(guess: int, secret: int, last_distance: int | float | None) -> tuple[str, int]:
    distance = abs(guess - secret)
    if distance == 0:
        return "you got it right!", 0.0
    if last_distance is not None:
        if distance < last_distance:
            trend = "getting warmer!"
        elif distance > last_distance:
            trend = "getting colder!"
        else:
            trend = "same distance - try a different number!"
        return trend, distance
    
    if distance <= 5:
        return "burning hot!", distance # very close
    elif distance <= 15: 
        return "hot!", distance # close
    elif distance <= 40:
        return "cool!", distance # far away
    else:
        return "cold!", distance # very far away
            
def choose_difficulty() -> tuple[str, int, int, int]:
    print("Choose a difficulty level:")
    print("1. EASY (1-50, 8 tries)")
    print("2. MEDIUM (1-100, 10 tries)")
    print("3. HARD (1-200, 12 tries)")
    
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    if choice not in DIFFICULTIES:
        print("Invalid choice. Please select 1, 2, or 3.")
        choice = "1"
    
    label, low, high, max_tries = DIFFICULTIES[choice]
    return label, low, high, max_tries

def play_round(name: str, low: int, high: int, max_tries: int) -> bool:
    secret = random.randint(low, high)
    last_distance : float | None = None
    guess_left = max_tries
    try_number = 0
    
    print (f" I am thinking of a number between {low} and {high}. You have {max_tries} tries to guess it. Good luck, {name}!")
    while guess_left > 0:
        try_number += 1
        raw = input(f"Try {try_number} ({guess_left} left): ").strip()
        
        try:
            guess = int(raw)
        except ValueError:
            try_number -= 1
            print("Invalid input. Please enter a valid integer.")
            continue
            
        if guess < low or guess > high:
            try_number -= 1
            print(f"Please enter a number between {low} and {high}.")
            continue

        if guess == secret:
            print(f"Congratulations, {name}! You guessed the number {secret} in {try_number} tries!")
            return True
        
        guess_left -= 1
        hint, last_distance = hot_cold_hit(guess, secret, last_distance)
        print(f"Hint: {hint}")
        
        if guess_left == 0:
            print(f"Sorry, {name}. You've used all your tries. The secret number was {secret}. Better luck next time!")
            return False
        
def main() -> None:
    name = input("Hi there, what is your name? ").strip()
    if not name:
        name = "Player"
    streak = 0
    best_streak = 0
    
    while True:
        label, low, high, max_tries = choose_difficulty()
        if play_round(name, low, high, max_tries):
            streak += 1
            best_streak = max(streak, best_streak)
            print(f"Current streak: {streak}. Best streak: {best_streak}.")
        else:
            streak = 0
            print(f"Current streak reset to 0. Best streak: {best_streak}.")
             
        play_again = input("Do you want to play again? (yes/no) ").strip().lower()
        if play_again != "yes":
            print(f"Thanks for playing, {name}! Your best streak was {best_streak}. Goodbye!")
            break

if __name__ == "__main__":
    main()