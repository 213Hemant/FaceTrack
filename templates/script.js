const startVideoBtn = document.getElementById('start-video');
const stopVideoBtn = document.getElementById('stop-video');
const videoFeed = document.getElementById('video-feed');
const spinner = document.getElementById('spinner');
const closeWebAppBtn = document.getElementById('close-webapp');
const attendanceStatus = document.getElementById('status');
const attendanceList = document.getElementById('attendance-list');

// Start video feed
startVideoBtn.addEventListener('click', () => {
    videoFeed.src = "{{ url_for('video_feed') }}";  // Start video feed
    videoFeed.style.display = 'block';
    spinner.style.display = 'none';  // Hide spinner
    startVideoBtn.style.display = 'none';
    stopVideoBtn.style.display = 'inline-block';
});

// Stop video feed
stopVideoBtn.addEventListener('click', () => {
    videoFeed.src = "";  // Stop video feed
    videoFeed.style.display = 'none';
    spinner.style.display = 'block';  // Show spinner again
    startVideoBtn.style.display = 'inline-block';
    stopVideoBtn.style.display = 'none';
});

// Close the web application
closeWebAppBtn.addEventListener('click', () => {
    window.close(); // Close the current window/tab
});
