/**
 * Chatty Talkie - Frontend Application
 * Handles UI interactions and API communication.
 */

const API_BASE = "http://127.0.0.1:8000/api";

// DOM Elements
const sourceText = document.getElementById("source-text");
const targetText = document.getElementById("target-text");
const sourceLang = document.getElementById("source-lang");
const targetLang = document.getElementById("target-lang");
const translateBtn = document.getElementById("translate-btn");
const swapBtn = document.getElementById("swap-btn");
const clearBtn = document.getElementById("clear-btn");
const copyBtn = document.getElementById("copy-btn");
const charCount = document.getElementById("char-count");
const statusBar = document.getElementById("status-bar");
const statusText = document.getElementById("status-text");

// === Translation ===

async function translate() {
    const text = sourceText.value.trim();
    if (!text) return;

    const src = sourceLang.value;
    const tgt = targetLang.value;

    if (src === tgt) {
        targetText.value = text;
        return;
    }

    translateBtn.disabled = true;
    translateBtn.textContent = "Translating...";
    targetText.value = "";

    try {
        const response = await fetch(`${API_BASE}/translate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                source_lang: src,
                target_lang: tgt,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Translation failed");
        }

        const data = await response.json();
        targetText.value = data.translated_text;
    } catch (error) {
        targetText.value = `Error: ${error.message}`;
        setStatus("error", `Translation error: ${error.message}`);
    } finally {
        translateBtn.disabled = false;
        translateBtn.textContent = "Translate";
    }
}

// === Swap Languages ===

function swapLanguages() {
    const tempLang = sourceLang.value;
    sourceLang.value = targetLang.value;
    targetLang.value = tempLang;

    // Also swap text content
    const tempText = sourceText.value;
    sourceText.value = targetText.value;
    targetText.value = tempText;

    updateCharCount();
}

// === Clear & Copy ===

function clearText() {
    sourceText.value = "";
    targetText.value = "";
    updateCharCount();
    sourceText.focus();
}

async function copyTranslation() {
    const text = targetText.value;
    if (!text) return;

    try {
        await navigator.clipboard.writeText(text);
        copyBtn.textContent = "✓";
        setTimeout(() => {
            copyBtn.textContent = "📋";
        }, 2000);
    } catch {
        // Fallback for older browsers
        targetText.select();
        document.execCommand("copy");
    }
}

// === Character Count ===

function updateCharCount() {
    const count = sourceText.value.length;
    charCount.textContent = `${count} / 5000`;
}

// === Status ===

function setStatus(type, message) {
    statusBar.className = `status-bar ${type}`;
    statusText.textContent = message;
}

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();

        if (data.model_loaded) {
            setStatus("ready", "✓ Model loaded — Ready to translate");
        } else {
            setStatus("loading", "⏳ Model is loading... Please wait");
            // Retry after 5 seconds
            setTimeout(checkHealth, 5000);
        }
    } catch {
        setStatus("error", "✕ Cannot connect to backend. Is the server running?");
        // Retry after 10 seconds
        setTimeout(checkHealth, 10000);
    }
}

// === Keyboard Shortcut ===

function handleKeyDown(event) {
    // Ctrl+Enter or Cmd+Enter to translate
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        translate();
    }
}

// === Event Listeners ===

translateBtn.addEventListener("click", translate);
swapBtn.addEventListener("click", swapLanguages);
clearBtn.addEventListener("click", clearText);
copyBtn.addEventListener("click", copyTranslation);
sourceText.addEventListener("input", updateCharCount);
sourceText.addEventListener("keydown", handleKeyDown);

// Prevent same language selection
sourceLang.addEventListener("change", () => {
    if (sourceLang.value === targetLang.value) {
        // Auto-switch target to a different language
        const options = ["en", "ro", "es"];
        targetLang.value = options.find((l) => l !== sourceLang.value);
    }
});

targetLang.addEventListener("change", () => {
    if (targetLang.value === sourceLang.value) {
        const options = ["en", "ro", "es"];
        sourceLang.value = options.find((l) => l !== targetLang.value);
    }
});

// === Init ===

checkHealth();
