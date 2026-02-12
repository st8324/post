package kr.hi.auth.dao;

import org.apache.ibatis.annotations.Param;

import kr.hi.auth.domain.UserDTO;
import kr.hi.auth.domain.UserVO;

public interface UserDAO {

	boolean insertUser(@Param("user") UserDTO newUser);

	UserVO selectUser(@Param("id")String id);

}
