# Runway Video Generation Chatbot

Streamlit 기반의 Runway API를 활용한 비디오 생성 챗봇입니다. 이 애플리케이션은 두 가지 모드의 비디오 생성을 지원합니다:
1. Text-to-Video: 텍스트 설명으로부터 비디오 생성
2. Image-and-Text-to-Video: 이미지와 텍스트 조합으로 비디오 생성

## 기능
- 텍스트 기반 비디오 생성
- 이미지와 텍스트 기반 비디오 생성
- 생성된 비디오 즉시 미리보기
- 생성된 비디오 다운로드
- 사용자 친화적 인터페이스

## Streamlit Cloud 배포 방법

1. Streamlit Cloud (https://share.streamlit.io) 접속
2. "New app" 클릭 후 이 레포지토리 연결
3. 설정:
   - Main file path: app.py
   - Secrets에 RUNWAY_API_KEY 추가

## 사용 방법
1. 텍스트로 비디오 생성:
   - 텍스트 설명 입력
   - "영상 생성" 클릭
   - 생성된 비디오 다운로드

2. 이미지와 텍스트로 비디오 생성:
   - 이미지 업로드
   - 텍스트 설명 입력
   - "영상 생성" 클릭
   - 생성된 비디오 다운로드
