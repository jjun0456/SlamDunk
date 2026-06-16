from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SurveyData(BaseModel):
    personality: str
    play_style: str
    motive: str

@app.post("/recommend")
def get_recommendation(data: SurveyData): 
    # 기본값 설정
    character = "안선생님"
    position = "감독"
    description = "포기하면 그 순간이 바로 시합 종료입니다."

    
    if data.personality == "활발한 성격이다":
        if data.play_style == "공격 중심 (득점기계)":
            if data.motive == "끝없는 열정과 승부욕":
                character = "강백호"
                position = "파워 포워드 (PF)"
                description = "무한한 체력과 열정, 폭발적인 활발함으로 코트를 지배하는 천재 강백호 타입입니다!"
            else:
                character = "정대만"
                position = "슈팅 가드 (SG)"
                description = "포기를 모르는 불꽃 남자! 과거의 공백을 이겨내고 결정적인 순간 3점슛을 꽂아넣는 정대만 타입입니다!"
        else:
            character = "송태섭"
            position = "포인트 가드 (PG)"
            description = "빠른 스피드와 활발한 리더십으로 팀을 지휘하는 코트 위의 사령관 송태섭 타입입니다."

    
    elif data.personality == "조용한/진지한 성격이다":
        if data.play_style == "공격 중심 (득점기계)":
            if data.motive == "끝없는 열정과 승부욕":
                character = "서태웅"
                position = "스몰 포워드 (SF)"
                description = "말수는 적지만 오직 승리와 실력으로 코트를 압도하는 최고의 에이스 서태웅 타입입니다."
            else:
                character = "윤대협"
                position = "스몰 포워드 / 포인트 가드 (스윙맨)"
                description = "승부의 압박감 속에서도 미소를 잃지 않고, 경기를 즐길 줄 아는 능구렁이 천재 윤대협 타입입니다!"
        else:
            character = "채치수"
            position = "센터 (C)"
            description = "묵묵하고 진지하게 골밑을 지키며 팀을 전국대회로 이끄는 든든한 기둥 주장 채치수 타입입니다."

    return {
        "character": character,
        "position": position,
        "description": description
    }