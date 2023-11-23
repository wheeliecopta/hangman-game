import requests
import random

##############################
# -----SET UP RANDOM WORD------#
##############################

# Thanks, stackoverflow
# https://stackoverflow.com/questions/18834636/random-word-generator-python
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.decode('utf-8').splitlines()  # Thanks, ChatGPT for helping me decode the website-content

# Pick a random word from 'WORDS' as the secret word
word = random.choice(WORDS)


#############################
# -----OTHER VARIABLES-------#
#############################

# Create list with placeholders (dashes) where the correct guesses will be stored in their right place
solution = "-" * len(word)

# Number of false guesses allowed
strikes = 6
# Counter for the false guesses
strike_count = 0

# List to be filled with incorrectly guessed letters
wrong_letters = []

# Counter for the correctly made guesses as measure for when the game is won
right_guess = 0

# Hangman image progression stored in a dict
hangman = {0: '''_________________
                |



            ''',
           1: '''_________________
                |
                O


                ''',
           2: '''_________________
                |
                O
               /

               ''',
           3: '''_________________
                |
                O
               / \\

               ''',
           4: '''_________________
                |
                O
               / \\
                |
                ''',
           5: '''_________________
                |
                O
               / \\
                |
               /''',
           6: '''_________________
                |
                O
               / \\
                |
               / \\ '''}



########################
# ------MAIN GAME------#
########################

# Get a guess for a letter from the player (while there are still guesses left)
while strike_count < strikes:
    letter = input("Give me a letter and press enter: ")

    # Make sure that the given input is a single letter.
    if letter.isalpha() == False or len(letter) != 1:
        print("====================================================")
        print(hangman[strike_count])
        print("Nope, not how it works. Give me a single letter.\nNext try.")
        print("====================================================")
        continue

    # Make sure that the letter was not already given
    if letter.upper() in solution or letter.upper() in wrong_letters:
        print("====================================================")
        print(hangman[strike_count])
        print(f"You already gave me \"{letter.upper()}\".")
        print(f"Status quo: {solution.upper()}.")
        # Show list of wrong letters only if there were wrong guesses already made
        if wrong_letters != []:
            print(f"Mistakes: {wrong_letters}.")
        # Correct written grammar, 'one strike' vs 'strikes'
        if strikes - strike_count == 1:
            print(f"{strikes - strike_count} strike left.")
        else:
            print(f"{strikes - strike_count} strikes left.")
        print("How about we try a new letter, darling?")
        print("====================================================\n")
        continue

    # If the letter is in the word, add it to the 'solution' list and adjust the 'right_guess' counter
    if letter in word:
        if word[0] == letter:
            solution = letter.upper() + solution[1:]
        for i in range(len(word)):
            if word[i] == letter:
                solution = solution[:i] + letter.upper() + solution[i+1:]
                right_guess += 1
        # End game if all letters have been guessed correctly
        if right_guess == len(word):
            break

        # Let the player know about the status quo and show the hangman image
        print("====================================================")
        print(hangman[strike_count])
        print(f"Wow, so smart! \"{letter.upper()}\" is in the word.")
        print(f"--> {solution.upper()}")
        # Only print out 'wrong_letters' if false guesses have already been made
        if wrong_letters != []:
            print(f"Mistakes: {wrong_letters}.")
        if strikes - strike_count == 1:
            print(f"{strikes - strike_count} strike left.")
        else:
            print(f"{strikes - strike_count} strikes left.")
        print("====================================================\n")

    # Else if the letter is not in the word...
    else:
        strike_count += 1
        # End game if the maximum amount of mistakes has been made
        if strike_count == strikes:
            break
        wrong_letters.append(letter.upper())
        print("====================================================")
        print(hangman[strike_count])
        # Two different versions: One if only one mistake left and the second version if more than one mistakes left
        if strike_count == strikes - 1:
            print(f"This is not going so well. Holding on for dear life, sweetie.")
            print("1 strike left.")
        else:
            print(f"\"{letter.upper()}\"? Nope. That was mistake no. {strike_count}")
            print(f"{strikes - strike_count} strikes left.")
        print(f"Status quo: {solution.upper()}.")
        print(f"Mistakes: {wrong_letters}.")
        print("====================================================\n")

##########################
# ------END OF GAME-------#
##########################

# Player loses
if strike_count == strikes:
    print("====================================================")
    print(hangman[strike_count])
    print(f"Da-dum! That was your last guess. You lose, sucker.")
    print(f"The word was \"{word.upper()}\". Wasn't that hard...")
    print("====================================================")

# Player wins
else:
    print("====================================================")
    print(hangman[strike_count])
    print(f"BAM! You win. What a boss. The word is \"{word.upper()}\".")
    print("====================================================")
