import streamlit as st
import requests


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "step" not in st.session_state:
    st.session_state["step"] = 1  


if not st.session_state["logged_in"]:
    st.title("🏀 슬램덩크 캐릭터 추천 시스템")
    st.subheader("로그인이 필요한 서비스입니다.")
    
    input_id = st.text_input("아이디 (ID)", placeholder="아이디를 입력하세요")
    input_pw = st.text_input("비밀번호 (PW)", type="password", placeholder="비밀번호를 입력하세요")
    
    if st.button("로그인"):
        if input_id == "ilovekwu" and input_pw == "1234":
            st.session_state["logged_in"] = True
            st.session_state["step"] = 1  
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 잘못되었습니다.")


else:
    st.title("🔥 나에게 맞는 슬램덩크 캐릭터 찾기")
    st.sidebar.write("👤 계정: ilovekwu")
    if st.sidebar.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.session_state["step"] = 1
        st.rerun()

    
    progress_percentage = (st.session_state["step"] - 1) / 3.0
    st.progress(min(progress_percentage, 1.0))

    
    if st.session_state["step"] == 1:
        st.subheader("Q1. 당신의 평소 성격은 어떤가요?")
        personality = st.radio(
            "선택해 주세요:",
            ["활발한 성격이다", "조용한/진지한 성격이다"],
            key="p_input"
        )
        
        if st.button("다음 질문으로 ➡️"):
            st.session_state["personality"] = personality 
            st.session_state["step"] = 2
            st.rerun()

    
    elif st.session_state["step"] == 2:
        st.subheader("Q2. 농구를 한다면 선호하는 플레이 스타일은?")
        play_style = st.selectbox(
            "선택해 주세요:",
            ["공격 중심 (득점기계)", "수비 및 리딩 중심 (팀 플레이어)"],
            key="s_input"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 이전으로"):
                st.session_state["step"] = 1
                st.rerun()
        with col2:
            if st.button("다음 질문으로 ➡️"):
                st.session_state["play_style"] = play_style 
                st.session_state["step"] = 3
                st.rerun()

    
    elif st.session_state["step"] == 3:
        st.subheader("Q3. 당신을 움직이는 가장 큰 원동력은 무엇인가요?")
        motive = st.radio(
            "선택해 주세요:",
            ["끝없는 열정과 승부욕", "위기를 극복하는 끈기 또는 즐기는 마음"],
            key="m_input"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ 이전으로"):
                st.session_state["step"] = 2
                st.rerun()
        with col2:
            if st.button("🏁 결과 확인하기"):
                st.session_state["motive"] = motive
                st.session_state["step"] = 4
                st.rerun()

    
    elif st.session_state["step"] == 4:
        st.markdown("### 🔍 결과를 분석하고 있습니다...")
        
        # 저장해뒀던 답변 데이터 꺼내기
        backend_url = "http://backend:8000/recommend"
        payload = {
            "personality": st.session_state["personality"],
            "play_style": st.session_state["play_style"],
            "motive": st.session_state["motive"]
        }
        
        try:
            # FastAPI 백엔드 호출
            response = requests.post(backend_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                st.markdown("---")
                st.balloons() # 축하 효과 애니메이션 (가산점 요소!)
                st.success(f"🎉 당신과 가장 닮은 캐릭터는 **[{result['character']}]** 입니다!")
                st.info(f"🏀 **포지션:** {result['position']}")
                st.write(f"📝 **특징:** {result['description']}")
            else:
                st.error("백엔드 서버 응답 실패")
        except Exception as e:
            st.error(f"서버 연결 오류: {e}")
            
        if st.button("🔄 다시 테스트하기"):
            st.session_state["step"] = 1
            st.rerun()