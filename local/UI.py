import customtkinter as ctk
from engine import GameMechanics
import random

class WordUI(ctk.CTkFrame):
    def __init__(self, master, word_len):
        super().__init__(master)
        
        self.word_lenght = word_len
        self.entries = []
        
        
        for i in range (word_len):
            entry = ctk.CTkEntry(self, fg_color = "grey", width = 40)
            entry.grid(row=1, column = i+1, padx = 5, pady=5)
            self.entries.append(entry)
        
    def set_status(self, index, color):
        self.entries[index].configure(fg_color=color) 
    
    def limit_lenght(self, event, entry):
        text = entry.get()
        if len(text) >1:
            entry.delete(0, "end")
            entry.insert(0, 1)
        


class WordleUI(ctk.CTk):
    def __init__(self, secret_word):
        super().__init__()

        #======================SET UP============================#
        
        self.title("Word Guesser")
        self.geometry("400x400")
        
        self.secret_word = secret_word
        self.word_len = len(secret_word)

        #-----------------------UI--------------------------------#

        self.word_ui = WordUI(self, self.word_len)
        self.word_ui.pack(pady=20)
        
        
        self.submit_button = ctk.CTkButton(self, text="SUBMIT GUESS", command= self.submit_guess)
        self.submit_button.pack()
                #======================Game Command Def==================#
    def submit_guess(self):
        guess = self.word_ui.get_guess()
        mechanics = GameMechanics(self.secret_word, guess)
        
        is_valid, word_len, guess_len = mechanics.lenght_check()
        if not is_valid:
            self.message.configure(text=f"Wrong length! Need {word_len} letters, got {guess_len}.")
            return










#==============================Execution===========================#
with open("words.txt", "r") as file:
    lines = file.read().splitlines()

random_word = random.choice(lines).lower()

        
if __name__ == "__main__":
    app = WordleUI(random_word)
    app.mainloop()