package kr.hi.auth.service;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import kr.hi.auth.dao.UserDAO;
import kr.hi.auth.domain.UserVO;
import kr.hi.auth.util.CustomUser;
import lombok.AllArgsConstructor;


@Service
@AllArgsConstructor
public class MemberDetailService implements UserDetailsService{

	
	private final UserDAO userDAO;
	
	@Override
	public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
		UserVO user = userDAO.selectUser(username);

		return user == null ? null : new CustomUser(user);
	}
}