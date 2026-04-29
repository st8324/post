from google.genai import types
chat_history = []
chat_history.append(types.Content(
	role="user", 
	parts=[types.Part.from_text(text="오늘 날씨 어때?")]
	))
chat_history.append(types.Content(
	role="model", 
	parts=[types.Part.from_text(text="오늘은 맑고 화창하네요.")]
	))
chat_history.append(types.Content(
	role="user", 
	parts=[types.Part.from_text(text="그럼 오늘 뭐하는 게 좋을까?")]
	))
chat_history.append(types.Content(
	role="model", 
	parts=[types.Part.from_text(text="산책하는 건 어때요?")]
	))

db = {
	"history" : [
		types.Content(role="user", 	parts=[types.Part.from_text(text="오늘 날씨 어때?")]),
		types.Content(role="model", parts=[types.Part.from_text(text="오늘은 맑고 화창하네요.")]),
		types.Content(role="user", 	parts=[types.Part.from_text(text="그럼 오늘 뭐하는 게 좋을까?")]),
		types.Content(role="model", parts=[types.Part.from_text(text="산책하는 건 어때요?")]),
	],
	"summary" : ""
}