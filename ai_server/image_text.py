# 이미지 + 텍스트 
# 예 : 이미지에서 사과가 몇개 있어?
# 결과 : 사과 7개 있어요 => 사과가 어디에 있는지 네모칸치기
from google import genai
from google.genai import types
import os
import re
import json
import cv2

GOOGLE_API_KEY = 'AIzaSyC3_DMp9sOHrw2DHF_NqG91jV46yiRhNGc'
GOOGLE_MODEL_NAME = "gemini-2.5-flash-lite"

client = genai.Client(api_key=GOOGLE_API_KEY)
# 이미지에서 사용자 질문에 맞는 결과를 반환
# 사과가 어디에 있는지(위치) 
def get_ai_vision_result(image_path, user_prompt):

	with open(image_path, "rb") as f:
		image_bytes = f.read()
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
# 이미지 원본에 찾은 객체를 네모박스 쳐서 결과를 반환
def save_dection_result(image_path, ai_response, output_finlename=""):
	# 출력 파일명이 없으면
	if not output_finlename:
		# 경로 제외하고 파일명만 가져옴
		base_name = os.path.basename(image_path)
		file_name, ext = os.path.splitext(base_name)
		output_finlename = file_name + "_result" + ext
	
	# image_path에서 이미지 로드
	img = cv2.imread(image_path)

	height, width, _ = img.shape

	if img is None:
		raise Exception("원본 이미지 파일을 찾을 수 없습니다.")

	try:
		# ai_response에서 JSON 추출
		json_match = re.search(r'\[.*\]',ai_response,re.DOTALL)
		if not json_match :
			return 0, _
		json_str = json_match.group()
		detections = json.loads(json_str)
		res_count = {}
		# 찾은 객체들을 그림
		for item in detections:
			# 위에서 box_2d로 설정함. 
			ymin, xmin, ymax, xmax = item['box_2d']
			label = item['label']
			if res_count.get(label):
				res_count[label] += 1
			else:
				res_count[label] = 1

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
		
		success = cv2.imwrite(output_finlename, img)
		if success:
			print("성공!")
			return res_count, _
		else :
			print("실패")
			return res_count, _

	except Exception as e:
		print(f"예외 발생 : {e}")


input_image_path = 'fruit.jpg'
prompt = '바나나와 키위가 어디에 있어?'
result = get_ai_vision_result(input_image_path, prompt)
# result = """
# [
#   {"box_2d": [22, 402, 427, 638], "label": "apple"},
#   {"box_2d": [272, 236, 694, 475], "label": "apple"},
#   {"box_2d": [150, 621, 728, 804], "label": "grapes"},
#   {"box_2d": [163, 816, 519, 1000], "label": "grapes"}
# ]
# """


res_count, img_bytes = save_dection_result(input_image_path, result)

for label in res_count.keys():
	print(f"{label} : {res_count[label]}개")
