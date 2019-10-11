create database if not exists ssafynews_ai character set = utf8mb4 collate = utf8mb4_unicode_ci;

use ssafynews_ai;

drop table if exists commentstag;
drop table if exists newstag;
drop table if exists comments;
drop table if exists news;

create table news(
    news_num int not null primary key,
    news_title varchar(100) not null,
    news_context text not null,
    news_date int default 0,
    news_time varchar(30) not null
    );
    
create table comments(
    comment_num int auto_increment primary key,
    comment_context varchar(500) not null,
    label_news tinyint not null,
    label_local tinyint not null,
    news_num int not null,
    comment_time varchar(20) not null,
    foreign key (news_num) references News(news_num) on delete cascade
    );

create table newstag (
	newstag_num int auto_increment primary key,
	newstag_name varchar(20) not null,
	newstag_count int not null,
	news_num int not null,
	foreign key (news_num) references news(news_num) on delete cascade
);

create table commentstag (
	commentstag_num int auto_increment primary key,
	commentstag_name varchar(20) not null,
	commentstag_count int not null,
	news_num int not null,
	foreign key (news_num) references news(news_num) on delete cascade
);

select * from news;	
select * from comments;
select * from newstag;
select * from commentstag;