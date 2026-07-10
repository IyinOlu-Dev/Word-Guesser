import random
import customtkinter as ctk




with open("wordlist.txt", "r", encoding= "utf-8") as file:
    words = file.read().splitlines()
    

    
    word_index = random.choice(words)
    chosen_word = words[word_index]
    print(chosen_word)
    test = (iter(chosen_word))
    print(type(test))
    # print(len(test))

#----------------MAKING A GUESS----------------------------#
def make_guess() -> str:
    guess = input(str("Make a guess: "))
    return guess
    

#---------------Verifying a guess-----------------

def verify_guess(choice: str) -> str:
    if choice != chosen_word:
        return("This is incorrect")
    else: 
        return("This is correct")
        
        
#------------------Check Accuracy----------------------
def accuracy(guess:str, chosen:list ) -> str:

    if len(guess) != len(chosen):
        print("Guess must be the same length as the word")
        return
    
    for i, (g,c) in enumerate (zip(guess, chosen)):
        if g != c:
            print (f"Mismatch at position {i +1}: {guess[i]}")
            
            
    
    
    
    
#-------------------------UI----------------------------
#-------------------------UI CONSTANTS--------------------------

app =ctk.CTk()
app.geometry("600x700")
app.title("Wordle")

current_theme = ctk.get_appearance_mode()
app._set_appearance_mode(current_theme)
#---------------------- UI FUNNCTIONS-----------------------
def toggle_appearance():
    global current_theme
    
    if current_theme == "Light":
        current_theme = "Dark"
    else:
        current_theme = "Light"
        
    ctk.set_appearance_mode(current_theme)     
#-------------------CLIENT FACING UI---------------------------------------------------

toggle_appearance_btn = ctk.CTkButton(app, text= "Toggle Theme", command= toggle_appearance)
toggle_appearance_btn.pack()













app.mainloop()