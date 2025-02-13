import functions_framework
from google.cloud import storage
import google.generativeai as genai
import vertexai
import tempfile
import os

# 初始化 Google Cloud 服務
project_id = "aci-wesley-playground"
location = "asia-east1"
vertexai.init(project=project_id, location=location)
#set up gemini api key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def process_audio(audio_path, file_name):
    """使用 Gemini 處理音訊檔案並生成結構化的會議記錄"""
    # 初始化 Gemini 模型
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # 準備音訊檔案
    audio_file = genai.upload_file(audio_path,mime_type="audio/m4a")
    print(f"audio_path:{audio_path}")
    
    # 第一步：生成原始逐字稿
    transcript_prompt = ["辨識這個音檔，要辨識出每位使用者，並標記為「Speaker A」, 「Speaker B」等, 將每位使用者的對話內容轉換為逐字稿，並在每段對話前加上開始時間戳。", audio_file]
    transcript_response = model.generate_content(transcript_prompt)
    raw_transcript = transcript_response.text

    # 第二步：使用結構化提示詞處理逐字稿
    summary_prompt = f"""請將以下會議逐字稿轉換為一份條列式摘要，
內容需包含：
- 會議主題
- 主要討論重點 (以條列方式呈現)
- 決議事項與行動方案 (以條列方式呈現，包含負責人或單位)

逐字稿內容：
{raw_transcript}"""

    # 生成結構化摘要
    summary_response = model.generate_content(summary_prompt)
    structured_summary = summary_response.text
    
    # 返回原始逐字稿和結構化摘要
    return {
        "raw_transcript": raw_transcript,
        "structured_summary": structured_summary
    }

@functions_framework.cloud_event
def process_gcs_audio(cloud_event):
    """Cloud Function 入口點，處理 GCS 觸發事件"""
    
    # 解析 GCS 事件數據
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]
    
    # 檢查檔案類型
    if not file_name.lower().endswith(('.mp3', '.wav', '.m4a')):
        print(f"不支援的檔案類型: {file_name}")
        return
    
    # 初始化 Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    # 下載音訊檔案到臨時目錄
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        blob.download_to_filename(temp_audio.name)
        audio_path = temp_audio.name
        print(f"audio_path:{audio_path}")
    
    try:
        # 處理音訊並生成逐字稿和摘要
        result = process_audio(audio_path, file_name)
        print(f"result:{result}")
        
        # 儲存原始逐字稿
        transcript_filename = f"{os.path.splitext(file_name)[0]}_transcript.txt"
        transcript_blob = bucket.blob(transcript_filename)
        transcript_blob.upload_from_string(result["raw_transcript"])
        
        # 儲存結構化摘要
        summary_filename = f"{os.path.splitext(file_name)[0]}_summary.txt"
        summary_blob = bucket.blob(summary_filename)
        summary_blob.upload_from_string(result["structured_summary"])
        
        print(f"已成功生成逐字稿和摘要:")
        print(f"逐字稿檔案: {transcript_filename}")
        print(f"摘要檔案: {summary_filename}")
        print("\n摘要內容:")
        print(result["structured_summary"])
        
    finally:
        # 清理臨時檔案
        os.unlink(audio_path)
    
    return "處理完成"