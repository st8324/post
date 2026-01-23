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

	
}
