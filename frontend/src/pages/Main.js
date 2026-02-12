import { useAuth } from "../AuthContext"

export function Main(){
	const {user} = useAuth();
	return (
		<div>
			<h1>메인</h1>
			{
				user ? <h1>{user.id}</h1> : <h1>아이디 없음</h1>
			}
		</div>
	)
}