import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";


export function Login(){

	const navigate = useNavigate();

	const [info, setInfo] = useState({id : '', pw : ''});

	const {getMeAndSetUser} = useAuth();

	const inputChange = (e)=>{
		const {id, value} = e.target;
		setInfo({...info, [id] : value});
	}

	const login = async ()=>{
		try{
			const response = await fetch("/api/v1/auth/login", {
				method : "POST",
				headers : {
					"Content-Type" : "application/json"
				},
				body : JSON.stringify(info)
			});

			if(!response.ok){
				alert("로그인 실패!");
				return;
			}
			const res = await response.json();
			if(res.accessToken){
				alert("로그인 성공");
				localStorage.setItem("accessToken", res.accessToken);
				navigate("/");
				getMeAndSetUser();
			}
		}catch(e){
			console.error(e);
		}
	}
	const sumbitHandler = (e)=>{
		e.preventDefault();
		login();
	}

	return (
		<div>
			<h1>로그인</h1>
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
				<button>로그인</button>
			</form>
		</div>
	)
}