// 存储转换结果
let convertedMarkdown = '';
let articleTitle = '';

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
  // 检查当前页面是否是微信公众号文章
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const statusEl = document.getElementById('status');
  
  if (!tab.url || !tab.url.includes('mp.weixin.qq.com')) {
    statusEl.className = 'status warning';
    statusEl.textContent = '⚠️ 请在微信公众号文章页面使用此插件';
    document.getElementById('convertBtn').disabled = true;
  } else {
    statusEl.className = 'status info';
    statusEl.textContent = '✨ 检测到微信公众号文章，可以开始转换';
  }

  // 加载保存的设置
  chrome.storage.sync.get(['imageMode', 'includeMetadata'], (result) => {
    // 默认使用原链接模式
    const mode = result.imageMode || 'original';
    document.querySelector(`input[name="imageMode"][value="${mode}"]`).checked = true;
    if (result.includeMetadata !== undefined) {
      document.getElementById('includeMetadata').checked = result.includeMetadata;
    }
  });
});

// 保存设置
document.querySelectorAll('input[name="imageMode"]').forEach(radio => {
  radio.addEventListener('change', (e) => {
    chrome.storage.sync.set({ imageMode: e.target.value });
  });
});

document.getElementById('includeMetadata').addEventListener('change', (e) => {
  chrome.storage.sync.set({ includeMetadata: e.target.checked });
});

// 转换按钮
document.getElementById('convertBtn').addEventListener('click', async () => {
  const btn = document.getElementById('convertBtn');
  const resultEl = document.getElementById('result');
  const errorEl = document.getElementById('error');
  
  // 获取选项
  const imageMode = document.querySelector('input[name="imageMode"]:checked').value;
  const includeMetadata = document.getElementById('includeMetadata').checked;
  
  // 显示加载状态
  btn.classList.add('loading');
  btn.disabled = true;
  resultEl.classList.add('hidden');
  errorEl.classList.add('hidden');
  
  try {
    // 获取当前标签页
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // 向 content script 发送消息
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'convert',
      options: { imageMode, includeMetadata }
    });
    
    if (response.success) {
      convertedMarkdown = response.markdown;
      articleTitle = response.title;
      resultEl.classList.remove('hidden');
      
      // 如果选择下载图片模式，触发图片下载
      if (imageMode === 'download' && response.images && response.images.length > 0) {
        for (const img of response.images) {
          await downloadImage(img.url, img.filename);
        }
      }
    } else {
      throw new Error(response.error || '转换失败');
    }
  } catch (error) {
    errorEl.textContent = `❌ ${error.message}`;
    errorEl.classList.remove('hidden');
  } finally {
    btn.classList.remove('loading');
    btn.disabled = false;
  }
});

// 复制按钮
document.getElementById('copyBtn').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(convertedMarkdown);
    const btn = document.getElementById('copyBtn');
    const originalText = btn.textContent;
    btn.textContent = '✅ 已复制';
    setTimeout(() => {
      btn.textContent = originalText;
    }, 2000);
  } catch (error) {
    alert('复制失败：' + error.message);
  }
});

// 下载按钮
document.getElementById('downloadBtn').addEventListener('click', () => {
  const filename = sanitizeFilename(articleTitle || 'article') + '.md';
  downloadFile(convertedMarkdown, filename);
});

// 下载文件
function downloadFile(content, filename) {
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  
  chrome.downloads.download({
    url: url,
    filename: filename,
    saveAs: true
  });
}

// 下载图片
async function downloadImage(url, filename) {
  try {
    chrome.downloads.download({
      url: url,
      filename: `images/${filename}`,
      saveAs: false
    });
  } catch (error) {
    console.error('下载图片失败:', error);
  }
}

// 清理文件名
function sanitizeFilename(name) {
  return name
    .replace(/[\\/:*?"<>|]/g, '_')
    .replace(/\s+/g, '_')
    .substring(0, 100);
}

