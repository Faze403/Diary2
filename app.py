from flask import Flask, render_template, request, redirect, url_for
import random
import openai
import os

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = 'sk-proj-hzjl9hIZdIS1Zwjwop6FT3BlbkFJu2di6ybGcqFd2T9j5nTa'

# 일기 저장 폴더 설정
DIARY_FOLDER = 'diaries'
if not os.path.exists(DIARY_FOLDER):
    os.makedirs(DIARY_FOLDER)

fixed_questions = [
    "나이가 어떻게 되나요?",
    "성별이 어뗳게 되나요?",
    "오늘 몇 시에 일어났나요?",
    "아침, 점심, 저녁을 모두 챙겨 먹었나요?",
    "양치질을 몇 번 했나요?",
    "오늘 운동이나 신체 활동을 했나요? 어떤 활동이었나요?",
    "오늘 하루 동안 물을 얼마나 마셨나요?",
    "오늘 읽은 책이나 기사가 있나요?",
    "오늘 몇 시간을 일하거나 공부했나요?",
    "오늘 몇 번 웃었나요?",
    "오늘 잠깐이라도 휴식을 취했나요?",
    "오늘 하루 중 가장 오래 사용한 앱이나 웹사이트는 무엇인가요?"
]

random_questions = [
    "당신의 인생에서 가장 큰 어려움을 어떻게 극복하셨나요?",
    "후세대가 겪을 수 있는 가장 큰 도전은 무엇일까요?",
    "지금 후세대를 보면서 어떤 생각이 드시나요?",
    "당신이 젊었을 때 배운 가장 중요한 교훈은 무엇이었나요?",
    "후세대에게 꼭 해주고 싶은 말씀이 있으신가요?",
    "현재 세대가 잊지 말아야 할 가치는 무엇이라고 생각하시나요?",
    "당신이 자라면서 경험했던 사회적 변화는 무엇인가요?",
    "후세대가 더 나은 삶을 살기 위해 필요한 덕목은 무엇일까요?",
    "어려운 시기를 지나온 당신이 후세대에게 전하고 싶은 용기의 말은 무엇인가요?",
    "후세대가 배워야 할 가장 중요한 역사는 무엇이라고 생각하시나요?",
    "인생에서 후회했던 일이 있다면 그것은 무엇이고, 어떤 교훈을 얻으셨나요?",
    "후세대가 더 행복한 삶을 살기 위해 필요한 것은 무엇일까요?",
    "당신이 존경하는 인물은 누구이며, 그 이유는 무엇인가요?",
    "후세대에게 꼭 추천하고 싶은 책이나 영화가 있나요?",
    "지금 세상을 바라보는 당신의 시각은 어떠신가요?",
    "어려운 상황에서 마음을 다스리는 방법은 무엇인가요?",
    "후세대가 성공하기 위해 반드시 갖춰야 할 자질은 무엇일까요?",
    "인생에서 가장 감사했던 순간은 언제였나요?",
    "후세대가 직면할 수 있는 윤리적 도전은 무엇일까요?",
    "당신이 젊었을 때와 지금을 비교해볼 때 가장 크게 변화한 것은 무엇인가요?",
    "후세대가 꼭 알아야 할 인생의 진리는 무엇일까요?",
    "인생의 어려움을 극복하는 데 도움이 되었던 습관이나 행동이 있나요?",
    "후세대가 중요하게 생각해야 할 환경 문제는 무엇이라고 생각하시나요?",
    "당신이 후세대에게 전하고 싶은 가정의 중요성에 대한 이야기가 있나요?",
    "후세대가 잘못된 길로 빠지지 않기 위해 주의해야 할 점은 무엇일까요?",
    "당신의 인생에서 가장 소중했던 경험은 무엇이었나요?",
    "후세대가 더 나은 사회를 만들기 위해 필요한 것은 무엇이라고 생각하시나요?",
    "당신이 젊었을 때 꿈꾸던 미래는 어떤 모습이었나요?",
    "후세대가 자신을 잘 돌보는 방법에 대해 조언해주실 수 있나요?",
    "인생에서 가장 큰 성취감을 느꼈던 순간은 언제였나요?",
    "후세대가 현재의 문제를 해결하기 위해 배워야 할 지혜는 무엇일까요?",
    "당신이 인생에서 가장 감사하게 생각하는 사람은 누구인가요?",
    "후세대에게 전하고 싶은 가장 큰 희망이나 꿈은 무엇인가요?",
    "지금 세대를 보면서 느끼는 감정은 무엇인가요?",
    "후세대가 배우면 좋은 경제적 지혜는 무엇일까요?",
    "인생에서 가장 큰 사랑을 느꼈던 순간은 언제였나요?",
    "후세대가 더 나은 결정을 내리기 위해 필요한 조언이 있으신가요?",
    "당신이 젊었을 때 마주한 도전과 지금 세대가 마주한 도전은 어떻게 다른가요?",
    "후세대에게 전하고 싶은 가족의 소중함에 대한 이야기가 있나요?",
    "당신이 후세대에게 해주고 싶은 마지막 말은 무엇인가요?"
]

random_questions2 = [
    "무엇이 당신을 가장 행복하게 하나요?",
    "어린 시절의 가장 행복했던 기억은 무엇인가요?",
    "삶에서 가장 큰 성취는 무엇이라고 생각하시나요?",
    "지금까지 살아오면서 가장 중요한 교훈은 무엇인가요?",
    "어려운 시기를 극복한 방법은 무엇인가요?",
    "가장 감사하게 여기는 사람은 누구인가요?",
    "일상에서 가장 즐기는 활동은 무엇인가요?",
    "꿈꾸던 직업을 가질 수 있었나요? 그 직업은 무엇이었나요?",
    "가장 감동적인 순간은 언제였나요?",
    "당신이 가장 자랑스러워하는 순간은 무엇인가요?",
    "삶의 목적은 무엇이라고 생각하시나요?",
    "인생에서 가장 후회되는 일은 무엇인가요?",
    "지금까지 가장 행복했던 여행지는 어디인가요?",
    "당신에게 가장 소중한 물건은 무엇인가요?",
    "가장 좋아하는 음악이나 노래는 무엇인가요?",
    "마음의 평화를 찾기 위해 무엇을 하나요?",
    "지금까지 가장 많은 영향을 준 책이나 영화는 무엇인가요?",
    "가족과 함께 보낸 가장 행복한 시간은 언제였나요?",
    "당신의 삶에서 중요한 가치나 원칙은 무엇인가요?",
    "가장 즐겨먹는 음식은 무엇인가요?",
    "친구들과의 소중한 추억은 무엇인가요?",
    "가장 기억에 남는 생일 선물은 무엇인가요?",
    "마음속에 담아두고 싶은 풍경은 어떤 것인가요?",
    "가장 힘들었던 시기에 의지했던 것은 무엇인가요?",
    "당신의 삶을 한 마디로 표현한다면 무엇인가요?",
    "당신이 가장 존경하는 인물은 누구인가요?",
    "일상 속 작은 행복을 어떻게 찾으시나요?",
    "살아오면서 배운 중요한 지혜는 무엇인가요?",
    "가장 사랑했던 사람은 누구인가요?",
    "삶의 의미를 찾기 위해 무엇을 하나요?",
    "당신에게 있어 진정한 행복은 무엇인가요?",
    "가장 큰 도전은 무엇이었나요?",
    "지금까지 당신을 웃게 만든 일은 무엇인가요?",
    "가장 좋아하는 꽃이나 식물은 무엇인가요?",
    "당신의 인생 철학은 무엇인가요?",
    "어떤 일을 할 때 가장 열정을 느끼시나요?",
    "당신이 원하는 이상적인 하루는 어떤 모습인가요?",
    "가장 기억에 남는 순간은 언제였나요?",
    "당신의 삶에서 가장 소중한 교훈은 무엇인가요?",
    "지금까지 만난 사람 중에서 가장 영향력 있는 사람은 누구인가요?"
]

random_questions3 = [
    "친구 관계에서 가장 싫어하는 행동은 무엇인가요?",
    "가족 간의 관계에서 불편하거나 싫어하는 점은 무엇인가요?",
    "연인 관계에서 가장 싫어하는 부분은 무엇인가요?",
    "친구가 배신했을 때 어떤 기분이 드셨나요?",
    "지인 중에서 믿을 수 없는 사람을 만났을 때 어떤 기분이었나요?",
    "친구나 가족과의 약속을 어길 때 어떤 생각이 드나요?",
    "대화 중에서 어떤 유형의 말투나 태도가 싫은가요?",
    "사람들과의 상호작용에서 가장 불편한 점은 무엇인가요?",
    "다른 사람이 자신을 오해할 때 어떤 기분이 드나요?",
    "갈등이 생길 때 가장 싫어하는 해결 방식은 무엇인가요?",
    "사람들 사이에서 경쟁이 심할 때 어떤 기분이 드나요?",
    "친한 사람과 멀어졌을 때 어떤 생각이 드나요?",
    "관계에서 의존적이거나 집착하는 사람을 만났을 때 어떤 기분이 드나요?",
    "타인이 자신의 의견을 무시할 때 어떤 기분이 드나요?",
    "가족이 개인의 선택을 존중하지 않을 때 어떤 기분이 드나요?",
    "친한 사람의 비밀을 알게 되었을 때 어떤 생각이 드나요?",
    "인간관계에서 가장 싫어하는 위선적인 행동은 무엇인가요?",
    "동료나 상사가 불공정하게 대할 때 어떤 기분이 드나요?",
    "타인이 자신의 감정을 이해하지 못할 때 어떤 기분이 드나요?",
    "관계에서 불신이 생길 때 어떤 생각이 드나요?",
    "오늘 하루 중 가장 기뻤던 순간은 언제였나요?",
    "오늘 슬펐던 이유가 무엇인가요?",
    "오늘 하루 중 가장 화가 났던 일은 무엇인가요?",
    "오늘의 감정 상태를 색으로 표현한다면 어떤 색일까요?",
    "오늘 특별히 감사한 일이 있었나요?",
    "오늘 누구에게 가장 큰 감동을 받았나요?",
    "오늘 느낀 외로움의 정도는 어떠했나요?",
    "오늘 웃게 만든 일이나 사람은 누구였나요?",
    "오늘 하루 중 가장 스트레스 받았던 순간은 언제였나요?",
    "오늘의 기분을 한 단어로 표현한다면 무엇인가요?",
    "오늘 하루 동안 어떤 점에서 자랑스러웠나요?",
    "오늘의 기분을 좋아지게 만든 것은 무엇인가요?",
    "오늘 가장 두려웠던 일은 무엇이었나요?",
    "오늘 자신이 느꼈던 감정 중 가장 강렬한 것은 무엇인가요?",
    "오늘 하루 중 가장 평화로웠던 순간은 언제였나요?",
    "오늘 가장 큰 실망을 준 일은 무엇이었나요?",
    "오늘 행복감을 느낀 이유는 무엇인가요?",
    "오늘 가장 부끄러웠던 순간은 언제였나요?",
    "오늘 자신에게 칭찬해주고 싶은 이유는 무엇인가요?",
    "오늘 하루 중 가장 감사했던 순간은 언제였나요?"
]

random_questions4 = [
    "오늘 하루 중 가장 기뻤던 순간은 언제였나요?",
    "오늘 슬펐던 이유가 무엇인가요?",
    "오늘 하루 중 가장 화가 났던 일은 무엇인가요?",
    "오늘의 감정 상태를 색으로 표현한다면 어떤 색일까요?",
    "오늘 특별히 감사한 일이 있었나요?",
    "오늘 누구에게 가장 큰 감동을 받았나요?",
    "오늘 느낀 외로움의 정도는 어떠했나요?",
    "오늘 웃게 만든 일이나 사람은 누구였나요?",
    "오늘 하루 중 가장 스트레스 받았던 순간은 언제였나요?",
    "오늘의 기분을 한 단어로 표현한다면 무엇인가요?",
    "오늘 하루 동안 어떤 점에서 자랑스러웠나요?",
    "오늘의 기분을 좋아지게 만든 것은 무엇인가요?",
    "오늘 가장 두려웠던 일은 무엇이었나요?",
    "오늘 자신이 느꼈던 감정 중 가장 강렬한 것은 무엇인가요?",
    "오늘 하루 중 가장 평화로웠던 순간은 언제였나요?",
    "오늘 가장 큰 실망을 준 일은 무엇이었나요?",
    "오늘 행복감을 느낀 이유는 무엇인가요?",
    "오늘 가장 부끄러웠던 순간은 언제였나요?",
    "오늘 자신에게 칭찬해주고 싶은 이유는 무엇인가요?",
    "오늘 하루 중 가장 감사했던 순간은 언제였나요?",
    "만약 내가 하루 동안 투명인간이 될 수 있다면 무엇을 하고 싶나요?",
    "만약 시간여행을 할 수 있다면 어느 시대로 가고 싶나요? 왜요?",
    "만약 내가 원하는 모든 언어를 말할 수 있다면 가장 먼저 배우고 싶은 언어는 무엇인가요?",
    "만약 로또에 당첨된다면 가장 먼저 하고 싶은 일은 무엇인가요?",
    "만약 내가 어떤 동물로 변신할 수 있다면 어떤 동물이 되고 싶나요? 이유는 무엇인가요?",
    "만약 내가 유명한 연예인이라면 가장 하고 싶은 일은 무엇인가요?",
    "만약 하루 동안 아무 일도 하지 않아도 된다면 무엇을 하고 싶나요?",
    "만약 나에게 마법의 지팡이가 있다면 어떤 소원을 빌고 싶나요?",
    "만약 평생 한 가지 음식만 먹어야 한다면 어떤 음식을 선택할 건가요?",
    "만약 내가 세계 여행을 떠날 수 있다면 첫 번째로 방문하고 싶은 나라는 어디인가요?",
    "만약 내가 초능력을 가질 수 있다면 어떤 능력을 갖고 싶나요?",
    "만약 하루 동안 누구와든 역할을 바꿀 수 있다면 누구와 바꾸고 싶나요? 왜요?",
    "만약 내가 무한한 돈을 가지고 있다면 가장 하고 싶은 프로젝트는 무엇인가요?",
    "만약 내가 만화 속 캐릭터가 될 수 있다면 어떤 캐릭터가 되고 싶나요?",
    "만약 지금 당장 이사를 가야 한다면 어디로 가고 싶나요?",
    "만약 내가 미래를 예측할 수 있다면 가장 먼저 알고 싶은 것은 무엇인가요?",
    "만약 내가 원하는 직업을 가질 수 있다면 어떤 직업을 선택할 건가요?",
    "만약 내가 하루 동안 왕이나 여왕이 된다면 어떤 법을 만들고 싶나요?",
    "만약 내가 원하는 곳에서 살 수 있다면 어디에서 살고 싶나요?",
    "만약 내 생애 단 한 가지 꿈을 이룰 수 있다면 무엇을 이루고 싶나요?"
]
responses = []

@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

@app.route('/ddiary')
def index():
    random_questions_group = random.choice([random_questions, random_questions2, random_questions3, random_questions4])
    selected_random_questions = random.sample(random_questions_group, 2)  # 랜덤 질문 2개 선택
    return render_template('index.html', fixed_questions=fixed_questions, random_questions=selected_random_questions)


@app.route('/submit', methods=['POST'])
def submit():
    global responses
    answers = []
    for i, question in enumerate(fixed_questions):
        answer = request.form.get(f'answer{i}')
        answers.append((question, answer))
    
    # 랜덤 질문 처리
    for i in range(2):
        random_question = request.form.get(f'random_question{i}')
        random_answer = request.form.get(f'random_answer{i}')
        answers.append((random_question, random_answer))
    
    # GPT-3.5 Turbo API를 사용하여 일기 생성
    diary_content = generate_diary(answers)
    
    
    responses.append({
        'answers': answers,
        'diary': diary_content
    })
    return redirect(url_for('diary'))

@app.route('/diary')
def diary():
    return render_template('diary.html', responses=responses)

def generate_diary(answers):
    prompt = "사용자의 대답을 바탕으로 일기를 작성해 주세요:\n"
    for question, answer in answers:
        prompt += f"Q: {question}\nA: {answer}\n"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes diary entries based on user's answers."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )
    
    diary_content = response['choices'][0]['message']['content'].strip()
    return diary_content


if __name__ == '__main__':
    app.run(debug=True)