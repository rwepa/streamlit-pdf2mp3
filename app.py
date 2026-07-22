# File     : app.py
# Topic    : PDF 轉 MP3 語音朗讀器 (Streamlit + Edge-TTS)
# Date     : 2026.07.20
# Author   : Ming-Chang Lee
# YouTube  : https://www.youtube.com/@alan9956
# RWEPA    : http://rwepa.blogspot.tw/
# GitHub   : https://github.com/rwepa
# Email    : alan9956@gmail.com

# pip install streamlit pypdf edge-tts langid
# ai-generated: google antigravity

import asyncio
import os
import re
import tempfile
import langid
import streamlit as st
from pypdf import PdfReader
import edge_tts

# -----------------------------------------------------------------------------
# 1. 頁面配置與標題
# -----------------------------------------------------------------------------
st.set_page_config(page_title="PDF 轉 MP3 語音朗讀器", page_icon="🎧", layout="wide")
st.title("🎧 RWEPA | PDF 轉 MP3 語音朗讀工具")
st.caption("免 API Key | 自動辨識中英文 | 免費 Edge-TTS 高品質發音")
st.caption("RWEPA: https://rwepa.blogspot.com/")
st.caption("GitHub: https://github.com/rwepa")
st.caption("Email: alan9956@gmail.com")

# -----------------------------------------------------------------------------
# 2. 聲音角色資料庫 (包含 4 種男/女生音色)
# -----------------------------------------------------------------------------
VOICES = {
    "zh": {  # 中文語音選項
        "女生 1 (曉曉 - 台灣)": "zh-TW-HsiaoChenNeural",
        "女生 2 (曉雙 - 中國大陸)": "zh-CN-XiaoxiaoNeural",
        "男生 1 (雲哲 - 台灣)": "zh-TW-YunJheNeural",
        "男生 2 (雲希 - 中國大陸)": "zh-CN-YunxiNeural",
    },
    "en": {  # 英文語音選項
        "女生 1 (Ava - 美國)": "en-US-AvaNeural",
        "女生 2 (Emma - 美國)": "en-US-EmmaNeural",
        "男生 1 (Andrew - 美國)": "en-US-AndrewNeural",
        "男生 2 (Brian - 美國)": "en-US-BrianNeural",
    },
}

# -----------------------------------------------------------------------------
# 3. 核心輔助函數 (語言判定、文本切段與 TTS 生成)
# -----------------------------------------------------------------------------
def detect_language(text: str) -> str:
    """
    穩健的中英文語言偵測：
    1. 計算 CJK (中文字元) 比例，避免 PDF 雜訊干擾
    2. 使用 langid 進行語系分類
    """
    if not text.strip():
        return "zh"

    # 抽取前 2000 個字元作為採樣
    sample_text = text[:2000]

    # 正則分析：計算中文字符數 (包含常用中文與全形標點)
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', sample_text)
    
    # 若中文字數超過 10 個字，優先判定為中文
    if len(chinese_chars) > 10:
        return "zh"

    # 使用 langid 模型做最終分類判斷
    try:
        lang, confidence = langid.classify(sample_text)
        if lang.startswith("zh"):
            return "zh"
        elif lang == "en":
            return "en"
    except Exception:
        pass

    return "zh"  # 預設回到中文


def split_text(text: str, max_chars: int = 800) -> list[str]:
    """將長篇文本依標點符號進行切段，避免超過 Edge-TTS 長度限制"""
    sentences = re.split(r'([。！？\n;;\?!])', text)
    chunks = []
    current_chunk = ""

    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""
        full_sentence = sentence + punctuation

        if len(current_chunk) + len(full_sentence) <= max_chars:
            current_chunk += full_sentence
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = full_sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


async def generate_audio_chunk(text: str, voice: str, rate_str: str) -> bytes:
    """單段文字轉語音，回傳 MP3 位元組"""
    communicate = edge_tts.Communicate(text, voice, rate=rate_str)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data


async def convert_text_to_mp3(text_chunks: list[str], voice: str, rate: float, progress_bar):
    """處理多段文字合成，並串接為完整 MP3"""
    rate_str = f"{'+' if rate >= 0 else ''}{int(rate * 100)}%"
    combined_audio = b""
    total_chunks = len(text_chunks)

    for idx, chunk in enumerate(text_chunks):
        chunk_audio = await generate_audio_chunk(chunk, voice, rate_str)
        combined_audio += chunk_audio
        # 更新 Streamlit 進度條
        progress_bar.progress((idx + 1) / total_chunks)

    return combined_audio


# -----------------------------------------------------------------------------
# 4. Streamlit 主介面邏輯
# -----------------------------------------------------------------------------
uploaded_file = st.file_uploader("請上傳 PDF 檔案", type=["pdf"])

if uploaded_file is not None:
    # --- 功能 1: 擷取 PDF 文字 ---
    with st.spinner("正在讀取 PDF 內容..."):
        pdf_reader = PdfReader(uploaded_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    if not extracted_text.strip():
        st.error("無法從此 PDF 中提取任何文字，可能是掃描版圖片或已加密。")
        st.stop()

    # --- 功能 1 (續): 改進版的自動辨識語言 (中/英) ---
    lang_key = detect_language(extracted_text)
    lang_name = "中文 (Traditional/Simplified)" if lang_key == "zh" else "英文 (English)"

    st.success(f"已成功擷取文字！自動偵測語言為：**{lang_name}**")

    # --- Sidebar 語音控制設定區 ---
    st.sidebar.header("⚙️ 語音設定")

    # --- 功能 4: 選擇 4 種音調角色 ---
    available_voices = VOICES[lang_key]
    selected_voice_name = st.sidebar.selectbox(
        "選擇朗讀配音角色：",
        options=list(available_voices.keys())
    )
    selected_voice_code = available_voices[selected_voice_name]

    # --- 功能 5: 語速調整 ---
    speed_options = {
        "非常慢 (-50%)": -0.5,
        "慢 (-25%)": -0.25,
        "正常 (0%)": 0.0,
        "快 (+25%)": 0.25,
        "非常快 (+50%)": 0.5
    }
    
    selected_speed_label = st.sidebar.radio(
        "選擇語速：",
        options=list(speed_options.keys()),
        index=2  # 預設選擇「正常 (0%)」
    )
    speed_offset = speed_options[selected_speed_label]

    # 主畫面兩欄佈局 (預覽與匯出 TXT)
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("📝 文字內容預覽")
        edited_text = st.text_area(
            "您可以直接在下方編輯或修正文字後再進行轉音檔：",
            value=extracted_text,
            height=250
        )

    with col2:
        st.subheader("📥 匯出文字")
        # --- 功能 2: 提供匯出 txt 檔案 ---
        st.download_button(
            label="下載為 TXT 檔案",
            data=edited_text,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}.txt",
            mime="text/plain"
        )

    # --- 功能 3 & 6: 分段轉換並匯出 MP3 ---
    st.markdown("---")
    st.subheader("🔊 生成與下載語音mp3檔案")

    if st.button("🚀 開始轉換為 MP3 語音"):
        # --- 功能 6: 長篇 PDF 自動切段 ---
        chunks = split_text(edited_text, max_chars=800)
        st.info(f"系統已自動將文字分割為 **{len(chunks)}** 個區段進行處理...")

        progress_bar = st.progress(0.0)

        try:
            # 執行異步 Edge-TTS 合成
            audio_bytes = asyncio.run(
                convert_text_to_mp3(chunks, selected_voice_code, speed_offset, progress_bar)
            )

            st.success("🎉 MP3 語音合成完成！")

            # 播放器與下載按鈕
            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                label="⬇️ 下載 MP3 檔案",
                data=audio_bytes,
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}.mp3",
                mime="audio/mp3"
            )

        except Exception as e:
            st.error(f"轉換過程發生錯誤: {str(e)}")
