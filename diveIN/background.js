function extractVideoId(url) {
  const match = url.match(/[?&]v=([^&]+)/);
  return match && match[1];
}

chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
  const currentTab = tabs[0];
  const currentUrl = currentTab.url;

  if (currentUrl.includes('youtube.com/watch')) {
      const videoId = extractVideoId(currentUrl);

      fetch('http://localhost:5000/extract_timestamp', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              video_url: currentUrl,
              topic: 'YOUR_TOPIC',
          }),
      })
      .then(response => response.json())
      .then(data => {
          const timestamp = data.timestamp;
          if (timestamp) {
              const videoUrl = `https://www.youtube.com/watch?v=${videoId}&t=${timestamp}`;
              window.location.href = videoUrl;
          } else {
              console.error('Timestamp not found.');
          }
      })
      .catch(error => console.error('Error:', error));
  } else {
      console.error('The current tab is not a YouTube video.');
  }
});
