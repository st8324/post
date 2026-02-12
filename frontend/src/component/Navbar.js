import {Link} from "react-router-dom";
import { useAuth } from "../AuthContext";

export function Navbar(){

	const NAV_ITEMS = [
		{label : "메인", path : "/", auth : "any"},
		{label : "로그인", path : "/login", auth : "guest"},
		{label : "회원가입", path : "/signup", auth : "guest"},
		{label : "마이 페이지", path : "/mypage", auth : "user"},
	];

	const {user} = useAuth();
	return (
		<nav>
			<ul>
				{
					NAV_ITEMS
					.filter(item =>{
						if(item.auth === "any") return true;
						if(item.auth === "guest") return !user;
						if(item.auth === "user") return user;
					})
					.map(item => <li key={item.label}><Link to={item.path}>{item.label}</Link></li>)
				}
			</ul>
		</nav>
	)
}