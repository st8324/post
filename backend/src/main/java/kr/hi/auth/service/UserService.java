package kr.hi.auth.service;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import kr.hi.auth.dao.UserDAO;
import kr.hi.auth.domain.UserDTO;
import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class UserService {
	
	private final UserDAO userDAO;
	
	private final BCryptPasswordEncoder encoder;

	public boolean signup(UserDTO user) {
		
		//기존 비밀번호를 가져와서 암호화
		//=> encode(비밀번호)를 이용해서
		String newPw = encoder.encode(user.pw());
		
		UserDTO newUser = new UserDTO(user.id(), newPw, user.email());
		try {
			return userDAO.insertUser(newUser);
		}catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}
}
