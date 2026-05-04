package kr.hi.server.controller;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import lombok.extern.log4j.Log4j2;

@RestController
@RequestMapping("/api/v1/ai")
@Log4j2
public class AIController {
	
	private final WebClient webClient;
	
	// 핵심: @AllArgsConstructor를 빼고 명시적으로 aiWebClient 빈을 주입받습니다.
    public AIController(@Qualifier("webClient") WebClient webClient) {
        this.webClient = webClient;
        System.out.println("====== AI_SERVER_URL 주입 확인: " + webClient);
    }
    
	@GetMapping("/ask")
	public String ask(
			@RequestParam("prompt")String prompt,
			@RequestParam("endpoint")String endpoint) {
		log.info("일반 챗봇 테스트 작업중입니다....");
		String result;
		try {
			result = webClient.get()
					.uri(uriBuilder-> uriBuilder
							.path("/ai"+endpoint)
							.queryParam("prompt", prompt)
							.build())
					.retrieve()
					.bodyToMono(String.class)
					.block();			
		}catch (Exception e) {
			e.printStackTrace();
			log.info("ai 테스트 서버 연결 실패");
			result = "{\"message\" : \"연결실패\"}";
		}
		return result;
	}
	
	@GetMapping("/translate")
	public String translate(
			@RequestParam("text")String text,
			@RequestParam("style")String style) {
		String result = webClient.get()
				.uri(uriBuilder-> uriBuilder
						.path("/ai"+"/translate")
						.queryParam("text", text)
						.queryParam("style", style)
						.build())
				.retrieve()
				.bodyToMono(String.class)
				.block();
		return result;
	}
	@GetMapping("/ad-copy")
	public String adCopy(
			@RequestParam("product")String product,
			@RequestParam("feature")String feature,
			@RequestParam("target")String target,
			@RequestParam("temp")String temp,
			@RequestParam("count")String count
			) {
		
		String result = webClient.get()
				.uri(uriBuilder-> uriBuilder
						.path("/ai"+"/ad-copy")
						.queryParam("product", product)
						.queryParam("feature", feature)
						.queryParam("target", target)
						.queryParam("temp", temp)
						.queryParam("count", count)
						.build())
				.retrieve()
				.bodyToMono(String.class)
				.block();
		return result;
	}
	@PostMapping("/summarize")
	public String summarize(@RequestBody Summary dto){
		System.out.println(dto);
		String result = 
				webClient.post()
					.uri("/ai"+"/summarize")
					.bodyValue(dto)
					.retrieve()
					.bodyToMono(String.class)
					.block();

		return result;
	}
	
	@PostMapping("/ingest-pdf")
	public String image(@RequestParam("pdfFile")MultipartFile file) {
		MultipartBodyBuilder bodyBuilder = new MultipartBodyBuilder();
		bodyBuilder.part("file", file.getResource());
		
		return webClient.post().uri("/ai"+"/ingest-pdf")
				.contentType(MediaType.MULTIPART_FORM_DATA)
				.body(BodyInserters
						.fromMultipartData(bodyBuilder.build()))
				.retrieve()
				.bodyToMono(String.class)
				.block();
	}
	@GetMapping("/rag-ask")
	public String ragAsk(
			@RequestParam("prompt")String prompt
			) {
		
		String result = webClient.get()
				.uri(uriBuilder-> uriBuilder
						.path("/ai"+"/rag-chatbot")
						.queryParam("prompt", prompt)
						.build())
				.retrieve()
				.bodyToMono(String.class)
				.block();
		return result;
	}
	
	@PostMapping("/image-text")
	public String imageText(
		@RequestParam("query")String query,
		@RequestParam("img")MultipartFile file) {
		
		MultipartBodyBuilder bodyBuilder = new MultipartBodyBuilder();
		bodyBuilder.part("file", file.getResource());
		bodyBuilder.part("query", query);
		
		return webClient.post().uri("/ai"+"/image-text")
				.contentType(MediaType.MULTIPART_FORM_DATA)
				.body(BodyInserters
						.fromMultipartData(bodyBuilder.build()))
				.retrieve()
				.bodyToMono(String.class)
				.block();
	}
}
record Summary(
	String text,
	String target_lan,
	int max_sentence) {}
