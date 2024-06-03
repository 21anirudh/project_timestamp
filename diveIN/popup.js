document.addEventListener("DOMContentLoaded", function () {
    const topicInput = document.getElementById("topic-input");
    const searchButton = document.getElementById("search-button");
  
    searchButton.addEventListener("click", function () {
      const topic = topicInput.value.trim();
      if (topic) {
        chrome.runtime.sendMessage({ action: "searchTopic", topic: topic });
      }
    });
  });