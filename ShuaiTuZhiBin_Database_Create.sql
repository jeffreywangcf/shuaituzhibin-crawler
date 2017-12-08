CREATE TABLE `ShuaiTuZhiBin_Database`(
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `名字` VARCHAR(20) NOT NULL,
  `国家` VARCHAR(4) NOT NULL,
  `星级` SMALLINT NOT NULL,
  `图片地址` VARCHAR(30) NOT NULL,
  `描述` VARCHAR(500) NOT NULL,
  `兵种` VARCHAR(5) NOT NULL,
  `cost` DOUBLE NOT NULL,
  `攻击距离` INT NOT NULL,
  `攻击` INT NOT NULL,
  `策略` INT NOT NULL,
  `攻城` INT NOT NULL,
  `防御` INT NOT NULL,
  `速度` INT NOT NULL,
  `战法` VARCHAR(100) NOT NULL,
  `可拆解战法` VARCHAR(100) NOT NULL
)DEFAULT CHARSET 'UTF8';
