// thinking.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. Retrieve Data (Optional, for context/verification)
    const pipelineData = sessionStorage.getItem('pipelineData');
    if (pipelineData) {
        console.log("🚀 Pipeline Data Received:", JSON.parse(pipelineData));
    }

    // 2. Timer Countdown Logic
    const timerElement = document.getElementById('countdown-timer');
    let timeLeft = 120; // 2 minutes in seconds

    const timerInterval = setInterval(() => {
        timeLeft--;
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            timerElement.textContent = "Sắp hoàn tất...";
        } else {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;

            if (timeLeft > 60) {
                timerElement.textContent = `Còn khoảng ${Math.ceil(timeLeft / 60)} phút`;
            } else {
                timerElement.textContent = `Còn khoảng ${timeLeft} giây`;
            }
        }
    }, 1000);

    // 3. Stepper Simulation Logic
    const steps = document.querySelectorAll('.step-item');
    const lines = document.querySelectorAll('.step-line');
    let currentStep = 0;

    // Simulate progress every 3 seconds for demo
    // In real app, this would be: setInterval(checkApiStatus, 3000)
    const progressInterval = setInterval(() => {
        if (currentStep >= steps.length - 1) {
            clearInterval(progressInterval);
            return;
        }

        // Mark current as completed
        steps[currentStep].classList.remove('active');
        steps[currentStep].classList.add('completed');

        // Color the line
        if (currentStep < lines.length) {
            lines[currentStep].classList.add('completed');
        }

        // Move to next
        currentStep++;
        steps[currentStep].classList.add('active');

        // Optional: Update text based on step?

    }, 5000); // 5 seconds per step

    // --- Sidebar Toggle ---
    const toggleBtn = document.querySelector('.menu-toggle');
    const appContainer = document.querySelector('.app-container');

    if (toggleBtn && appContainer) {
        toggleBtn.addEventListener('click', () => {
            appContainer.classList.toggle('sidebar-collapsed');
        });
    }
});
