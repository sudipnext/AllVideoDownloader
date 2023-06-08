$(document).ready(function () {
  $("#downloadBtn").click(function () {
    var videoUrl = $("#videoUrl").val();
    if (videoUrl.trim() === "") {
      alert("Please enter a valid YouTube video URL");
      return;
    }

    // Create an invisible <a> element
    var link = document.createElement("a");
    link.style.display = "none";

    // Set the download URL
    link.href = "https://www.youtubeinmp3.com/fetch/?video=" + videoUrl;

    // Set the file name
    link.download = "video.mp4";

    // Append the link to the document body
    document.body.appendChild(link);

    // Click the link to start the download
    link.click();

    // Remove the link from the document body
    document.body.removeChild(link);
  });
});
