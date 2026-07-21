import random
from engine import GameMechanics


playing_again = True
while playing_again:

    with open("words.txt", "r") as file:
        lines = file.read().splitlines()

    random_word = random.choice(lines).lower()
    word_length = len(random_word)
    
    tries = 6

    Game = True
    while Game:
        user_guess = str(input(f"Please guess the words. HINT: It is a {word_length} letter word: ")).lower().strip()
        game = GameMechanics(random_word, user_guess)

            

        is_valid, word_len, guess_len = game.length_check()
        if is_valid:
            tries -=1
            
            print(game.guess)

            check = game.compare_words()
        
            if all(status == "green" for status in check):
                print("YOU WIN!!!")
                Game = False
            else:
                for i, status in enumerate(check):
                    print(f"letter at position {i}: {user_guess[i]} is {status.upper()}")
            print(f"Tries left: {tries}")
        else:
            print(f"Wrong length! You entered {guess_len} letters, but it must be {word_len}.")
        
        
        if tries == 0 and Game:
            print(f"You Lose. \nThe word was {random_word}" )
            Game = False
    replay = input("Play again y/n: ").lower().strip()
    if replay not in ("y", "yes") :
        playing_again = False
        print("Thanks for playing the game")