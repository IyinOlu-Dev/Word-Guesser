import customtkinter as ctk
from engine import GameMechanics

# GRAY = "grey"

class WordUI(ctk.CTkFrame):
    def __init__(self, len):
        super().__init__()
        
        self.word_lenght = len
        self.entries = []
        
        
        for i in range (len):
            entry = ctk.CTkEntry(self, fg_color = "grey", width = 40)
            entry.grid(row=1, col = 1, padx = 5, pady=5)
            self.entries.append(entry)
        

class ColorChoice():
    def __init__(self, status):
        super().__init__()
        
        self.status  = status
        


class WordleUI(ctk.CTk):
    def __init__(self, secret_word):
        super().__init__()
        
        self.title("Wordle")
        self.geometry("400x400")
        
        self.secret_word = secret_word
        self.word_len = len(secret_word)
        self.mechanics = GameMechanics(word = secret_word)
        
        
        #-----------------------UI--------------------------------#
        
        self.cover_block = ctk.Ctk