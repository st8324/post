package kr.hi.post.dao;

import java.util.List;

import kr.hi.post.model.vo.PostVO;

public interface PostDAO {

	List<PostVO> selectPosts();

	
}
