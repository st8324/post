const sendData = async (url, params, type, callbackFunc)=>{
	try{
		//URLSearchParams는 객체 안에 있는 변수들을 다음과 같이 만들어줌
		//변수=값&변수=값&변수=값 ...
		//객체 = {변수 : 값, 변수:값}
		const queryString = new URLSearchParams(params).toString()
		const response = await fetch(`${url}?${queryString}`)

		if(!response.ok){
			return
		}

		const result = type === 'json' ? await response.json() : await response.text()
		//콜백 함수가 있으면 마지막에 콜백 함수를 실행
		if(callbackFunc)
			callbackFunc(result)
	}catch(e){
		console.error(e)
	}
}

const sendDataPost = async (url, params, type, callbackFunc)=>{
	try{
		const response = await fetch(url,{
			method : 'post',
			headers :{
				'Content-type' : 'application/json'
			},
			body : JSON.stringify(params)
		})

		if(!response.ok){
			return
		}

		const result = type === 'json' ? await response.json() : await response.text()
		//콜백 함수가 있으면 마지막에 콜백 함수를 실행
		if(callbackFunc)
			callbackFunc(result)
	}catch(e){
		console.error(e)
	}
}
const fetchPost = async (url, init, type, callbackFunc)=>{
	try{
		const response = await fetch(url, init)

		if(!response.ok){
			return
		}

		const result = type === 'json' ? await response.json() : await response.text()
		//콜백 함수가 있으면 마지막에 콜백 함수를 실행
		if(callbackFunc)
			callbackFunc(result)
	}catch(e){
		console.error(e)
	}
}
export {sendData, sendDataPost, fetchPost}