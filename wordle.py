# EC__ICTPRG302_Project_2025_S2
# Author: Edgard Corcovado
# Student ID: 20153680
# Course: Cert III in IT (Cybersecurity)
# Lecturer: Suchi Baria

# TODO: Add Import statements (if needed)
import random
import os

# Variables and Constants
# TODO: Define Constants
DEBUG = False # Set to True to run tests, False to play game
MAX_GUESSES = 6
WORD_LENGTH = 5
ALL_WORDS_FILE = "all_words.txt"
TARGET_WORDS_FILE = "target_words.txt"

# TODO: Define Variables 
# (No global variables needed)


# Application Functions

# TODO: Score Guess Function
def score_guess(guess, target):
    """Scores the guess word against the target word.

    Arguments
    ---------
    guess (str): The 5-letter word provided by the user.
    target (str): The 5-letter secret word.

    Returns
    -------
    list: A list of integers (0, 1, or 2) representing the score.
          0 = Incorrect letter
          1 = Correct letter, wrong position
          2 = Correct letter, correct position
    """
    score = [0] * len(target)
    target_letters = list(target) 

    # First pass: Check for exact matches (Score = 2)
    for i in range(len(target)):
        if guess[i] == target[i]:
            score[i] = 2
            target_letters[i] = None 

    # Second pass: Check for misplaced matches (Score = 1)
    for i in range(len(target)):
        if score[i] == 0: 
            if guess[i] in target_letters:
                score[i] = 1
                target_letters.remove(guess[i]) 
                
    return score

# TODO: Read File Into Word List Function
def read_words_from_file(filename):
    """Reads words from a text file into a list.

    Arguments
    ---------
    filename (str): The name of the file to read.

    Returns
    -------
    list: A list of words from the file. Returns an empty list
          if the file is not found or an error occurs.
    """
    word_list = []
    
    if not os.path.exists(filename):
        print(f"--- ERROR ---")
        print(f"Error: File '{filename}' not found.")
        print(f"Please ensure it is in the same directory as wordle.py")
        print(f"---------------")
        return [] 
        
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Add word, stripping whitespace and ensuring lowercase
                word_list.append(line.strip().lower())
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
        return [] 

    return word_list

# TODO: Display Greeting Function
def show_greeting():
    """Prints the game's welcome message."""
    print("==============================")
    print("      Welcome to Wordle!      ")
    print("==============================")
    print(f"Guess the {WORD_LENGTH}-letter word in {MAX_GUESSES} tries.\n")

# TODO: Display Instructions Function
def show_instructions():
    """Prints the scoring instructions for the player."""
    print("--- How to Play ---")
    print("Invalid words won't count as an attempt ❁´◡`❁")
    print("X = Correct letter, correct position")
    print("? = Correct letter, wrong position")
    print("- = Letter not in the word")
    print("Type 'help' to see these rules again.")
    print("Type 'exit' to quit the game anytime.\n")

# TODO: Any Optional Additional Functions 
def Random_Target_Word(word_list):
    """Selects a random word from a provided list."""
    if word_list:
        return random.choice(word_list)
    return None

def display_score(score, guess_word):
    """Displays the score (X, ?, -) and the guess word."""
    score_output = ""
    word_output = ""
    
    for position in range(len(score)):
        if score[position] == 0:
            score_output += "- "
        elif score[position] == 1:
            score_output += "? "
        elif score[position] == 2:
            score_output += "X "

    # Display the guess word in uppercase
    for position in range(len(guess_word)):
        word_output += guess_word[position].upper() + " "

    print(score_output)
    print(word_output)
    print() # Add a blank line for readability

# TODO: Play Game Function
def play_game():
    """Runs the main game loop for Wordle."""
    
    # --- 1. Setup ---
    show_greeting()
    show_instructions()
    
    all_word_list = read_words_from_file(ALL_WORDS_FILE)
    target_word_list = read_words_from_file(TARGET_WORDS_FILE)
    
    # Check that files loaded successfully
    if not all_word_list or not target_word_list:
        print("Could not load word files. Exiting game.")
        return # Exit the function
        
    target_word = Random_Target_Word(target_word_list)
    
    # Uncomment the line below for easy testing
    # print(f"(DEBUG: Target word is {target_word})")
    
    guess_count = 0
    has_won = False
    
    # --- 2. Main Game Loop (Repetition) ---
    while guess_count < MAX_GUESSES and not has_won:
        guess_number = guess_count + 1
        print(target_word)
        
        # Get User Input
        # .lower().strip() ensures all input is case insensitive (EXIT = exit, Help = help)
        guess_word = input(f"Attempt used: {guess_number}/{MAX_GUESSES} \nEnter a word:").lower().strip()
        #print(f"Attempt used: {guess_number}/{MAX_GUESSES}")
        
        # --- COMMAND CHECK: Exit ---
        if guess_word == "exit":
            print("Game exited. Thanks for playing!")
            return # Stops the function immediately
            
        # --- COMMAND CHECK: Help ---
        if guess_word == "help":
            show_instructions()
            continue # Skips the rest of the loop, does NOT count as a guess
        
        # --- 3. Input Validation (Selection) ---
        
        # Check 1: Is it the right length?
        if len(guess_word) != WORD_LENGTH:
            print(f"Invalid guess. Word must be {WORD_LENGTH} letters long. Try again.\n")
            continue # Skip to next loop iteration
            
        # Check 2: Is it a valid word?
        if guess_word not in all_word_list:
            print("Invalid guess. Not in the word list. Try again.\n")
            continue
            
        # --- 4. Process Valid Guess ---
        guess_count += 1
        
        # Score the guess
        score = score_guess(guess_word, target_word)
        
        # Display score
        display_score(score, guess_word)
        
        # Check for win (Selection)
        if guess_word == target_word:
            has_won = True
            
    # --- 5. End of Game ---
    if has_won:
        print(f"Congratulations! You guessed the word '{target_word.upper()}' in {guess_count} tries!")
    else:
        print("Game Over. You ran out of guesses.")
        print(f"The word was '{target_word.upper()}'.")

    print("\nThanks for playing!")


#TODO: Testing Function
def test_game():
    """Runs all test cases for the game functions."""
    print("--- RUNNING TESTS ---")
    
    # Test Case 1
    print("\n--- Test Case 1 ---")
    ##Arrange
    guess_word = "hello"
    target_word = "train"
    ##Act
    score = score_guess(guess_word, target_word)
    ##Assert
    print("Score:", score, "Expected:", [0, 0, 0, 0, 0])
    
    # Test Case 2
    print("\n--- Test Case 2 ---")
    ##Arrange
    guess_word = "hello"
    target_word = "hello"
    ##Act
    score = score_guess(guess_word, target_word)
    ##Assert
    print("Score:", score, "Expected:", [2, 2, 2, 2, 2])
    
    # Test Case 3
    print("\n--- Test Case 3 ---")
    # TODO: set guess word to "world"
    guess_word = "world"
    # TODO: set target word to "hello"
    target_word = "hello"
    # TODO: set score to score guess (guess word and target word)
    score = score_guess(guess_word, target_word)
    # TODO: display the score
    print("Score:", score, "Expected:", [0, 1, 0, 2, 0])
    
    # Test Case 4
    print("\n--- Test Case 4 ---")
    ## Arrange
    all_word_filename = "all_words.txt"
    ## Act
    all_word_list = read_words_from_file(all_word_filename)
    ## Assert
    print("Got:", all_word_list[:5], "Expected:", ['aahed', 'aalii', 'aargh', 'aarti', 'abaca'])

    # Test Case 5
    print("\n--- Test Case 5 ---")
    ##Arrange
    target_word_filename = "target_words.txt"
    ##Act
    target_word_list = read_words_from_file(TARGET_WORDS_FILE)
    ##Assert
    if target_word_list: 
        print("Got:", target_word_list[-5:], "Expected:", ["young", "youth", "zebra", "zesty", "zonal"])

    # Test Case 6
    print("\n--- Test Case 6 ---")
    #TODO: Set list of words to ["apple", "banana", "cherry"]
    print("Test Case 6 Output (will vary):")
    list_of_words = ["apple", "banana", "cherry"]
    for count in range(5):
        selected_word = Random_Target_Word(list_of_words)
        print(selected_word)
        
    print("\n--- TESTS COMPLETE ---")


# TODO: Main Program
# Use __name__ == "__main__" to make the file importable
if __name__ == "__main__":
    if DEBUG:
        test_game()
    else:
        play_game()
