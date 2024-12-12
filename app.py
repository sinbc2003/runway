import streamlit as st
import requests
import json
from PIL import Image
import io
import base64
from datetime import datetime
from runwayml import RunwayML

# Streamlit 페이지 설정
st.set_page_config(page_title="Video Generation Chatbot", layout="wide")

def generate_video_from_text(prompt):
    """텍스트 프롬프트로부터 영상을 생성하는 함수"""
    try:
        # RunwayML 클라이언트 초기화
        client = RunwayML(api_key=st.secrets['RUNWAY_API_KEY'])
        
        # 텍스트 투 비디오 태스크 생성
        task = client.text_to_video.create(
            model='gen3a_turbo',
            prompt=prompt,
            num_frames=60,
            fps=30
        )
        
        # 태스크 완료 대기 및 결과 받기
        result = task.wait_for_completion()
        if result.status == 'completed':
            video_url = result.output['video']
            # 생성된 영상 다운로드
            video_response = requests.get(video_url)
            return video_response.content
        else:
            st.error(f"Error: {result.status} - {result.error}")
            return None
            
    except Exception as e:
        st.error(f"영상 생성 중 오류가 발생했습니다: {str(e)}")
        return None

def generate_video_from_image_and_text(image, prompt):
    """이미지와 텍스트로부터 영상을 생성하는 함수"""
    try:
        # 이미지를 임시로 저장
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # RunwayML 클라이언트 초기화
        client = RunwayML(api_key=st.secrets['RUNWAY_API_KEY'])
        
        # 이미지 투 비디오 태스크 생성
        task = client.image_to_video.create(
            model='gen3a_turbo',
            prompt_image=img_byte_arr,
            prompt_text=prompt,
            num_frames=60,
            fps=30
        )
        
        # 태스크 완료 대기 및 결과 받기
        result = task.wait_for_completion()
        if result.status == 'completed':
            video_url = result.output['video']
            # 생성된 영상 다운로드
            video_response = requests.get(video_url)
            return video_response.content
        else:
            st.error(f"Error: {result.status} - {result.error}")
            return None
            
    except Exception as e:
        st.error(f"영상 생성 중 오류가 발생했습니다: {str(e)}")
        return None

# Streamlit UI
st.title("Video Generation Chatbot")

# requirements.txt에 추가해야 할 내용을 알림
st.info("이 앱을 실행하기 위해서는 requirements.txt에 runwayml 패키지를 추가해야 합니다.")

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
