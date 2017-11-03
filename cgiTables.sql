create table if not exists user (
	user_id int not null autoincrement,
	username varchar(50) not null,
	email varchar(50) not null,
	password varchar(50)
	entry_date datetime not null default current_timestamp,
    
	constraint pk_user primary key(userId),
	constraint uc_user_username(username),
	constraint uc_user_email unique(email)
)

create table if not exists product (
	product_id int not null autoincrement,
	entry_date datetime not null default current_timestamp,
descr varchar(100),
price decimal(13,2),
image_path varchar(1024)
    
	constraint pk_product primary key(product_id),
CONSTRAINT fk_product FOREIGN KEY (userr_id)
  	REFERENCES user(product_id)
  	ON DELETE CASCADE
  	ON UPDATE CASCADE
)


