import { useState } from "react"
import { sendDataPost } from "./Ai"
import { Link } from "react-router-dom"

function Summarize(){

	const [isLoading, setIsLoading] = useState(false)
	const [result, setResult] = useState('')
	const [keywords, setKeywords] = useState([])
	const [form, setForm] = useState({
		text : '', 
		target_lan: 'Korean', 
		max_sentence : 3
	})
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
		sendDataPost('/api/v1/ai/summarize', form, 'json', (res) =>{
			let msg = res.message
			//요약과 키워드 분리 
			let arr = msg.split('======================')
			let summary = arr[0]
			let tmpKeywords = arr[1]
			
			setResult(parseSummary(summary))
			setKeywords(parseKeywords(tmpKeywords))

			//setResult()
			setIsLoading(false)
		})
	}
	function parseSummary(str){
		const separator = "- 요약 : "
		let summary = str ; 
		if(str.includes(separator)){
			summary = str.split(separator)[1].trim()	
		}
		let summaryArr = summary.split(".").map(item=>item.trim())
		return summaryArr.join(".\n")
	}
	function parseKeywords(kyes){
		let tmpKeywords = kyes.split("- 키워드 : ")[1].trim()
		return tmpKeywords.split(", ")
	}
	return (
		<div>
			<Link to="/list">뒤로가기</Link>
			<h1>요약</h1>
			{/* text, target_lan,	max_sentence */}
			<form onSubmit={formSubmit}>
				<div style={{display:'flex'}}>
					<label>요약문장수 : </label>
					<input type="number" name="max_sentence" 
						onChange={inputChange} 
						defaultValue={3} min={1} max={20}/>
					<label>요약언어 : </label>
					<select name="target_lan" onChange={inputChange}>
						<option value="Korean">한국어</option>
						<option value="English">영어</option>
					</select>
				</div>
				<div>
					<label>내용</label>
					<textarea name="text" onChange={inputChange}
						style={{width:'100%', height:'200px',boxSizing:'border-box'}}></textarea>
				</div>
				<button style={{width:'100%'}}>요약</button>
			</form>
			<div>
				<h2>요약 결과</h2>
				<pre style={{minHeight:'200px', border:'1px solid black', whiteSpace:'pre-wrap' }}>
					{isLoading ? "[요약 중입니다.....]" : result}
				</pre>
				<div>
					{keywords.map(item=>{
						return(
							<span key={item}>{item}</span>
						)
					})}
				</div>
			</div>
		</div>
	)
}

export default Summarize