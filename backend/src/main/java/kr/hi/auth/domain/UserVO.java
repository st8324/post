package kr.hi.auth.domain;

import lombok.Data;

@Data
public class UserVO {
	
	String me_id;
	String me_pw;
	String me_email;
	String me_role;
	
}
