from fastapi import FastAPI, status, HTTPException
from fastapi.staticfiles import StaticFiles
from core.engine import GameMechanics
from pydantic import BaseModel

from pathlib import Path

app = FastAPI()

WORD_PATH = Path(__file__).resolve().parent.parent /"core"/"words"
static =  Path(__file__).resolve().parent/"statics"



class GuessRequest(BaseModel):
    guess: str
    word: str


# @app.get("/")
# def home():
#     return {"message": "hello"}


@app.post("/word-guesser")
def guess(req: GuessRequest):
    game = GameMechanics(req.word, req.guess)
    
    is_valid, word_len, = game.lenght_check()
    
    if not is_valid:
        raise HTTPException(
           status_code = status.HTTP_400_BAD_REQUEST,
           detail = f"Your guess has to be the same as the length of the word which is {word_len}" 
        )
    else:
        return {"result": game.compare_words()}
    
    
app.mount("/", StaticFiles(directory=static, html=True), name = "statics")
    