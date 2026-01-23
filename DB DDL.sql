drop database if exists post;
create database post;
use post;

create table post(
	num int primary key auto_increment,
    title varchar(50) not null,
    content longtext not null,
    writer varchar(20) not null,
    date datetime not null default current_timestamp
);