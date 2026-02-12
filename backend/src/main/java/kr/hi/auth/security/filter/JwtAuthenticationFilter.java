package kr.hi.auth.security.filter;

import java.io.IOException;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import io.jsonwebtoken.Claims;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import kr.hi.auth.security.jwt.JwtTokenProvider;
import kr.hi.auth.service.MemberDetailService;
import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtTokenProvider jwtTokenProvider;
    private final MemberDetailService userDetailsService;

    @Override
    protected void doFilterInternal(
        HttpServletRequest request,
        HttpServletResponse response,
        FilterChain filterChain
    ) throws ServletException, IOException {
				//요청 headers에 Authorization을 추출. 
				//로그인 후에 하는 요청에는 다 Authorization이 포함되도록 autFetch를 이용해서 작업
        String header = request.getHeader("Authorization");
        
				//Authorization가 없거나 유효한 토큰 정보가 아니면 인증확인을 안함
        if (header != null && header.startsWith("Bearer ")) {
		        //"Bearer " 뒷부분을 추출 => 토큰이기 때문에 
            String token = header.substring(7);
						//토큰에 있는 정보를 추출
            Claims claims = jwtTokenProvider.parseClaims(token);
            
            //토큰이 리프레쉬 토큰이면 인증 안함
            if ("refresh".equals(claims.get("type"))) {
				        filterChain.doFilter(request, response);
				        return;
				    }
						//토큰 소유주 정보 가져옴
            String username = claims.getSubject();

						//MemberDetailsService에서 구현한 기능을 이용해 [아이디]를 통해 회원 정보를
						//UserDetails로 가져옴(실제는 null이거나 CustomUser)
            UserDetails userDetails =
            		userDetailsService.loadUserByUsername(username);
						//사용자 인증
            Authentication auth = new UsernamePasswordAuthenticationToken(
                    userDetails, null, userDetails.getAuthorities()
            );
						//인증된 사용자 인증정보라고 저장 
						// => @AuthenticationPrincipal을 이용하여 로그인한 사용자 정보를 가져올 수 있음
            SecurityContextHolder.getContext().setAuthentication(auth);
        }

        filterChain.doFilter(request, response);
    }
}
