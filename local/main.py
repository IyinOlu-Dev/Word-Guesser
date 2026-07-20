import random
from engine import GameMechanics
from UI import wordleUI


playing_again = True
while playing_again:

    with open("words.txt", "r") as file:
        lines = file.read().splitlines()

    random_word = random.choice(lines).lower()
    word_lenght = len(random_word)
    
    tries = 6

    Game = True
    while Game:
        user_guess = str(input(f"Please guess the words. HINT: It is a {word_lenght} letter word: ")).lower().strip()
        game = GameMechanics(random_word, user_guess)
        if tries == 0:
            Game = False

        is_valid, word_len, guess_len = game.lenght_check()
        print(game.word)
        if is_valid:
        
            print(game.word)
            print(game.guess)

            check = game.compare_words()
        
            if all(status == "green" for status in check):
                print("YOU WIN!!!")
                Game = False
            else:
                for i, status in enumerate(check):
                    print(f"letter at position {i}: {user_guess[i]} is {status.upper()}")
                    tries -=1
                    print(tries)
        else:
            print(f"Wrong length! You entered {guess_len} letters, but it must be {word_len}.")

    replay = input("Play again y/n: ").lower().strip()
    if replay != "y":
        playing_again = False
        print("Thanks for playing the game")