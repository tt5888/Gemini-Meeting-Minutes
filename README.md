# Gemini-Meeting-Minutes
## 這個專案使用gemini-2.0-flash，辨識音檔後產生兩份文件，產生逐字稿與會議摘要。

### Google AI 的工具分類
![Google AI 的工具分類](https://github.com/tt5888/Gemini-Meeting-Minutes/blob/main/Google%20AIs.png?raw=true)

### 架構圖
![架構圖](https://github.com/tt5888/Gemini-Meeting-Minutes/blob/main/Architecture%20diagram.png?raw=true)



逐字稿會辨識出每位使用者，並標記為「Speaker A」, 「Speaker B」等, 將每位使用者的對話內容轉換為逐字稿，並在每段對話前加上開始時間戳。


會議摘要採條列式摘要，
內容包含：
- 會議主題
- 主要討論重點 (以條列方式呈現)
- 決議事項與行動方案 (以條列方式呈現，包含負責人或單位


### 結果展示
#### 逐字稿
![逐字稿](https://github.com/tt5888/Gemini-Meeting-Minutes/blob/main/Dr.%20Chen_transcript.png?raw=true)

#### 會議摘要
![會議摘要](https://github.com/tt5888/Gemini-Meeting-Minutes/blob/main/Dr.%20Chen_summary.png?raw=true)

## Reference：
[Transcript an audio file with Gemini 1.5 Pro](https://cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-gemini-audio-transcription#generativeaionvertexai_gemini_audio_transcription-python)
