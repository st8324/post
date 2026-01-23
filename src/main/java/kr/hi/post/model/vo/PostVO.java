package kr.hi.post.model.vo;

import lombok.Data;

@Data
public class PostVO {
	int num;
	String title, content, writer;
	String date;
}
