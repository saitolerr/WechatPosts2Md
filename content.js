// 微信公众号文章转 Markdown - Content Script

// 监听来自 popup 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'convert') {
    convertToMarkdown(request.options)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // 保持消息通道开放
  }
});

// 主转换函数
async function convertToMarkdown(options) {
  const { imageMode, includeMetadata } = options;
  
  // 提取文章信息
  const title = extractTitle();
  const author = extractAuthor();
  const publishTime = extractPublishTime();
  const content = await extractContent(imageMode);
  
  // 构建 Markdown
  let markdown = '';
  
  // 元信息
  if (includeMetadata) {
    markdown += `# ${title}\n\n`;
    markdown += `> **作者**: ${author}  \n`;
    markdown += `> **发布时间**: ${publishTime}  \n`;
    markdown += `> **原文链接**: ${window.location.href}\n\n`;
    markdown += `---\n\n`;
  } else {
    markdown += `# ${title}\n\n`;
  }
  
  // 正文内容
  markdown += content.markdown;
  
  return {
    success: true,
    markdown: markdown,
    title: title,
    images: content.images
  };
}

// 提取标题
function extractTitle() {
  const titleEl = document.getElementById('activity-name') || 
                  document.querySelector('.rich_media_title');
  return titleEl ? titleEl.textContent.trim() : '未知标题';
}

// 提取作者
function extractAuthor() {
  const authorEl = document.getElementById('js_name') || 
                   document.querySelector('.rich_media_meta_nickname');
  return authorEl ? authorEl.textContent.trim() : '未知作者';
}

// 提取发布时间
function extractPublishTime() {
  const timeEl = document.getElementById('publish_time') || 
                 document.querySelector('.rich_media_meta_date');
  return timeEl ? timeEl.textContent.trim() : '未知时间';
}

// 预处理：在段落之间插入空行标记
function markBlankLines(element) {
  // 微信公众号的段落空行是通过 CSS margin 实现的，不是空元素
  // 所以我们需要在每个"内容段落"后面插入空行标记
  
  // 获取直接子元素中的 section（微信用 section 作为段落容器）
  const topLevelSections = element.querySelectorAll(':scope > section');
  
  topLevelSections.forEach(section => {
    // 检查这个 section 是否有实际文本内容
    const text = section.textContent.trim();
    if (text) {
      // 有内容的段落，在末尾添加空行标记
      section.setAttribute('data-add-blank', 'true');
    }
  });
  
  // 也处理直接在 js_content 下的 p 标签
  const topLevelPs = element.querySelectorAll(':scope > p');
  topLevelPs.forEach(p => {
    const text = p.textContent.trim();
    if (text) {
      p.setAttribute('data-add-blank', 'true');
    }
  });
}

// 提取正文内容
async function extractContent(imageMode) {
  const contentEl = document.getElementById('js_content');
  if (!contentEl) {
    throw new Error('未找到文章内容');
  }
  
  // 克隆节点以避免修改原页面
  const clone = contentEl.cloneNode(true);
  
  // 预处理：标记空行
  markBlankLines(clone);
  
  // 处理图片
  const images = [];
  const imgElements = clone.querySelectorAll('img');
  let imgIndex = 0;
  
  for (const img of imgElements) {
    const src = img.getAttribute('data-src') || img.src;
    if (!src || src.startsWith('data:')) continue;
    
    imgIndex++;
    const filename = `image_${imgIndex}.png`;
    
    if (imageMode === 'download') {
      // 下载模式：使用相对路径
      images.push({ url: src, filename: filename });
      img.setAttribute('data-md-src', `./images/${filename}`);
    } else if (imageMode === 'base64') {
      // Base64 模式：转换为 base64
      try {
        const base64 = await imageToBase64(src);
        img.setAttribute('data-md-src', base64);
      } catch (e) {
        console.error('图片转 base64 失败:', e);
        img.setAttribute('data-md-src', src);
      }
    } else {
      // 原链接模式
      img.setAttribute('data-md-src', src);
    }
  }
  
  // 转换 HTML 为 Markdown
  const markdown = htmlToMarkdown(clone);
  
  return { markdown, images };
}

// 图片转 Base64
async function imageToBase64(url) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);
      try {
        const dataURL = canvas.toDataURL('image/png');
        resolve(dataURL);
      } catch (e) {
        reject(e);
      }
    };
    img.onerror = reject;
    img.src = url;
  });
}

// HTML 转 Markdown
function htmlToMarkdown(element) {
  let markdown = '';
  
  function processNode(node, context = {}) {
    if (node.nodeType === Node.TEXT_NODE) {
      let text = node.textContent;
      // 清理多余空白，但保留必要的换行
      if (!context.preserveWhitespace) {
        text = text.replace(/\s+/g, ' ');
      }
      return text;
    }
    
    if (node.nodeType !== Node.ELEMENT_NODE) {
      return '';
    }
    
    const tag = node.tagName.toLowerCase();
    const children = Array.from(node.childNodes);
    
    // 跳过隐藏元素和脚本
    if (node.style.display === 'none' || 
        node.style.visibility === 'hidden' ||
        ['script', 'style', 'noscript'].includes(tag)) {
      return '';
    }
    
    // 检查是否需要在此元素后添加空行
    const shouldAddBlank = node.getAttribute && node.getAttribute('data-add-blank') === 'true';
    
    let content = '';
    for (const child of children) {
      content += processNode(child, context);
    }
    content = content.trim();
    
    switch (tag) {
      // 标题
      case 'h1':
        return `\n## ${content}\n\n`;
      case 'h2':
        return `\n### ${content}\n\n`;
      case 'h3':
        return `\n#### ${content}\n\n`;
      case 'h4':
      case 'h5':
      case 'h6':
        return `\n##### ${content}\n\n`;
      
      // 段落
      case 'p':
        if (!content) return '';
        // 需要额外空行的段落
        if (shouldAddBlank) {
          return `${content}\n\n\n`;
        }
        return `${content}\n\n`;
      
      // 换行
      case 'br':
        return '\n';
      
      // 粗体
      case 'strong':
      case 'b':
        return content ? `**${content}**` : '';
      
      // 斜体
      case 'em':
      case 'i':
        return content ? `*${content}*` : '';
      
      // 删除线
      case 'del':
      case 's':
      case 'strike':
        return content ? `~~${content}~~` : '';
      
      // 链接
      case 'a':
        const href = node.getAttribute('href') || '';
        if (href && !href.startsWith('javascript:')) {
          return `[${content}](${href})`;
        }
        return content;
      
      // 图片
      case 'img':
        const src = node.getAttribute('data-md-src') || 
                    node.getAttribute('data-src') || 
                    node.src;
        const alt = node.alt || '图片';
        if (src && !src.startsWith('data:image/gif;base64,R0lGOD')) { // 跳过占位图
          return `\n![${alt}](${src})\n\n`;
        }
        return '';
      
      // 列表
      case 'ul':
        return `\n${processListItems(node, '-')}\n`;
      case 'ol':
        return `\n${processListItems(node, '1.')}\n`;
      case 'li':
        return content;
      
      // 引用
      case 'blockquote':
        const lines = content.split('\n').filter(line => line.trim());
        return `\n${lines.map(line => `> ${line}`).join('\n')}\n\n`;
      
      // 代码
      case 'code':
        if (node.parentElement?.tagName.toLowerCase() === 'pre') {
          return content;
        }
        return content ? `\`${content}\`` : '';
      
      // 代码块
      case 'pre':
        const codeContent = content.replace(/`/g, '');
        return `\n\`\`\`\n${codeContent}\n\`\`\`\n\n`;
      
      // 水平线
      case 'hr':
        return '\n---\n\n';
      
      // 表格
      case 'table':
        return processTable(node);
      
      // 分区元素，直接返回内容
      case 'div':
      case 'section':
        if (!content) return '';
        // 需要额外空行的 section（顶层段落）
        if (shouldAddBlank) {
          return `${content}\n\n\n`;
        }
        return `${content}\n`;
      case 'article':
      case 'span':
      case 'main':
        return content ? `${content}\n` : '';
      
      default:
        return content;
    }
  }
  
  // 处理列表项
  function processListItems(listNode, marker) {
    const items = listNode.querySelectorAll(':scope > li');
    let result = '';
    items.forEach((item, index) => {
      const itemContent = processNode(item).trim();
      const prefix = marker === '1.' ? `${index + 1}.` : marker;
      result += `${prefix} ${itemContent}\n`;
    });
    return result;
  }
  
  // 处理表格
  function processTable(tableNode) {
    const rows = tableNode.querySelectorAll('tr');
    if (rows.length === 0) return '';
    
    let result = '\n';
    rows.forEach((row, rowIndex) => {
      const cells = row.querySelectorAll('td, th');
      const cellContents = Array.from(cells).map(cell => {
        return processNode(cell).trim().replace(/\|/g, '\\|').replace(/\n/g, ' ');
      });
      result += `| ${cellContents.join(' | ')} |\n`;
      
      // 添加表头分隔行
      if (rowIndex === 0) {
        result += `| ${cellContents.map(() => '---').join(' | ')} |\n`;
      }
    });
    result += '\n';
    return result;
  }
  
  markdown = processNode(element);
  
  // 清理过多的空行（保留最多2个空行）
  markdown = markdown
    .replace(/\n{5,}/g, '\n\n\n\n')  // 最多保留2个空行
    .replace(/^\s+/, '')
    .replace(/\s+$/, '\n');
  
  return markdown;
}

