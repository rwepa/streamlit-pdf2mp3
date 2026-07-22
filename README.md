# streamlit-pdf2mp3

# 主題：

本專案採用 Python 搭配 Streamlit 框架開發，提供 PDF 轉換 MP3 語音檔，詳細規格如下：

1.採用 Python + Streamlit 開發 Web 應用程式。

2.支援 PDF 文件上傳。

3.自動辨識中文與英文文字內容（OCR）。

4.提供 TXT 文字檔下載。

5.提供 MP3 語音檔下載（Text-to-Speech）。

6.支援男聲／女聲切換。

7.支援語音播放速度調整。

8.適用於文件閱讀、語音學習及無障礙閱讀等應用場景。

# 程式碼：

+ GitHub: https://github.com/rwepa/streamlit-pdf2mp3/

+ requirements.txt: https://github.com/rwepa/streamlit-pdf2mp3/blob/main/requirements.txt

+ app.py: https://github.com/rwepa/streamlit-pdf2mp3/blob/main/app.py

# Streamlit佈署：

## 步驟1. 新增 ＧitHub 專案檔案

+ 選取 ＧitHub 首頁 \ 選取上方 [Repositories] \ 按 [New] 按鈕
+ Create a new repository 視窗 \ Repository name 方格輸入專案名稱: streamlit-pdf2mp3 \ Add README: 選取 ON \ 按最下方的 [Create repository] 按鈕
+ 最上方 [Add file] \ Upload files \ 上傳 requirements.txt 與 app.py 二個檔案

## 步驟2. 佈署至 Streamlit

+ 連結 https://share.streamlit.io \ 選取適當的登入選項, 本例選取 "Continue with GitHub"
+ 選取右側 Create app, 參考以下附圖.

![image](https://github.com/rwepa/streamlit-pdf2mp3/blob/main/images/streamlit_create_app.png)

+ 在 What would you like to do?視窗有3個選項 (1)Deploy a public app from GitHub (2)Deploy a public app from a template (3)Deploy a private app in Snowflake
+ 本例使用第1個 [Deploy a public app from GitHub] 
+ 在 Deploy an app 視窗依序輸入3個項目: Repository, Main file path, App URL, 最後按 Deploy 按鈕, 參考以下附圖.

![image](https://github.com/rwepa/streamlit-pdf2mp3/blob/main/images/streamlit_deploy_an_app.png)

## 步驟3. 測試 Streamlit

+ 連接 https://rwepa-pdf2mp3.streamlit.app/
+ 上傳 PDF: https://github.com/rwepa/streamlit-pdf2mp3/blob/main/biography-ming-chang-lee.pdf
+ 下載 TXT: https://github.com/rwepa/streamlit-pdf2mp3/blob/main/biography-ming-chang-lee.txt
+ 下載男生 MP3: https://github.com/rwepa/streamlit-pdf2mp3/blob/main/biography-ming-chang-lee-male.mp3
+ 下載女生 MP3: https://github.com/rwepa/streamlit-pdf2mp3/blob/main/biography-ming-chang-lee-female.mp3

