package kr.hi.post.service;

import java.util.List;

import org.springframework.stereotype.Service;

import kr.hi.post.dao.PostDAO;
import kr.hi.post.model.vo.PostVO;

@Service
public class PostService {

	private final PostDAO postDAO;
	
	public PostService(PostDAO postDAO) {
		this.postDAO = postDAO;
	}

	public List<PostVO> getPosts() {
		
		return postDAO.selectPosts();
	}

	public PostVO getPost(int num) {
		return postDAO.selectPost(num);
	}

	public boolean insertPost(PostVO post) {
		if(post == null || 
			post.getTitle().isBlank() || 
			post.getContent().isBlank() || 
			post.getWriter().isBlank()) {
			return false;
		}
		//다오에게 게시글 정보를 주면서 게시글을 등록하라고 요청
		//결과 = 다오야.게시글등록해(게시글정보);
		boolean 결과 = postDAO.insertPost(post);
		return 결과;
	}

	
}
