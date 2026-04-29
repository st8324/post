import { useState } from "react"
import { Link } from "react-router-dom"
import { fetchPost } from "./Ai"

function ImageText(){

	const [form, setForm] = useState({query:''})
	const [file, setFile] = useState(null)
	const [result, setResult] = useState('')

	const inputChange = (e)=>{
		const {name, value} = e.target 
		setForm({...form, [name] : value})
	}
	const fileChange = (e)=>{
		setFile(e.target.files[0])
	}
	const sumbitHandler = async (e)=>{
		e.preventDefault()
		const formData = new FormData()
		formData.append("img", file)
		formData.append("query", form.query)
		await fetchPost('/api/v1/ai/image-text',{
			method : 'post',
			body : formData
		},'json', (res)=>{
			let detections = res.detections
			let str = '' 
			for (let label in detections){
				str += `${label}의 개수 : ${detections[label]}\n`
			}
			res.detections = str
			setResult(res)

		})
	}

	return (
		<div>
			<Link to={"/list"}>뒤로가기</Link>
			<h1>이미지 + 텍스트</h1>
			<form onSubmit={sumbitHandler}>
				<div>
					<input type="file" name="img" accept="image/*" onChange={fileChange} />
				</div>
				<div>
					<label>찾을 객체는? </label>
					<input type="text" name="query" onChange={inputChange} />
				</div>
				<button>전송</button>
			</form>
			<h2>결과</h2>
			<pre style={{
				whiteSpace:'pre-wrap', 
				minHeight:'200px', 
				border:'1px solid black'}}>{result.detections}</pre>
			<img src={result.image_data} alt="" />
		</div>
	)
}

export default ImageText