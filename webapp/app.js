const MAX_GUESSES = 6;
const FLIP_STEP = 280; // ms between tiles revealing
const KEY_ROWS = ["QWERTYUIOP", "ASDFGHJKL", ["ENTER", ..."ZXCVBNM", "⌫"]];

let targetWord = "APPLE";
let currentRow = 0;
let currentTile = 0;
let board = [];
let locked = false;      // true while reveal animation plays or game is over
let keyStatus = {};      // letter -> "correct" | "present" | "absent"
let toastTimer;

const $ = (id) => document.getElementById(id);
const RANK = { absent: 1, present: 2, correct: 3 };

/* ---------- Setup ---------- */
function initBoardArray() {
    board = Array.from({ length: MAX_GUESSES }, () => new Array(targetWord.length).fill(""));
}

function createGrid() {
    const grid = $("grid");
    grid.innerHTML = "";
    grid.style.setProperty("--n", targetWord.length);
    board.forEach((row, r) => {
        const rowDiv = document.createElement("div");
        rowDiv.className = "row";
        rowDiv.id = `row-${r}`;
        rowDiv.setAttribute("role", "row");
        row.forEach((_, t) => {
            const tile = document.createElement("div");
            tile.className = "tile";
            tile.id = `tile-${r}-${t}`;
            tile.setAttribute("role", "gridcell");
            rowDiv.appendChild(tile);
        });
        grid.appendChild(rowDiv);
    });
    $("subtitle").textContent = `Guess the ${targetWord.length}-letter word in ${MAX_GUESSES} tries.`;
}

function createKeyboard() {
    const kb = $("keyboard");
    kb.innerHTML = "";
    KEY_ROWS.forEach((keys) => {
        const row = document.createElement("div");
        row.className = "kb-row";
        [...keys].forEach((k) => row.appendChild(makeKey(k)));
        kb.appendChild(row);
    });
}

function makeKey(k) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "key" + (k.length > 1 || k === "⌫" ? " wide" : "");
    btn.textContent = k === "ENTER" ? "Enter" : k;
    btn.dataset.key = k;
    btn.setAttribute("aria-label", k === "⌫" ? "Backspace" : k === "ENTER" ? "Enter" : k);
    btn.addEventListener("click", () => handleKey(k));
    return btn;
}

async function loadTargetWord() {
    try {
        const response = await fetch("/core/words.txt");
        const text = await response.text();
        const words = text.split("\n").map((w) => w.trim().toUpperCase()).filter(Boolean);
        if (words.length) targetWord = words[Math.floor(Math.random() * words.length)];
    } catch (error) {
        console.error("Could not load words.txt, using default word.", error);
    }
    startRound();
}

function startRound() {
    currentRow = 0;
    currentTile = 0;
    keyStatus = {};
    locked = false;
    $("result").hidden = true;
    initBoardArray();
    createGrid();
    createKeyboard();
}

/* ---------- Input ---------- */
function handleKey(key) {
    if (locked || currentRow >= MAX_GUESSES) return;
    if (key === "ENTER") submitGuess();
    else if (key === "⌫") deleteLetter();
    else addLetter(key);
}

document.addEventListener("keydown", (e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === "Enter") {
        if (document.activeElement && document.activeElement.tagName === "BUTTON") return; // let focused buttons act on Enter
        handleKey("ENTER");
    } else if (e.key === "Backspace") handleKey("⌫");
    else if (/^[a-zA-Z]$/.test(e.key)) handleKey(e.key.toUpperCase());
});

function addLetter(letter) {
    if (currentTile >= targetWord.length) return;
    board[currentRow][currentTile] = letter;
    const tile = $(`tile-${currentRow}-${currentTile}`);
    tile.textContent = letter;
    tile.classList.add("filled");
    currentTile++;
}

function deleteLetter() {
    if (currentTile === 0) return;
    currentTile--;
    board[currentRow][currentTile] = "";
    const tile = $(`tile-${currentRow}-${currentTile}`);
    tile.textContent = "";
    tile.classList.remove("filled");
}

/* ---------- Feedback ---------- */
function toast(message) {
    const el = $("toast");
    el.textContent = message;
    el.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove("show"), 1600);
}

function shakeRow(row) {
    const el = $(`row-${row}`);
    el.classList.remove("shake");
    void el.offsetWidth; // restart animation
    el.classList.add("shake");
}

/* ---------- Evaluation ---------- */
function evaluate(guess, target) {
    const guessArr = [...guess];
    const targetArr = [...target];
    const statuses = new Array(guessArr.length).fill("absent");

    guessArr.forEach((letter, i) => {
        if (letter === targetArr[i]) {
            statuses[i] = "correct";
            targetArr[i] = null;
            guessArr[i] = null;
        }
    });
    guessArr.forEach((letter, i) => {
        if (letter === null) return;
        const j = targetArr.indexOf(letter);
        if (j !== -1) {
            statuses[i] = "present";
            targetArr[j] = null;
        }
    });
    return statuses;
}

function updateKeyboard(guess, statuses) {
    [...guess].forEach((letter, i) => {
        const prev = keyStatus[letter];
        if (!prev || RANK[statuses[i]] > RANK[prev]) keyStatus[letter] = statuses[i];
        const btn = document.querySelector(`.key[data-key="${letter}"]`);
        if (btn) btn.className = `key ${keyStatus[letter]}`;
    });
}

/* ---------- Submit ---------- */
function submitGuess() {
    if (currentTile < targetWord.length) {
        toast(`Needs ${targetWord.length} letters`);
        shakeRow(currentRow);
        return;
    }

    const row = currentRow;
    const guess = board[row].join("");
    const statuses = evaluate(guess, targetWord);
    const won = guess === targetWord;

    locked = true;
    statuses.forEach((status, i) => {
        const tile = $(`tile-${row}-${i}`);
        setTimeout(() => {
            tile.classList.add("flip");
            setTimeout(() => tile.classList.add(status), FLIP_STEP / 2 + 60);
        }, i * FLIP_STEP);
    });

    setTimeout(() => {
        updateKeyboard(guess, statuses);
        currentRow++;
        currentTile = 0;

        if (won) return endGame(`You got it in ${currentRow} ${currentRow === 1 ? "try" : "tries"}.`);
        if (currentRow === MAX_GUESSES) return endGame(`Out of tries. The word was ${targetWord}.`);
        locked = false;
    }, statuses.length * FLIP_STEP + 400);
}

function endGame(message) {
    locked = true;
    $("result-text").textContent = message;
    $("result").hidden = false;
    $("restart-btn").focus();
}

function resetGame() {
    $("subtitle").textContent = "Loading a word…";
    loadTargetWord();
}

$("restart-btn").addEventListener("click", resetGame);

/* ---------- Start ---------- */
startRound();
loadTargetWord();