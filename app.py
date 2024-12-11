import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_law(law_code, article_number):
    base_url = f"https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode={law_code}"
    response = requests.get(base_url)
    
    if response.status_code != 200:
        return {"error": "無法連接法律資料庫"}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        article_content = soup.find('div', {'id': f'article_{article_number}'}).text.strip()
        last_updated = soup.find('div', {'class': 'date'}).text.strip()
        return {
            "article": article_content,
            "last_updated": last_updated
        }
    except AttributeError:
        return {"error": "找不到條文內容"}

st.title("法條查詢工具")
law_code = st.text_input("輸入法規代碼", "B0000001")
article_number = st.text_input("輸入條文編號", "184")

if st.button("查詢"):
    result = fetch_law(law_code, article_number)
    if "error" in result:
        st.error(result["error"])
    else:
        st.write(f"條文內容：{result['article']}")
        st.write(f"修訂日期：{result['last_updated']}")
