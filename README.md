# Gemini LINE ChatBot

這個專案是一個基於 Python 與 Flask 的 LINE 聊天機器人，利用 LINE Messaging API 與 Google Gemini 2.0 模型，提供專業且快速的 AI 自動回覆服務。

<img src="https://github.com/EVANLIN2001/AI-LINE-ChatBot/blob/main/image/S__74170384_0.jpg?raw=true" alt="Demo 1" width="250"><br>

## 功能特色

### AI 專業回覆
利用 Google Gemini 2.0 模型生成即時且專業的回應，適合 AI 領域問答與對話。

### 非同步訊息處理
透過多執行緒設計，確保 LINE Webhook 不會超時，提升使用者體驗。

### 快速部署
使用 Docker 與 Fly.io 快速部署，輕鬆將服務上線。

### 記憶功能
使用者對話將自動儲存在短期記憶中，讓 Gemini 回覆更具上下文，提升對話連貫性與準確度。

<img src="https://github.com/EVANLIN2001/AI-LINE-ChatBot/blob/main/image/S__74170385_0.jpg?raw=true" alt="Demo 2" width="500">

## 技術棧

- **後端框架**：Python, Flask
- **LINE 串接**：LINE Messaging API, LINE Bot SDK
- **AI 模型串接**：Google Gemini API
- **部署平台**：Fly.io, Docker

## 專案挑戰
**本專案雖然程式架構簡單，功能明確，但實作過程中包含**
- LINE Webhook 即時回應與 timeout 除錯
- Gemini 模型回應延遲處理與非同步設計
- 雲端部署環境（Fly.io）下的模組安裝、環境變數管理
- Docker 建構與機器啟動策略調整

## 此專案涵蓋 LINE Bot 開發、AI 模型串接與 Fly.io 雲端部署，結構簡潔，適合作為學習與實作的入門範例。
