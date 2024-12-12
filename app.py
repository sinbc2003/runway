import streamlit as st
import requests
import json
from PIL import Image
import io
import base64
from datetime import datetime
import time

# Streamlit 페이지 설정
st.set_page_config(page_title="Video Generation Chatbot", layout="wide")

def generate_video_from_text(prompt):
    """텍스트 프롬프트로부터 영상을 생성하는 함수"""
    try:
        headers = {
            "Authorization": f"Bearer {st.secrets['RUNWAY_API_KEY']}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "prompt": prompt,
            "num_frames": 300,  # 10초 영상을 위한 프레임 수 (30fps * 10초)
            "fps": 30,
            "model": "gen3a_turbo"
        }
        
        # 영상 생성 요청
        response = requests.post(
            "https://api.runway.ai/v2/text2video",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            video_url = result.get('uri')
            if video_url:
                # 생성된 영상 다운로드
                video_response = requests.get(video_url)
                return video_response.content
            else:
                st.error("비디오 URL을 찾을 수 없습니다.")
                return None
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"영상 생성 중 오류가 발생했습니다: {str(e)}")
        return None

def generate_video_from_image_and_text(image, prompt):
    """이미지와 텍스트로부터 영상을 생성하는 함수"""
    try:
        # 이미지를 base64로 인코딩
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
        
        headers = {
            "Authorization": f"Bearer {st.secrets['RUNWAY_API_KEY']}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "image": f"data:image/png;base64,{base64_image}",
            "prompt": prompt,
            "num_frames": 300,  # 10초 영상을 위한 프레임 수 (30fps * 10초)
            "fps": 30,
            "model": "gen3a_turbo"
        }
        
        # 영상 생성 요청
        response = requests.post(
            "https://api.runway.ai/v2/image2video",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            video_url = result.get('uri')
            if video_url:
                # 생성된 영상 다운로드
                video_response = requests.get(video_url)
                return video_response.content
            else:
                st.error("비디오 URL을 찾을 수 없습니다.")
                return None
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"영상 생성 중 오류가 발생했습니다: {str(e)}")
        return None

# Streamlit UI
st.title("Video Generation Chatbot")

# 탭 생성
tab1, tab2 = st.tabs(["텍스트로 영상 생성", "이미지와 텍스트로 영상 생성"])

# 텍스트로 영상 생성 탭
with tab1:
    st.header("텍스트로 영상 생성")
    text_prompt = st.text_area("영상을 생성할 텍스트를 입력하세요:", height=100)
    
    if st.button("영상 생성", key="text_gen"):
        if text_prompt:
            with st.spinner("영상을 생성하고 있습니다..."):
                video_data = generate_video_from_text(text_prompt)
                if video_data:
                    st.video(video_data)
                    st.download_button(
                        label="영상 다운로드",
                        data=video_data,
                        file_name=f"generated_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                        mime="video/mp4"
                    )
        else:
            st.warning("텍스트를 입력해주세요.")

# 이미지와 텍스트로 영상 생성 탭
with tab2:
    st.header("이미지와 텍스트로 영상 생성")
    uploaded_file = st.file_uploader("이미지를 업로드하세요:", type=['png', 'jpg', 'jpeg'])
    image_prompt = st.text_area("영상을 생성할 텍스트를 입력하세요:", key="image_prompt", height=100)
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)
        
        if st.button("영상 생성", key="image_gen"):
            if image_prompt:
                with st.spinner("영상을 생성하고 있습니다..."):
                    video_data = generate_video_from_image_and_text(image, image_prompt)
                    if video_data:
                        st.video(video_data)
                        st.download_button(
                            label="영상 다운로드",
                            data=video_data,
                            file_name=f"generated_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                            mime="video/mp4"
                        )
            else:
                st.warning("텍스트를 입력해주세요.")
