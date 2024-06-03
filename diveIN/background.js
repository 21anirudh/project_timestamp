chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === "searchTopic") {
      const topic = request.topic;
      const videoTitle = document.querySelector("title").textContent;
      const videoDescription = document.querySelector("meta[name='description']").getAttribute("content");
      const transcript = getTranscript(); // implement this function to get the video transcript
      const timestamp = searchTranscript(transcript, topic);
      if (timestamp) {
        const videoPlayer = document.querySelector("#movie_player");
        videoPlayer.currentTime = timestamp;
      }
    }
  });
  
  function getTranscript() {
    // implement this function to get the video transcript
    // you can use YouTube's API or a third-party library to achieve this
  }
  
  function searchTranscript(transcript, topic) {
    // implement this function to search the transcript for the topic
    // return the timestamp if found, otherwise return null
  }