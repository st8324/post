from google import genai
from google.genai import types
from chromadb.config import Settings
import os
import chromadb
import pypdf
import time

# 전역 상수
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_MODEL_NAME = "gemini-2.5-flash-lite"
GOOGLE_EMBED_MODEL_NAME = "gemini-embedding-2-preview"
# 벡터 DB 설정(로컬)
CHROMA_PATH = './knowledge_base'

client = genai.Client(api_key=GOOGLE_API_KEY)

chroma_client = chromadb.PersistentClient(
	path=CHROMA_PATH,
	settings=Settings(
		# 우리가 사용한 데이터를 크로마db 본사 서버에 익명으로 보낼건지 말지
		anonymized_telemetry=False, 
		# 명령어로 db 내용을 초기화 권한을 부여할건지 말건지. 배포할 땐 False
		allow_reset=True)
)

collection = chroma_client.get_or_create_collection(name="class_knowledge")

def log(text:str):
	print("-"*50)
	print(text)
	print("-"*50)

# pdf를 임베딩하여 파일로 저장하는 함수
def ingest_pdf(file_path:str, size : int):
	log("지식 학습 시작")

	try:
		with open(file_path, "rb") as f:
			pdf_reader = pypdf.PdfReader(f)
			texts = [page.extract_text() or "" for page in pdf_reader.pages]
			full_text = "".join(texts)

			if not full_text.strip():
				log("PDF에서 읽어올 글자가 없습니다.")
			
			# 청킹(글자들를 분할)
			# size = 1000 # 한 분할에 포할될 문자 개수
			# range(strt, end, step) : start번지부터 end-1번지까지 step씩 증가
			# 리스트[start:end]/문자열[start:end] : start번지부터 end-1번지까지 추출
			# ["0번지부터999번지까지로된문자열", "1000~1999", "" ]
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
				ids=[f"{file_path}_{i}_{int(time.time())}" for i in range(len(chunks))],
				documents=chunks,
				embeddings=embeddings,
				metadatas=[{"source" : file_path} for _ in chunks]
			)
			log("저장 완료")
	except Exception as e:
		log(f"에러발생 : {e}")


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

# ingest_pdf('2026_미래소프트_복지규정.pdf', 100)
print(rag_ask("해피 프라이데이의 조건이 어떻게 되?"))