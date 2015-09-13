CREATE TABLE program_book (
        id INT NOT NULL AUTO_INCREMENT,
        rating FLOAT(3,1), -- 评分
        votes INT, -- 评价人数
        image_name VARCHAR(30) NOT NULL,
        title VARCHAR(70) NOT NULL,
        subtitle VARCHAR(70),
        origin VARCHAR(70), -- 原作名
        description VARCHAR(120) ,
        author VARCHAR(100),
        translator VARCHAR(100),
        publisher VARCHAR(50),
        publish_date DATE,
        page_number SMALLINT,
        price VARCHAR(10),
        binding_type VARCHAR(16), -- 装帧类型
        series VARCHAR(30), -- 丛书
        ISBN CHAR(13) UNIQUE,
        introduction VARCHAR(2000), -- 内容简介
        PRIMARY KEY(id)
    );
