let minutes = 25;
let seconds = 0;
let isRunning = false;
let isBreak = false;
let totalFocusTime = 0; // in seconds
let sessionStartTime;
let focusSessionStartTime;
let timer;
let session_no = 1;

const button = document.getElementById("start");
const stats = document.getElementById("status");
const time = document.getElementById("time");

// As button is clicked, if it is not running, start it. If it is running, stop it.
button.addEventListener("click", () => {
    if (!isRunning) {
        startTimer();
    } else {
        stopTimer();
    }
});

function startTimer() {
    isRunning = true;
    button.textContent = "Stop";
    sessionStartTime = Date.now();
    if (!isBreak) {
        focusSessionStartTime = sessionStartTime;
    }
    timer = setInterval(updateTimer, 1000);
    updateStatus();
}

function stopTimer() {
    isRunning = false;
    button.textContent = "Start";
    clearInterval(timer);
    if (!isBreak) {
        totalFocusTime += Math.floor(
            (Date.now() - focusSessionStartTime) / 1000
        );
    }

    sendDataToServer();
    resetTimer();
}

function updateStatus() {
    if (!isBreak) {
        stats.textContent = "Focus";
    } else {
        stats.textContent = "Break";
    }
}

function updateTimerText() {
    time.textContent = `${padZero(minutes)}:${padZero(seconds)}`;
}

function padZero(num) {
    return num.toString().padStart(2, "0");
}

function resetTimer() {
    minutes = 25;
    seconds = 0;
    isBreak = false;
    updateTimerText();
    updateStatus();
}

function updateTimer() {
    if (seconds > 0) {
        seconds--;
    } else if (minutes > 0) {
        minutes--;
        seconds = 59;
    } else {
        if (!isBreak) {
            session_no++;
            if (session_no >= 4) {
                minutes = 20;
                seconds = 0;
                session_no = 1;
            } else {
                minutes = 5;
                seconds = 0;
            }
            isBreak = true;
            totalFocusTime += 25 * 60;
        } else {
            isBreak = false;
            minutes = 25;
            seconds = 0;
            focusSessionStartTime = Date.now();
        }

        updateStatus();
    }
    updateTimerText();
}

function sendDataToServer() {
    fetch("/focus_data", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            totalFocusTime: totalFocusTime,
            focusStartTime: focusSessionStartTime,
        }),
    })
        .then((response) => response.json())
        .then((data) => console.log("Success:", data))
        .catch((error) => console.error("Error:", error));
}
updateTimerText();
updateStatus();
