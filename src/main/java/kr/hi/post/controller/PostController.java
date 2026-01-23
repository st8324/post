package kr.hi.post.controller;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import kr.hi.post.model.vo.PostVO;
import kr.hi.post.service.PostService;

@Controller
public class PostController {

	private final PostService postService;
	
	public PostController(PostService postService) {
		this.postService = postService;
	}
	
	@GetMapping("/")
	public String main() {
		
		return "index";
	}
	
	@GetMapping("/post/list")
	public String postList(Model model) {
		//서비스에게 게시글 목록을 가져오라고 요청
		//게시글목록 = 서비스야.게시글목록가져와
		//게시글 목록 : List<게시글>
		List<PostVO> 게시글목록 = postService.getPosts();
		
		//화면에 게시글 목록을 전달
		//model.addAttribute("화면에서쓸이름", 게시글목록);
		model.addAttribute("posts", 게시글목록);
		return "post/list";
	}
}
