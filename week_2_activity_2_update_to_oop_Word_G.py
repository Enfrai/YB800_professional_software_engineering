import random
import string

'''
Week2. Activity 2: Update the code to be OOP for the attached file

See the attached file and update it to align with OOP principles. 
Add appropriate inline comments to explain the code. 
Share your GitHub link by tomorrow at 8:00 AM
'''

def get_random_word():
    '''
    Randomly pick up and return one word from a list of constant words.
    '''

    # To define a data set of words
    words = [
        "python", "variable", "function", "iterator", "notebook",
        "pipeline", "dataset", "computer", "research", "analytics"
    ]
    # Randomly pick up a word from the data set and return it
    return random.choice(words)

def make_blanks(word):
    '''
    Relace each letter in the word with an underscore, 
    store them in a list and return.
    '''
    return ["_" for _ in word]

def prompt_for_letter(used_letters):
    '''
    Lead user to input a letter, 
    and validate the input to ensure it is a single letter and
    not already used.
    '''

    while True:
        # Grab an input from the user with wish for a letter
        guess = input("Guess a letter: ").strip().lower()

        # Validate the input to ensure it is a single letter and
        # not already used
        if len(guess) != 1 or guess not in string.ascii_lowercase:
            print(" → Please enter a single A-Z letter.")
            continue
        if guess in used_letters:
            print(" → You already tried that letter.")
            continue
        return guess

def reveal_letters(word, blanks, letter):
    '''
    Try to verify if the letter is used for the spelling of the word.
    If it is, replace the blank '_' with the letter for any time 
    this letter appears in the word and return true.
    And if not, return false.
    '''

    found_any = False
    for i, ch in enumerate(word):
        if ch == letter and blanks[i] == "_":
            blanks[i] = letter
            found_any = True
    return found_any

def all_blanks_filled(blanks):
   '''
   Check if all blanks are filled with letters.
   If yes, return true. Otherwise, return false.
   '''
   return "_" not in blanks

def play_game(max_lives=6):
    '''
    Start to play a word guessing game. 
    The user will be asked to guess what letters are contained 
    in a random word with a limited number of lives, default to 6.
    '''

    # Randomly generate a word.
    secret = get_random_word()
    # Init a list of blanks to represent the letters in the word.
    blanks = make_blanks(secret)
    # Maximum tries for misses, default to 6.
    lives = max_lives
    # Init a set to store what letters have been tried by the user.
    used = set()

    print("\nWelcome to Word Guessing!")
    print(f"The word has {len(secret)} letters.")

    # Show blanks to the user for the first time.
    print(" ".join(blanks))

    while True:
        # Ask the user to successfully guess a letter
        guess = prompt_for_letter(used)
        used.add(guess)

        # To check if the guessed letter is in the word, and if yes, reveal the letter in the blanks.
        if reveal_letters(secret, blanks, guess):
            # The letter is matched and revealed, and show the gussed result.
            print("\n Well done, Nice job! You found a letter.")
            print(" ".join(blanks))
            # To check if all blanks are filled with letters, 
            # and if yes, the user wins the game and jump out the loop.
            if all_blanks_filled(blanks):
                print("\n Congratulation! You guessed the word!")
                print(f"Word: {secret}")
                print("GAME OVER")
                break
        else:
            # The letter is not matched, maximum tries for misses is reduced by 1,
            # and show the already guessed result.
            lives -= 1
            print(f"\nNope. You lose a life. Lives left: {lives}")
            print(" ".join(blanks))

            # Jump out the loop, and show the correct word if the user is out of lives.
            if lives <= 0:
                print("\n Out of lives & Sad story!")
                print(f"The word was: {secret}")
                print("GAME OVER")
                break

        # (loop continues to ask for another letter)


if __name__ == "__main__":
    # Main entrance.
    play_game()
