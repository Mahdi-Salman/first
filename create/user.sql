CREATE TABLE User (
    user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(20) UNIQUE,
    user_type ENUM('CUSTOMER', 'SUPPORT', 'ADMIN') NOT NULL,
    city VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    registration_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    account_status ENUM('ACTIVE', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    CHECK (email IS NOT NULL OR phone_number IS NOT NULL),
    CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' OR email IS NULL),
    CHECK (phone_number REGEXP '^[0-9]{10,15}$' OR phone_number IS NULL)
);

ALTER TABLE User
    DROP COLUMN city;

ALTER TABLE User
    ADD COLUMN city_id BIGINT NOT NULL;
    
ALTER TABLE User
    ADD CONSTRAINT fk_city
        FOREIGN KEY (city_id) REFERENCES City(city_id)
        ON DELETE CASCADE;

CREATE INDEX EMAIL_PASS_IDX
ON USER (EMAIL, PASSWORD_HASH);

INSERT INTO USER (
    USER_ID,
    FIRST_NAME,
    LAST_NAME,
    EMAIL,
    PHONE_NUMBER,
    USER_TYPE,
    CITY,
    PASSWORD_HASH,
    REGISTRATION_DATE,
    ACCOUNT_STATUS
) VALUES (
    1,
    'Ali',
    'Prs',
    'test@test.com',
    '09032948208',
    'CUSTOMER',
    'Ardebil',
    '11f0f5d8293fd1d996210e49d4642dadb6c1463ff9c47c888d45d4a1fb47eb6a',
    '2024-10-04 13:10:19',
    'ACTIVE'
);

INSERT INTO USER (
    USER_ID,
    FIRST_NAME,
    LAST_NAME,
    EMAIL,
    PHONE_NUMBER,
    USER_TYPE,
    CITY,
    PASSWORD_HASH,
    REGISTRATION_DATE,
    ACCOUNT_STATUS
) VALUES (
    2,
    'Mehdi',
    'Salman',
    'test2@test2.com',
    '09938634069',
    'CUSTOMER',
    'Tehran',
    '71a5f574ff500816cea8b3d5fd8555dbee7493773f04870217a111984c0fc13f',
    '2024-10-04 13:20:39',
    'ACTIVE'
);

SELECT 
    USER_ID, 
    FIRST_NAME, 
    LAST_NAME, 
    EMAIL, 
    PHONE_NUMBER, 
    USER_TYPE
FROM USER
WHERE FIRST_NAME = 'Ali';

SELECT 
    USER_ID, 
    FIRST_NAME, 
    LAST_NAME, 
    EMAIL, 
    PHONE_NUMBER, 
    USER_TYPE
FROM USER
WHERE PHONE_NUMBER = '09938634069';
