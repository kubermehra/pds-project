var tag = document.createElement('script');
tag.src = "https://www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var video=document.getElementsByTagName('h1')[0];
id=video.id

var lastSentTime = 0;
function onYouTubePlayerAPIReady() {
    player = new YT.Player('video-frame', {
    width: '1239px',
    height:'695px',
    videoId: id,
    playerVars: {
        'autoplay': 0, // This is optional, 1 for autoplay when the video loads
        'controls': 1, // This is optional, 0 to hide player controls
        'fs': 1 // Allows the fullscreen button
    },
    events: {
        'onStateChange': onPlayerStateChange
    }
});
}

function onPlayerStateChange(events){
    if (events.data == YT.PlayerState.PLAYING) {
        setInterval(sendCurrentTime, 20000); // Send current time every 10 seconds
    }
}

function sendCurrentTime() {
    var currentTime = Math.round(player.playerInfo.currentTime);
    if (currentTime !== lastSentTime) {
        lastSentTime = currentTime;
        // Send current time to Flask backend
        fetch('/update_time', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ video_id: id, current_time: currentTime })
        }).then(response => {
            console.log('Current time sent successfully:', currentTime);
        }).catch(error => {
            console.error('Error sending current time:', error);
        });
    }
}
function startVideoAt30Seconds(videoId,famous_segment) {
    var startSeconds = parseInt(famous_segment);
    player.loadVideoById({
        'videoId': videoId,
        'startSeconds': startSeconds
        
    });
}