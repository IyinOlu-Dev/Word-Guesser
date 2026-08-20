let targetWord = "";
const maxGuesses = 6;
let currentRow = 0;
let currentTile = 0;
let board = [];

// Initialize an empty board based on the word length
function initBoardArray() {
    const wordLength = targetWord.length;
    board = [];
    for (let i = 0; i < maxGuesses; i++) {
        board.push(new Array(wordLength).fill(""));
    }
}

// 1. Build the grid UI dynamically and adjust CSS columns for any word length
function createGrid() {
    const grid = document.getElementById("grid");
    grid.innerHTML = ""; // Clear existing grid if resetting
    
    // Dynamically set CSS grid columns based on word length
    grid.style.setProperty('--word-length', targetWord.length);

    board.forEach((row, rowIndex) => {
        const rowDiv = document.createElement("div");
        rowDiv.className = "row";
        rowDiv.id = `row-${rowIndex}`;
        // Apply column template dynamically to each row
        rowDiv.style.gridTemplateColumns = `repeat(${targetWord.length}, 50px)`;
        
        row.forEach((_, tileIndex) => {
            const tileDiv = document.createElement("div");
            tileDiv.className = "tile";
            tileDiv.id = `tile-${rowIndex}-${tileIndex}`;
            rowDiv.appendChild(tileDiv);
        });
        
        grid.appendChild(rowDiv);
    });
}

// 2. Fetch words in the background and rebuild board to match length
async function loadTargetWord() {
    try {
        const response = await fetch('/core/words.txt');
        const text = await response.text();
        const words = text.split('\n').map(w => w.trim().toUpperCase()).filter(w => w.length > 0);
        
        if (words.length > 0) {
            const randomIndex = Math.floor(Math.random() * words.length);
            targetWord = words[randomIndex];
        }
    } catch (error) {
        console.error("Could not load words.txt, using default word.", error);
    }

    // Once word is loaded, re-initialize board and grid with correct dimensions
    initBoardArray();
    createGrid();
}

// 3. Listen for keyboard inputs
document.addEventListener("keydown", (e) => {
    if (currentRow >= maxGuesses) return;

    if (e.key === "Enter") {
        submitGuess();
    } else if (e.key === "Backspace") {
        deleteLetter();
    } else if (/^[a-zA-Z]$/.test(e.key)) {
        addLetter(e.key.toUpperCase());
    }
});

function addLetter(letter) {
    if (currentTile < targetWord.length) {
        board[currentRow][currentTile] = letter;
        updateTileUI(currentRow, currentTile, letter);
        currentTile++;
    }
}

function deleteLetter() {
    if (currentTile > 0) {
        currentTile--;
        board[currentRow][currentTile] = "";
        updateTileUI(currentRow, currentTile, "");
    }
}

function updateTileUI(row, tile, letter) {
    const tileDiv = document.getElementById(`tile-${row}-${tile}`);
    if (tileDiv) {
        tileDiv.textContent = letter;
    }
}

// 4. Process and evaluate the guess dynamically
function submitGuess() {
    if (currentTile < targetWord.length) {
        alert(`Not enough letters! (Needs ${targetWord.length})`);
        return;
    }

    const guessArray = board[currentRow]; 
    const targetArray = targetWord.split('');

    // Evaluate each letter
    guessArray.forEach((letter, index) => {
        const tileDiv = document.getElementById(`tile-${currentRow}-${index}`);
        
        if (letter === targetArray[index]) {
            tileDiv.classList.add("correct");
        } else if (targetArray.includes(letter)) {
            tileDiv.classList.add("present");
        } else {
            tileDiv.classList.add("absent");
        }
    });

    if (guessArray.join("") === targetWord) {
        alert("You Win!");
        currentRow = maxGuesses; 
        document.getElementById("restart-btn").style.display = "inline-block"; 
        return;
    }

    currentRow++;
    currentTile = 0;

    if (currentRow === maxGuesses) {
        alert(`Game Over! The word was ${targetWord}`);
        document.getElementById("restart-btn").style.display = "inline-block"; 
    }
}

// Function to reset the game state
function resetGame() {
    currentRow = 0;
    currentTile = 0;
    document.getElementById("restart-btn").style.display = "none";
    loadTargetWord(); // Fetches a new word and rebuilds the grid automatically
}

// Initial startup call
initBoardArray();
createGrid();
loadTargetWord();