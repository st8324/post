import { createContext, useContext, useEffect, useState } from "react";
import { authFetch } from "./api/authFetch";

const AuthContext = createContext(null);

function AuthProvider({children}){
	const [user, setUser] = useState(null);

	const getMe = async ()=>{
		try{
			const response = await authFetch("/api/v1/auth/me");
	
			if(response.ok){
				const res = await response.json();
				return res;
			}
		}catch(e){
			console.error(e);
		}
		return null;
	}

	//첫 렌더링할때만 실행하기 위해
	useEffect(()=>{
		getMeAndSetUser();
	},[]);

	const getMeAndSetUser = async ()=>{
		//회원 정보를 가져오고 : getMe
		const me = await getMe();
		//가져온 회원정보를 user에 업데이트 : setUser
		setUser(me);
	}

	const logout = async ()=>{
		//accessToken 삭제
		localStorage.removeItem("accessToken");

		try{
			//서버에 로그아웃 요청
			const response = await authFetch("/api/v1/auth/logout", {method : "POST"});
			
			if(!response.ok) return;

			alert("로그아웃했습니다.");
			//user를 null 변경
			setUser(null);

		}catch(e){
			console.error(e);
		}
	}
	return (
		<AuthContext.Provider value={{user, getMeAndSetUser, logout}} >
			{children}
		</AuthContext.Provider>
	)
}

const useAuth = ()=>useContext(AuthContext);

export {useAuth, AuthProvider};