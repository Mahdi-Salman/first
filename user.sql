CREATE TABLE user (
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    main_role ENUM('passenger', 'admin'),
    hometown VARCHAR(50),
    password_hash VARCHAR(100),
    login_date TIMESTAMP,
    account_status ENUM('active', 'deactvie')
);
