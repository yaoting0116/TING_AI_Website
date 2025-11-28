// static/js/responsive.js
(function () {
  function applyResponsive() {
    try {
      // 確保所有 img 元素都有可縮放樣式（CSS 已處理，但作為備援）
      var imgs = document.getElementsByTagName('img');
      for (var i = 0; i < imgs.length; i++) {
        var img = imgs[i];
        img.style.maxWidth = img.style.maxWidth || '100%';
        img.style.height = img.style.height || 'auto';
        img.style.display = img.style.display || 'block';
      }

      // audio 元素也寬度100%
      var audios = document.getElementsByTagName('audio');
      for (var j = 0; j < audios.length; j++) {
        var a = audios[j];
        a.style.width = a.style.width || '100%';
      }

      // 如果頁面中有 <pre> 或長單行文字，允許換行避免爆版
      var pres = document.getElementsByTagName('pre');
      for (var k = 0; k < pres.length; k++) {
        pres[k].style.whiteSpace = 'pre-wrap';
        pres[k].style.wordBreak = 'break-word';
      }

      // 可選：若 template 顯示多個 {{ image.name }} 文字，而你在同頁面同時有 image_info 傳入，
      // 這個 JS 無法安全地把文字替換成 <img>（需要 template 支援），因此不在這做 aggressive DOM rewrite。
    } catch (e) {
      // silent fail
      console && console.error && console.error('responsive.js error', e);
    }
  }

  if (document.readyState !== 'loading') {
    applyResponsive();
  } else {
    document.addEventListener('DOMContentLoaded', applyResponsive);
  }
})();
