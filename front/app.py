import streamlit as str
import requests

str.set_page_config(page_title="슬램덩크 캐릭터 찾기", page_icon="🏀", layout="centered")

if "logged_in" not in str.session_state:
    str.session_state.logged_in = False
if "step" not in str.session_state:
    str.session_state.step = 1
if "answers" not in str.session_state:
    str.session_state.answers = {}

VALID_ID = "ilovekwu"
VALID_PW = "1234"

if not str.session_state.logged_in:
    str.title("🏀 슬램덩크 캐릭터 추천 시스템")
    str.subheader("로그인 후 서비스를 이용해 주세요.")
    
    login_id = str.text_input("아이디", key="login_id")
    login_pw = str.text_input("비밀번호", type="password", key="login_pw")
    
    if str.button("로그인"):
        if login_id == VALID_ID and login_pw == VALID_PW:
            str.session_state.logged_in = True
            str.success("로그인 성공! 질문을 시작합니다.")
            str.rerun()
        else:
            str.error("아이디 또는 비밀번호가 올바르지 않습니다.")

else:
    str.title("🔥 나에게 맞는 슬램덩크 캐릭터 찾기")
    
    if str.session_state.step == 1:
        str.subheader("Q1. 당신의 평소 성격은 어떤가요?")
        personality = str.radio(
            "선택해 주세요:",
            ["활발한 성격이다", "조용한/진지한 성격이다"],
            key="q1_radio"
        )
        if str.button("다음 질문으로"):
            str.session_state.answers["personality"] = personality
            str.session_state.step = 2
            str.rerun()
            
    elif str.session_state.step == 2:
        str.subheader("Q2. 농구를 할 때 선호하는 플레이 스타일은?")
        play_style = str.radio(
            "선택해 주세요:",
            ["공격 중심 (득점기계)", "수비 및 리바운드 중심"],
            key="q2_radio"
        )
        if str.button("다음 질문으로"):
            str.session_state.answers["play_style"] = play_style
            str.session_state.step = 3
            str.rerun()
            
    elif str.session_state.step == 3:
        str.subheader("Q3. 당신을 움직이는 가장 큰 원동력은?")
        motive = str.radio(
            "선택해 주세요:",
            ["끝없는 열정과 승부욕", "팀의 승리와 책임감"],
            key="q3_radio"
        )
        
        if str.button("🏁 결과 확인하기"):
            str.session_state.answers["motive"] = motive
            str.write("🔍 결과를 분석하고 있습니다...")
            
            
            backend_url = "http://backend:8000/recommend"
            
            payload = {
                "personality": str.session_state.answers["personality"],
                "play_style": str.session_state.answers["play_style"],
                "motive": str.session_state.answers["motive"]
            }
            
            try:
                response = requests.post(backend_url, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    str.success(f"분석 완료! 당신은 **{result['character']}** 타입입니다!")
                    str.metric(label="포지션", value=result["position"])
                    str.info(result["description"])
                    
                   
                    image_path = f"images/{result['character']}.png"
                    
                    try:
                        str.image(image_path, caption=f"슬램덩크 - {result['character']}", use_container_width=True)
                    except Exception as img_err:
                        str.warning(f"선수 이미지를 불러오지 못했습니다. 경로를 확인하세요: {image_path}")
                    # ==========================================================
                    
                    str.balloons()  
                else:
                    str.error(f"서버 오류 발생 (코드: {response.status_code})")
            except Exception as e:
                str.error(f"서버 연결 오류: {e}")
                
        if str.button("처음부터 다시하기"):
            str.session_state.step = 1
            str.session_state.answers = {}
            str.rerun()