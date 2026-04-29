from google import genai
from google.genai import types
from fastapi import FastAPI, Query, File, UploadFile
from pydantic import BaseModel
from chromadb.config import Settings
import uvicorn
import os
import sample as sp
import sys
import pypdf
import time
import chromadb
import io
import cv2
import numpy as np
import json 
import re
import base64

app = FastAPI()

# gemini-2.5-flash-lite
# "gemini-3.1-flash-lite-preview"
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_MODEL_NAME = "gemini-2.5-flash-lite"
GOOGLE_SUMMARY_MODEL_NAME = "gemini-3.1-flash-lite-preview"
GOOGLE_EMBED_MODEL_NAME = "gemini-embedding-2-preview"
# GOOGLE_MODEL_NAME = "gemini-3.1-flash-lite-preview"
SYSTEM_INSTRUCTION= "당신은 내 담당 영양사야. 내가 먹은 음식들을 토대로 식단을 관리해줘."
MAX_HISTORY_SIZE=4
CHROMA_PATH = './knowledge_base'

client = genai.Client(api_key=GOOGLE_API_KEY)

chat_history = sp.chat_history if sp.chat_history else []
db =  sp.db if sp.db else {	"history" : [], "summary" : ""}

chroma_client = chromadb.PersistentClient(
	path=CHROMA_PATH,
	settings=Settings(
		# 우리가 사용한 데이터를 크로마db 본사 서버에 익명으로 보낼건지 말지
		anonymized_telemetry=False, 
		# 명령어로 db 내용을 초기화 권한을 부여할건지 말건지. 배포할 땐 False
		allow_reset=True)
)
collection = chroma_client.get_or_create_collection(name="class_knowledge")


@app.get("/ask")
async def ask_gemini(prompt: str):
	response = client.models.generate_content(
    model= GOOGLE_MODEL_NAME,
    contents=types.Part.from_text(text=prompt),
	)
	
	return {
		"message": response.text
	}

@app.get("/translate")
async def translate(
	text:str = Query(..., description='번역할 문장'),
	style:str =  Query("formal", description='말투: formal(격식), casual(반말), business(비즈니스)')
):
	
	# 좋은 번역을 위하여 번역 문장을 좋은 프롬프트로 변환
	# I am a boy => 나는 소년이다
	# f : 문자열 안에 변수를 쉽게 넣을 때 사용
	# """ : 문자열이 여러줄이 가능하게 해줌
	prompt = f"""
	너는 세계 최고의 다국어 번역가야. 아래의 규칙을 지켜서 번역해줘.
	1. 대상 문장 : {text}
	2. 요청 말투 : {style} 말투로 번역해줘.
	3. 도착어 : 한국어면 영어로, 영어이면 한국어로 자동 감지해서 번역해줘.
	4. 결과물 : 번역된 문장 외에 다른 설명은 생략해
	"""
	# Have you heard of that? I was the only one who didn’t know.
	# => "그것에 대해 들어본 적 있어요? 나만 몰랐어요."
	# => casual : "너 그거 들어봤어? 나만 몰랐어."
	response = client.models.generate_content(
    model=GOOGLE_MODEL_NAME,
    contents=types.Part.from_text(text=prompt),
	)

	return {
		"message": response.text
	}

@app.get("/ad-copy")
def ad_copy(
	product:str = Query(..., description='상품명'),
	feature:str = Query(..., description='제품 특징'),
	target:str = Query('전연령', description='타겟'),
	# 1과 가까울수록 창의적
	temp:float = Query(0.8, ge=0.0, le=1.0, description='창의성 온도(0~1)'),
	count:int = Query(50, description='광고문구 글자제한'),
):

	prompt = f"""
	너는 창의적인 카피라이터야. 
	{product}의 광고 문구를 {target}을 타겟으로 맞춰 {count}자 내외로 작성해줘.
	특징 : {feature}
	"""

	response = client.models.generate_content(
    model=GOOGLE_MODEL_NAME,
    contents=types.Part.from_text(text=prompt),
    config=types.GenerateContentConfig(
			temperature=temp,
			top_p=0.95,
			top_k=20,
    ),
	)
	return { 'message' : response.text}

class Summary(BaseModel):
	text : str
	target_lan : str = "Korean"
	max_sentence: int = 3 # n문장 요약

@app.post("/summarize")
async def summarize(summary:Summary):
	
	prompt = f"""
	너는 복잡한 정보를 명료하게 정리하는 전문 편집자야.
	아래 텍스트를 분석해서 {summary.target_lan}로 요약해줘	

	[텍스트]
	{summary.text}

	[작성 가이드]
	1. 핵심 내용을 최대 {summary.max_sentence}개의 문장으로 요약할 것.
	2. 가장 중요한 키워드를 3개 추출할 것.
	3. 객관적이고 중립적인 어조를 유지할 것.

	[출력형식]
	- 요약 : (내용)
	======================
	- 키워드 : #키워드1, #키워드2, #키워드3
	"""
	"""
	- 요약 : 삼성SDS는 국회 빅데이터 플랫폼 구축 1단계 사업을 통해 AI 기반 국회 의정 지원 플랫폼을 공식 오픈했으며, 
	이는 국회의 방대한 데이터를 기반으로 검색, 분석, 작성까지 지원하는 생성형 AI 시스템이다. 
	이 플랫폼은 국회의원 및 보좌진 5000여 명이 활용하여 데이터 기반 의정활동을 본격화하고, 
	AI 어시스턴트, 지능형 검색, 법률안 서비스 등 3가지 핵심 의정지원 서비스를 제공한다. 
	삼성SDS는 이번 사업을 통해 AI 전환 자동화, 데이터 거버넌스 체계 수립, 국회 특화 언어모델 도입 등으로 안정적인 데이터 활용 기반을 마련하고 보안성을 강화했다.
	- 키워드 : #AI국회, #의정지원플랫폼, #생성형AI"
	"""

	response = client.models.generate_content(
    model=GOOGLE_MODEL_NAME,
    contents=types.Part.from_text(text=prompt),
    config=types.GenerateContentConfig(temperature=0.2),
	)
	return { 'message' : response.text}

# 최근 N개 대화를 이용한 챗봇 => N개 이전 대화는 날라감
@app.get("/chatbot")
async def chatbot_gemini(prompt: str):
	global chat_history
	chat_history.append(types.Content(
		role="user", 
		parts=[types.Part.from_text(text=prompt)]
		))

	response = client.models.generate_content(
		model= GOOGLE_MODEL_NAME,
		contents=chat_history, #types.Part.from_text(text=prompt),
		config=types.GenerateContentConfig(
			temperature=0.7,
			system_instruction=SYSTEM_INSTRUCTION
		),
	)
	model_text = response.text
	# 대화 기록을 저장(추가)
	# 사용자 질문을 저장
	chat_history.append(types.Content(
		role="user", 
		parts=[types.Part.from_text(text=prompt)]
		))
	chat_history.append(types.Content(
		role="model", 
		parts=[types.Part.from_text(text=model_text)]
		))

	# 대화 기록이 최대 저장수를 넘어가면 앞부분 제거
	if(len(chat_history) >= MAX_HISTORY_SIZE):

		chat_history = chat_history[-10:] # 뒤에서 10개 추출

	# 답변을 리턴
	return {
		"message": model_text
	}

async def update_summary():
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
	db["summary"] = response.text

@app.get("/summary-chatbot")
async def chatbot_gemini(prompt: str):
	
	db["history"].append(types.Content(	role="user", parts=[types.Part.from_text(text=prompt)]))

	response = client.models.generate_content(
		model= GOOGLE_MODEL_NAME,
		contents=db["history"], 
		config=types.GenerateContentConfig(
			temperature=0.7,
			system_instruction=SYSTEM_INSTRUCTION
		),
	)
	model_text = response.text
	db["history"].append(types.Content(	role="model", parts=[types.Part.from_text(text=model_text)]	))

	if(len(chat_history) >= MAX_HISTORY_SIZE):
		await update_summary()
	
	# 답변을 리턴
	return {
		"message": model_text,
		"summary": db["summary"]
	}


def log(text:str):
	print("-"*50)
	print(text)
	print("-"*50)
	sys.stdout.flush()

async def ingest_pdf(file:UploadFile, size : int):
	log("지식 학습 시작")

	try:
		content = await file.read()
		pdf_reader = pypdf.PdfReader(io.BytesIO(content))
		texts = [page.extract_text() or "" for page in pdf_reader.pages]
		full_text = "".join(texts)

		if not full_text.strip():
			log("PDF에서 읽어올 글자가 없습니다.")
		
		chunks = [full_text[i:i+size] for i in range(0, len(full_text), size)]

		log("[분할 완료]")
		embeddings = []
		for chunk in chunks:
			embed_res = client.models.embed_content(
				model=GOOGLE_EMBED_MODEL_NAME,
				contents=chunk
			)
			embeddings.append(embed_res.embeddings[0].values)
		log("[임베딩 완료]")
		
		
		collection.add(
			# id를 "파일명_숫자_시간정수"
			ids=[f"{file.filename}_{i}_{int(time.time())}" for i in range(len(chunks))],
			documents=chunks,
			embeddings=embeddings,
			metadatas=[{"source" : file.filename} for _ in chunks]
		)
		log("저장 완료")
	except Exception as e:
		# log(f"에러발생 : {e}")
		raise Exception(e)

# pdf를 주면 임베딩해서 저장
@app.post("/ingest-pdf")
async def ingest_pdf_get(file:UploadFile = File(...)):
	
	try:
		await ingest_pdf(file, 100)
		return { "message" : "규정집이 등록 됐습니다."}
	except Exception as e:
		log(f"에러발생 : {e}")
		return { "message" : "규정집 등록에 실패했습니다."}

def rag_ask(prompt : str):
	if collection.count() == 0:
		log("학습된 데이터가 없습니다. PDF를 등록해주세요.")
		return
	
	try:
		log(f"질문 : {prompt}")
		embed_res = client.models.embed_content(
			model=GOOGLE_EMBED_MODEL_NAME,
			contents=[prompt]
		)
		embedding = embed_res.embeddings[0].values

		results = collection.query(
			query_embeddings=[embedding],
			n_results=3 # 상위 몇개를 가져올지
		)
		# print(results)
		context = "\n".join(results['documents'][0])
		
		send_prompt = f"""
		[지식 데이터]를 참고하여 질문에 답해줘.
		정보가 부족하면 추측하지 말고 솔직히 답해줘.
		[지식 데이터] : {context}
		질문 : {prompt}
		답변 : 
		"""
		response = client.models.generate_content(
			model=GOOGLE_MODEL_NAME,
			contents=send_prompt,
			config=types.GenerateContentConfig(temperature=0.1)
		)
		return {
			"message" : response.text
		}
	except Exception as e:
		log(f"예외 발생 : {e}")

@app.get("/rag-chatbot")
async def rag_chatbot(prompt:str=Query(...,description='질문')):
	return rag_ask(prompt)

async def get_ai_vision_result(image_bytes, user_prompt):

	output_type = '[{"box_2d": [ ymin, xmin, ymax, xmax], "label" : "apple"}]'
	prompt = f"""
	질문 : {user_prompt}
	이미지에서 해당 객체를 모두 찾아주세요.
	출력 형식은 반드시 {output_type}처럼 json 리스트 형태로만 나열하세요.
	객체명은 영문으로 해주세요.
	예 : {output_type}
	"""

	response = client.models.generate_content(
    model= GOOGLE_MODEL_NAME,
    contents=[
			types.Part.from_text(text=prompt),
			types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')
		]
	)
	return response.text

async def save_detection_result(image_bytes, ai_response):
	detections = {}
	image_data = None

	
	try:
		nparr = np.frombuffer(image_bytes, np.uint8)
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

		height, width, _ = img.shape
		if img is None:
			raise Exception("원본 이미지 파일을 찾을 수 없습니다.")
		
		json_match = re.search(r'\[.*\]',ai_response,re.DOTALL)
		if not json_match :
			raise Exception("찾을 객체가 없습니다.")
		
		json_str = json_match.group()
		detections_json = json.loads(json_str)
		
		# 찾은 객체들을 그림
		
		for item in detections_json:
			# 위에서 box_2d로 설정함. 
			ymin, xmin, ymax, xmax = item['box_2d']
			label = item['label']
			if detections.get(label):
				detections[label] += 1
			else:
				detections[label] = 1
		
			
			# 좌표 변환. 
			# 제미나이 ai는 이미지 해상도와 관계없이 
			# 이미지 전체 크기를 1000x1000규격의 가상 좌표계로 변환하여 결과를 반환
			left = int(xmin * width / 1000)
			top = int(ymin * height / 1000)
			right = int(xmax * width / 1000)
			bottom = int(ymax * height / 1000)
			# cv2는 rgb가 아니라 bgr
			cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
			cv2.putText(img, label, (left, top-10), 
				cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
				(255, 0, 0), 2)
		
		success, encoded_img = cv2.imencode(".jpg", img)
		if success:
			log("성공!")
			image_data = encoded_img
		else :
			log("실패")
	except Exception as e:
		log(f"예외 발생 : {e}")
	finally:
		return detections, image_data

@app.post("/image-text")
async def image_text(
	file:UploadFile = File(...),
	query:str=File(...)):
	# log(query)
	# log(file.filename)
	image_bytes = await file.read()
	ai_response = await get_ai_vision_result(image_bytes, query)

	detections, encoded_img = await save_detection_result(image_bytes, ai_response)
	base64_image = base64.b64encode(encoded_img).decode('utf-8')

	return {
		"detections" : detections, 
		"image_data" : f"data:image/jpeg;base64,{base64_image}"
	}

if __name__ == '__main__':
	uvicorn.run('main:app',host='0.0.0.0', port=8000, reload=True)