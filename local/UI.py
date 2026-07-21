import customtkinter as ctk
from engine import GameMechanics
import random
import sys
import os

class WordUI(ctk.CTkFrame):
    def __init__(self, master, word_len, on_complete = None):
        super().__init__(master)
        
        self.word_length = word_len
        self.entries = []
        self.on_complete = on_complete

        for i in range (word_len):
            entry = ctk.CTkEntry(self, fg_color = "grey", width = 40)
            entry.grid(row=1, column = i+1, padx = 5, pady=5)
            entry.bind("<KeyRelease>", lambda event, e=entry, idx=i: self.handle_key(event, e, idx))
            self.entries.append(entry)
            
        self.entries[0].focus_set() 
    
    def set_status(self, index, color):
        self.entries[index].configure(fg_color=color) 
    
    def get_guess(self):
        return "".join(entry.get() for entry in self.entries) 
    
    def apply_color(self, colors):
        for i, color in enumerate(colors):
            self.set_status(i, color)
            
    def lock_row(self):
        for entry in self.entries:
            entry.configure(state="disabled")
    
    def handle_key(self, event, entry, idx):
        text = entry.get()
        if len(text) > 1:
            entry.delete(0, "end")
            entry.insert(0, text[-1])
            text = text[-1]

        # Backspace: move to previous box if this one is empty
        if event.keysym == "BackSpace":
            if text == "" and idx > 0:
                self.entries[idx - 1].focus_set()
            return

        # Typing a letter: move to next box
        if text != "":
            if idx + 1 < len(self.entries):
                self.entries[idx + 1].focus_set()
            elif self.on_complete:
                self.on_complete() 
    

class WordleUI(ctk.CTk):
    MAX_ATTEMPTS = 6    
    
    def __init__(self, secret_word, word_list):
        super().__init__()

        #======================SET UP============================#
        
        self.title("Word Guesser")
        self.geometry("600x600")
        self.attempts = 0
        self.word_list = word_list
        self.secret_word = secret_word
        self.word_len = len(secret_word)

        #-----------------------UI--------------------------------#

        self.life_label = ctk.CTkLabel(self, text=f"{self.MAX_ATTEMPTS - self.attempts} tries left")
        self.life_label.pack() 

        self.row = ctk.CTkFrame(self)
        self.row.pack(pady=10)
        
        self.message = ctk.CTkLabel(self, text="")
        self.message.pack()
        

        
        self.word_ui = None
        self.new_row()
        
        self.submit_button = ctk.CTkButton(self, text="SUBMIT GUESS", command= self.submit_guess)
        self.submit_button.pack()
                #======================Game Functionality==================#
    
    def show_popup(self, text):
        popup = ctk.CTkToplevel(self)
        popup.title("WordGuesser")
        popup.geometry("350x200")
        popup.attributes("-topmost", True)
        
        label = ctk.CTkLabel(popup, text=text, font=("Arial", 20))
        label.pack(pady=20)
        
        close_button = ctk.CTkButton(popup, text="OK", command=lambda: [popup.destroy(), self.restart_game()])
        close_button.pack(pady=10)
    
    def new_row(self):
        self.word_ui = WordUI(self.row, self.word_len)
        self.word_ui.pack(pady = 10)
        
    def restart_game(self):
        self.secret_word = random.choice(self.word_list)
        self.word_len = len(self.secret_word)
        self.attempts = 0
        
        for widgets in self.row.winfo_children():
            widgets.destroy()
            
        self.message.configure(text = "")
        self.submit_button.configure(state="normal")
        self.new_row()
        
    def submit_guess(self):
        guess = self.word_ui.get_guess().lower()
        mechanics = GameMechanics(self.secret_word, guess)

        is_valid, word_len, guess_len = mechanics.length_check()
        if not is_valid:
            self.show_popup(text=f"Wrong length! Need {word_len} letters, got {guess_len}.")
            return
        
        colors = mechanics.compare_words()
        self.word_ui.apply_color(colors)
        self.word_ui.lock_row()
        self.attempts +=1
        
        if self.secret_word == guess:
            self.show_popup(text="You are correct")
            self.submit_button.configure(state="disabled")
            return
        elif self.attempts >= self.MAX_ATTEMPTS:
            self.show_popup(text=f"You Lost! The word was {self.secret_word}")
            self.submit_button.configure(state="disabled")
            return
            
        self.new_row()
        self.word_ui.entries[0].focus_set()


#==============================Execution===========================#

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

with open(resource_path("words.txt"), "r") as file:
    lines = file.read().splitlines()

random_word = random.choice(lines).lower()

        
if __name__ == "__main__":
    app = WordleUI(random_word, lines)
    app.mainloop()