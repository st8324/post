package kr.hi.server.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import lombok.extern.log4j.Log4j2;

@Configuration
@Log4j2
public class WebConfig implements WebMvcConfigurer {

	@Value("${ai.server.url}")
    private String aiServerUrl;
	
	@Override
	public void addCorsMappings(CorsRegistry registry) {
		registry.addMapping("/**")
			.allowedOrigins("http://localhost:3000")
			.allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
			.allowedHeaders("*")
			.allowCredentials(true);
	}
	
	@Bean
    public WebClient webClient() {
		log.info("AI Server ULR : " + aiServerUrl);
        return WebClient.builder()
                .baseUrl(aiServerUrl)
                .build();
    }
}
