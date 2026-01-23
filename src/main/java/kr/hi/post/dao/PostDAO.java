package kr.hi.post.dao;

import java.util.List;

import org.apache.ibatis.annotations.Param;

import kr.hi.post.model.vo.PostVO;

public interface PostDAO {

	List<PostVO> selectPosts();

	PostVO selectPost(@Param("num")int num);

	boolean insertPost(PostVO post);

	
}
