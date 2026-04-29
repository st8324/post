package kr.hi.server.controller;

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

import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/api/v1/ai")
@AllArgsConstructor
public class AIController {
	
	private final WebClient webClient;
	
	@GetMapping("/ask")
	public String ask(
			@RequestParam("prompt")String prompt,
			@RequestParam("endpoint")String endpoint) {
		String result = webClient.get()
			.uri(uriBuilder-> uriBuilder
					.path(endpoint)
					.queryParam("prompt", prompt)
					.build())
			.retrieve()
			.bodyToMono(String.class)
			.block();
		return result;
	}
	
	@GetMapping("/translate")
	public String translate(
			@RequestParam("text")String text,
			@RequestParam("style")String style) {
		String result = webClient.get()
				.uri(uriBuilder-> uriBuilder
						.path("/translate")
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
						.path("/ad-copy")
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
					.uri("/summarize")
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
		
		return webClient.post().uri("/ingest-pdf")
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
						.path("/rag-chatbot")
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
		
		return webClient.post().uri("/image-text")
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
