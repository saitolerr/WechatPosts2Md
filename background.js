// Background Service Worker

// 监听安装事件
chrome.runtime.onInstalled.addListener(() => {
  console.log('微信公众号转 Markdown 插件已安装');
});

// 处理下载请求
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'downloadImage') {
    chrome.downloads.download({
      url: request.url,
      filename: request.filename,
      saveAs: false
    }, (downloadId) => {
      sendResponse({ success: true, downloadId });
    });
    return true;
  }
});

