import { useState } from "react"
import { sendData } from "./Ai"
import { Link } from "react-router-dom"

function Translate(){

	const [form, setForm] = useState({style : 'formal', text : ''})
	const [result, setResult] = useState('')
	//작업중인지 아닌지 확인하기 위한 변수
	const [isLoading, setIsLoading] = useState(false)

	//이벤트들
	//태그들의 입력값들이 변하면 변한 값을 form(state 변수)에 넣어주는 함수
	const inputChange = (e)=>{
		const {name, value} = e.target
		setForm({...form, [name] : value})
	}

	const formSubmit = (e)=>{
		e.preventDefault()

		if(form.text.trim() === ''){
			alert("내용을 입력하세요.")
			return
		}
		setIsLoading(true)
		sendData('/api/v1/ai/translate', form, 'json', (res) =>{
			setResult(res.message)
			setIsLoading(false)
		})
	}
	return(
		<div>
			<Link to="/list">뒤로가기</Link>
			<h1>번역</h1>

			<form onSubmit={formSubmit}>
				<select name="style" onChange={inputChange}>
					<option value="formal">격식</option>
					<option value="casual">반말</option>
					<option value="business">비즈니스</option>
				</select>
				<div style={{display:'flex'}}>
					<textarea name="text" rows={5} cols={30} 
						style={{width:'100%'}}
						onChange={inputChange}
						readOnly={isLoading}
					></textarea>
					<div style={{width:'100%', border:'1px solid black'}}>
						{
							isLoading ? "[[번역중입니다. 잠시만 기다려주세요....]]" : result
						}
					</div>
				</div>
				<button disabled={isLoading}>번역</button>
			</form>
		</div>
	)
}

export default Translate