import { useState } from "react"
import { useNavigate } from "react-router-dom";


export function Signup(){

	const navigate = useNavigate();

	const [info, setInfo] = useState({ id : '', pw : '', pw2 : '', email : ''})
	const inputChange = (e) => {
		//e.target : 이벤트가 발생한 요소
		//name, value : e.target.name, e.target.value 
		// => 이벤트가 발생한 요소의 표준 속성 name과 value를 가져옴
		// => 모든 태그에서 name과 value는 표준 속성이다(X)
		const {name, value} = e.target;
		//{...info} : info 객체에 있는 속성과 값들을 복사해서 넣어줌
		//{...info, [name] : value} : info 객체에 있는 속성과 값들을 복사한 후 
		//   name변수에 있는 값을 속성명으로, value 변수에 있는 값을 값으로 덮어쓰기 
		setInfo({...info, [name] : value});
	}

	const singup = async ()=>{
		try{
			const response = await fetch("/api/v1/auth/signup", {
				method : "POST",
				headers : {
					"Content-Type" : "application/json"
				},
				body : JSON.stringify(info)
			});

			if(!response.ok){
				alert("회원 가입 실패!");
				return;
			}
			const res = await response.json();
			if(res){
				alert("회원 가입 성공!");
				navigate("/login");
			}else{
				alert("아이디 또는 이메일이 중복되었습니다.");
			}
		}catch(e){
			console.error(e);
		}
	}

	const sumbitHandler = (e) =>{
		e.preventDefault();
		singup();
	}
	return (
		<div>
			<h1>회원가입</h1>
			<form onSubmit={sumbitHandler}>
				<div>
					<div>
						<label htmlFor="id">아이디 : </label>
					</div>
					<div>
						<input type="text" name="id" id="id" onChange={inputChange} />	
					</div>
				</div>
				<div>
					<div>
						<label htmlFor="pw">비번 : </label>
					</div>
					<div>
						<input type="password" name="pw" id="pw" onChange={inputChange}/>	
					</div>
				</div>
				<div>
					<div>
						<label htmlFor="pw2">비번확인 : </label>
					</div>
					<div>
						<input type="password" name="pw2" id="pw2" onChange={inputChange}/>	
					</div>
				</div>
				<div>
					<div>
						<label htmlFor="email">이메일 : </label>
					</div>
					<div>
						<input type="text" name="email" id="email" onChange={inputChange}/>	
					</div>
				</div>
				<button>회원가입</button>
			</form>
		</div>
	)
}