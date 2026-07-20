class GameMechanics:
    def __init__(self, word, guess):
        self.word = word
        self.guess = guess
        
    def lenght_check(self) -> tuple[bool, int, int]:
        is_valid =  len(self.word) == len(self.guess)
        return is_valid, len(self.word), len(self.guess)

    def compare_words(self):
        result= ["gray"] * len(self.word)
        word_letter = list(self.word)
        guess_letter = list(self.guess)
        
        for i, (g,h) in enumerate(zip(self.word, self.guess)):
            if g == h:
                result[i] = "green"
                guess_letter[i] = None
                word_letter[i] = None
            
        for i, letter in enumerate(guess_letter):
            if letter is not None and letter in word_letter:
                result[i] = "yellow"
                word_letter[word_letter.index(letter)] = None
                
        return result