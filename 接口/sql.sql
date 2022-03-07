CREATE TABLE Mayor_mail(

content_index INT NOT NULL AUTO_INCREMENT,

question_number CHAR(50),

question_title CHAR(50),

question_url CHAR(50),

question_end CHAR(50),

question_clickNum INT(20),

question_content CHAR(200),

question_time CHAR(30),

response_content longtext,

response_time CHAR(30),

response_department CHAR(30),
PRIMARY KEY(content_index))
DEFAULT CHARSET=utf8;
