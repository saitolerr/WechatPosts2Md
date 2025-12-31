# 微信公众号转 Markdown

<p align="center">
  <img src="icons/icon128.png" alt="Logo" width="80">
</p>

<p align="center">
  一键将微信公众号文章转换为 Markdown 格式，保留段落格式和图片。
</p>

## ✨ 功能特性

- 📝 提取文章标题、作者、发布时间
- 📄 正文内容自动转换为 Markdown 格式
- 🎯 保留段落空行，还原原文排版
- 🖼️ 图片链接自动提取
- 📊 支持标题、列表、引用、代码块、表格等元素
- ⚙️ 可选择是否包含元信息

## 📦 安装方法

### 方式一：开发者模式加载（推荐）

1. 下载并解压本插件

2. 打开浏览器扩展管理页面：
   - **Chrome**: `chrome://extensions/`
   - **Edge**: `edge://extensions/`

3. 开启右上角的 **「开发者模式」**

4. 点击 **「加载已解压的扩展程序」**

5. 选择本插件文件夹（包含 `manifest.json` 的目录）

6. 安装完成！✅

### 方式二：从商店安装

- Edge 商店：[点此下载](https://microsoftedge.microsoft.com/addons/detail/nfopjnegiibpjdilhophlbnanbkbejda)   
>  store_assets  目录下为上架备案时所需素材

## 🚀 使用方法

1. 在浏览器中打开微信公众号文章页面
   > 💡 可以从微信复制文章链接，粘贴到浏览器打开
   
2. 点击浏览器工具栏中的插件图标

3. 点击 **「开始转换」** 按钮

4. 转换完成后：
   - 点击 **「复制 Markdown」** 复制到剪贴板
   - 点击 **「下载文件」** 保存为 `.md` 文件

## ⚠️ 注意事项

### 关于评论区

微信公众号评论区只能在微信客户端内查看，浏览器打开的文章页面**无法获取评论内容**。这是微信的限制。

### 关于图片

- 图片使用微信原始链接，可以正常显示
- 如果图片失效，可能需要手动下载保存

## 📁 文件结构

```
Webpage2Md/
├── manifest.json        # 插件配置文件
├── popup.html/css/js    # 弹窗界面
├── content.js/css       # 内容脚本（注入到页面）
├── background.js        # 后台服务脚本
├── icons/               # 插件图标
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
├── store_assets/        # 商店素材
│   ├── icon_300x300.png
│   └── promo_440x280.png
└── README.md
```

## 🛠️ 开发

本插件使用 **Chrome Extension Manifest V3** 开发，兼容 Chrome、Edge 等 Chromium 内核浏览器。

### 本地调试

1. 修改代码后，在扩展管理页面点击 **刷新** 按钮
2. 重新打开目标页面测试

### 生成图标

```bash
python generate_icons.py
```

### 生成商店素材

```bash
python generate_store_assets.py
```

## 📄 License

MIT

---

<p align="center">
  Made with ❤️ for WeChat Article Lovers
</p>
