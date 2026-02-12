import { authFetch } from "../api/authFetch";
import { useAuth } from "../AuthContext";


export function MyPage(){

	const {logout} = useAuth();

	return (
		<div>
			<h1>마이페이지</h1>
			<button onClick={logout}>로그아웃</button>
		</div>
	)
}