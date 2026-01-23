package kr.hi.post.controller;

import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

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
	@GetMapping("/post/detail/{num}")
	public String postDetail(
			//화면에서 보낸 게시글번호 가져옴 
			@PathVariable("num") int num,
			Model model) {
		//서비스에게 게시글번호 주면서 게시글 정보 가져오라고 요청
		//게시글 = 서비스야.게시글가져와(번호);
		PostVO 게시글 = postService.getPost(num);
		//- 가져온 게시글 화면에 전달
		model.addAttribute("post", 게시글);
		return "post/detail";
	}
	
	@GetMapping("/post/insert")
	public String postInsert() {
		
		return "post/insert";
	}
	
	@PostMapping("/post/insert")
	public String postInsertPost(
			//화면에서 보낸 게시글 정보를 가져옴
			PostVO post
			) {
		//확인용 : 게시글 정보 출력
		//System.out.println(post);
		//서비스에게 게시글 정보를 주면서 등록하고 결과를 알려달라고 요청
		//결과 = 서비스야.게시글등록해(게시글정보);
		boolean 결과 = postService.insertPost(post);
		//성공하면 /post/list로 이동
		if(결과) {
			return "redirect:/post/list";
		}
		//실패하면 /post/insert로 이동
		return "redirect:/post/insert";
	}
}
