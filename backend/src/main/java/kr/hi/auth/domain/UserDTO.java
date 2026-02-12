package kr.hi.auth.domain;

public record UserDTO(
	String id, 
	String pw, 
	String email) {}
