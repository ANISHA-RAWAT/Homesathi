/**
 * pp-media.js
 * Shared media upload panel definition + upload interaction logic.
 * Depends on: pp-helpers.js
 */
'use strict';

var PP_MEDIA = (function () {

  /* ── PANEL DEFINITION ────────────────────────────────────── */
  function mediaPanel() {
    return {
      id: 'media', title: 'Photos & Video', icon: '📸',
      html:
        '<div class="pp-panel-intro">Listings with photos get <strong>3× more inquiries</strong>. Add up to 15 photos and a video tour.</div>' +
        '<div class="pp-field field-full">' +
          '<label class="pp-label">Property Photos<span class="req-star">*</span></label>' +
          '<div class="drop-zone" id="dropZone">' +
            '<input type="file" name="property_images" id="photoInput" multiple accept="image/*" class="drop-input">' +
            '<div class="drop-zone-content" id="dropZoneContent">' +
              '<div class="dz-icon">📷</div>' +
              '<p class="dz-title">Drag &amp; drop photos here</p>' +
              '<p class="dz-sub">or <span class="dz-link">click to browse</span></p>' +
              '<p class="dz-note">JPG · PNG · WEBP · Max 5 MB each · Up to 15 photos</p>' +
            '</div>' +
          '</div>' +
          '<div class="photo-preview-grid" id="photoPreviewGrid"></div>' +
        '</div>' +
        '<div class="pp-field field-full">' +
          '<label class="pp-label">Property Video <span class="opt-tag">optional</span></label>' +
          '<p class="field-hint" style="margin-bottom:10px">A walkthrough video gets <strong>5× more engagement</strong>. MP4 recommended · Max 100 MB</p>' +
          '<label class="file-btn-label" for="videoInput"><span>🎬</span> <span id="videoFileName">Choose video file…</span></label>' +
          '<input type="file" name="property_video" id="videoInput" accept="video/*" class="hidden-file-input">' +
          '<div id="videoPreview" style="margin-top:12px;display:none;">' +
            '<video id="videoPlayer" controls style="width:100%;border-radius:10px;max-height:240px;"></video>' +
          '</div>' +
        '</div>',
    };
  }

  /* ── UPLOAD INTERACTION ──────────────────────────────────── */
  function initImageUpload() {
    var dropZone     = document.getElementById('dropZone');
    var photoInput   = document.getElementById('photoInput');
    var previewGrid  = document.getElementById('photoPreviewGrid');
    var videoInput   = document.getElementById('videoInput');
    var videoName    = document.getElementById('videoFileName');
    var videoPreview = document.getElementById('videoPreview');
    var videoPlayer  = document.getElementById('videoPlayer');

    if (!dropZone || !photoInput) return;

    var files = [];

    function renderPreviews() {
      previewGrid.innerHTML = '';
      files.forEach(function (file, i) {
        var reader = new FileReader();
        reader.onload = function (e) {
          var div = document.createElement('div');
          div.className = 'photo-thumb';
          div.innerHTML =
            '<img src="' + e.target.result + '" alt="Photo ' + (i + 1) + '">' +
            '<button type="button" class="photo-thumb-remove" data-index="' + i + '">✕</button>' +
            '<span class="photo-thumb-num">' + (i + 1) + '</span>';
          previewGrid.appendChild(div);
          div.querySelector('.photo-thumb-remove').addEventListener('click', function () {
            files.splice(parseInt(this.dataset.index, 10), 1);
            syncFileInput();
            renderPreviews();
          });
        };
        reader.readAsDataURL(file);
      });
      var content = document.getElementById('dropZoneContent');
      if (content) content.style.display = files.length > 0 ? 'none' : '';
    }

    function syncFileInput() {
      var dt = new DataTransfer();
      files.forEach(function (f) { dt.items.add(f); });
      photoInput.files = dt.files;
    }

    function addFiles(newFiles) {
      for (var i = 0; i < newFiles.length; i++) {
        if (files.length >= 15) { alert('Maximum 15 photos allowed.'); break; }
        if (newFiles[i].size > 5 * 1024 * 1024) { alert(newFiles[i].name + ' exceeds 5 MB limit.'); continue; }
        files.push(newFiles[i]);
      }
      syncFileInput();
      renderPreviews();
    }

    dropZone.addEventListener('click', function () { photoInput.click(); });
    photoInput.addEventListener('change', function () { addFiles(this.files); });
    dropZone.addEventListener('dragover', function (e) { e.preventDefault(); dropZone.classList.add('drag-over'); });
    dropZone.addEventListener('dragleave', function () { dropZone.classList.remove('drag-over'); });
    dropZone.addEventListener('drop', function (e) {
      e.preventDefault(); dropZone.classList.remove('drag-over'); addFiles(e.dataTransfer.files);
    });

    if (videoInput && videoName) {
      videoInput.addEventListener('change', function () {
        if (this.files[0]) {
          videoName.textContent = this.files[0].name;
          if (videoPreview && videoPlayer) {
            videoPlayer.src = URL.createObjectURL(this.files[0]);
            videoPreview.style.display = 'block';
          }
        }
      });
    }
  }

  return {
    mediaPanel:      mediaPanel,
    initImageUpload: initImageUpload,
  };
})();