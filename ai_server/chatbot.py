# 누적 요약 챗봇 => 삭제할 때 요약을 해서 추가
# 12개 => 이전 10개를 요약 => 추가 => 3개
from google import genai
from google.genai import types
import os

db = {
	"history" : [
		types.Content(role="user", 	parts=[types.Part.from_text(text="오늘 날씨 어때?")]),
		types.Content(role="model", parts=[types.Part.from_text(text="오늘은 맑고 화창하네요.")]),
		types.Content(role="user", 	parts=[types.Part.from_text(text="그럼 오늘 뭐하는 게 좋을까?")]),
		types.Content(role="model", parts=[types.Part.from_text(text="산책하는 건 어때요?")]),
	],
	"summary" : ""
}
# "gemini-2.5-flash-lite"
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_MODEL_NAME = "gemini-3.1-flash-lite-preview"
GOOGLE_SUMMARY_MODEL_NAME = "gemini-3.1-flash-lite-preview"
SYSTEM_INSTRUCTION= "당신은 내 담당 영양사야. 내가 먹은 음식들을 토대로 식단을 관리해줘."
MAX_HISTORY_SIZE = 4

client = genai.Client(api_key=GOOGLE_API_KEY)

# 최근 2개를 제외한 나머지를 요약후 삭제
def update_summary():
	to_summarize = db["history"][:-2] #마지막 2개 제외 

	prompt = f"""
	기존 요약 : {db['summary']}
	추가된 대화 : {to_summarize}

	위 내용을 바탕으로 지금가지의 대화 맥락을 한 문장으로 업데이트해줘.
	사용자의 주요 관심사와 언급된 핵심 사실을 포함해줘.
	"""

	response = client.models.generate_content(
    model=GOOGLE_SUMMARY_MODEL_NAME,
    contents=types.Part.from_text(text=prompt),
		config=types.GenerateContentConfig(
			temperature=0.7,
			system_instruction=SYSTEM_INSTRUCTION
		),
	)
	print(response.text)
	db["summary"] = response.text

print(db)
prompt = '어디로 갈까?'
model_text = '가까운 공원이 좋을 것 같아요.'
db["history"].append(types.Content(role="user", 	
	parts=[types.Part.from_text(text=prompt)]))

db["history"].append(types.Content(role="model", 	
	parts=[types.Part.from_text(text=model_text)]))
update_summary()
print(db)