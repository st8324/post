package kr.hi.auth.controller;

import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.jsonwebtoken.Claims;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import kr.hi.auth.domain.UserDTO;
import kr.hi.auth.domain.UserVO;
import kr.hi.auth.security.jwt.JwtTokenProvider;
import kr.hi.auth.service.MemberDetailService;
import kr.hi.auth.service.UserService;
import kr.hi.auth.util.CustomUser;
import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/api/v1/auth")
@AllArgsConstructor
public class AuthController {
	
	private final UserService userService;
	private final AuthenticationManager authenticationManager;
    private final JwtTokenProvider jwtTokenProvider;
    private final MemberDetailService userDetailsService;
	
	@PostMapping("/signup")
	public ResponseEntity<Boolean> signup(
			@RequestBody UserDTO user){
		
		boolean res = userService.signup(user);
		
		return ResponseEntity.ok(res);
	}
	@PostMapping("/login")
	public ResponseEntity<Map<String, Object>> login(
			@RequestBody UserDTO user,
			HttpServletResponse response){
		Authentication authentication = authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(
                user.id(), user.pw()
            )
        );
        CustomUser customUser = (CustomUser) authentication.getPrincipal();
        String accessToken = jwtTokenProvider.createAccessToken(customUser);
        String refreshToken = jwtTokenProvider.createRefreshToken(customUser);
		
	    // RefreshToken → HttpOnly Cookie
	    Cookie cookie = new Cookie("refreshToken", refreshToken);
	    cookie.setHttpOnly(true);
	    cookie.setSecure(false); // https면 true
	    cookie.setPath("/");
	    cookie.setMaxAge(7 * 24 * 60 * 60);
	    response.addCookie(cookie);
	    
		return ResponseEntity.ok(Map.of(
				"accessToken", accessToken
		));
	}
	
	@GetMapping("/me")
	public ResponseEntity<Map<String, Object>> me(
			@AuthenticationPrincipal CustomUser customUser){
		UserVO user = customUser.getUser();
		
		return ResponseEntity.ok(Map.of(
			"id" , user.getMe_id(),
			"email", user.getMe_email(),
			"role", user.getMe_role()
			));
	}
	
	@PostMapping("/refresh")
	public ResponseEntity<?> refresh(
	    @CookieValue(name = "refreshToken", required = false) String refreshToken
	) {
	    if (refreshToken == null) {
	        return ResponseEntity.status(401).build();
	    }
	
	
	    if (!jwtTokenProvider.isRefreshToken(refreshToken)) {
	        return ResponseEntity.status(401).build();
	    }
	    
	    Claims claims = jwtTokenProvider.parseClaims(refreshToken);
	
	    String username = claims.getSubject();
	    CustomUser user =
	        (CustomUser) userDetailsService.loadUserByUsername(username);
	
	    String newAccessToken =
	        jwtTokenProvider.createAccessToken(user);
	
	    return ResponseEntity.ok(
	        Map.of("accessToken", newAccessToken)
	    );
	}
	
	@PostMapping("/logout")
	public ResponseEntity<?> logout(HttpServletResponse response) {
	
	    Cookie cookie = new Cookie("refreshToken", null);
	    cookie.setHttpOnly(true);
	    cookie.setSecure(false); // https면 true
	    cookie.setPath("/");
	    cookie.setMaxAge(0); // 즉시 삭제
	
	    response.addCookie(cookie);
	
	    return ResponseEntity.ok().build();
	}
}
