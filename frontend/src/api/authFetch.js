
/**
 * 서버에 요청할 때 header에 토큰 정보를 자동으로 추가해주는 함수
 * @param {string} url 요청할 URL
 * @param {object} options 전송에 필요한 옵션들로, method, headers, body등이 옴
 */
async function authFetch(url, options = {} ){

	//토큰 정보를 가져옴
	const accessToken = localStorage.getItem("accessToken");

	//헤더를 설정
	const headers = {
		"credentials" : "include", 
		"Content-Type": "apllication/json",
		//"Authorization" : `Bearer 토큰값`,
		...(options.headers || {})
	}

	//토큰이 있으면 헤더에 토큰 정보를 추가
	if(accessToken){
		headers.Authorization = `Bearer ${accessToken}`;
	}
	//fetch를 이용해서 요청
	const response = await fetch(url, {
		...options,
		headers
	});
	
	//성공하면 요청 결과를 반환
	if(response.ok){
		return response;
	}
	//실패하면 리프레쉬 토큰을 이용해서 새 토큰을 발급받고, 받았으면 기존 하던작업 다시 진행
	const refresh = await fetch("/api/v1/auth/refresh", {
		method: "POST",
		credentials: "include",
	});

	if (!refresh.ok) throw new Error("로그인 만료");

	const data = await refresh.json();
	localStorage.setItem("accessToken", data.accessToken);

	return authFetch(url, options);
}

export {authFetch};