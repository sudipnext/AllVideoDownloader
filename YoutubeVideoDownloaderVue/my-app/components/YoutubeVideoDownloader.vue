<script>
import $ from 'jquery';

export default {
  mounted() {
    $(".click-btn-down").click(() => {
      const link = $(".link").val();
      const format = $(".formte").children("option:selected").val();
      const src = `${link}=${format}`;
      this.downloadVideo(link, format);
    });
  },
  methods: {
    downloadVideo(link, format) {
      $('.download-video').html(
        `<iframe style="width:100%;height:60px;border:0;overflow:hidden;" scrolling="no" src="https://loader.to/api/button/?url=${link}&f=${format}"></iframe>`
      );
    },
  },
};
</script>

<template>
    <div style="position: relative; background-image: linear-gradient(to right, #2101b9, #005eec, #0090f8, #00bcee, #00e3e3); min-height: 99vh;">
      <div id="hd">
        <div class="columns-md-6 ring-offset-0  m-10">
          <div class="card">
            <div class="card-header bg-info">
              <h5 class="text-center">YouTube Video Downloader</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label class="text-weight"><b>Enter YT Video Link:</b></label>
                    <input type="text" name="link" class="form-control link" required />
                  </div>
                </div>
              </div>
              <form class="form-download">
                <div class="row">
                  <div class="col-md-12">
                    <div class="form-group">
                      <label class="text-weight"><b>Select Video Format:</b></label>
                      <select class="form-control formte" required>
                        <option selected disabled>Select Video Format</option>
                        <option value="mp3">Mp3</option>
                        <option value="mp4a">144 Mp4</option>
                        <option value="360">360 Mp4</option>
                        <option value="480">480 Mp4</option>
                        <option value="720">720 Mp4</option>
                        <option value="1080">1080 Mp4</option>
                        <option value="4k">4k Mp4</option>
                        <option value="8k">8k Mp4</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12">
                    <div class="form-group mt-4 download-video">
                      <button class="btn btn-success btn-block click-btn-down" type="submit">Click Here</button>
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
  
        <div class="custom-shape-divider-bottom-1610026357">
          <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
            <path
              d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
              class="shape-fill"
            ></path>
          </svg>
        </div>
      </div>
    </div>
  </template>
  