CREATE DATABASE `score-analyse` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `score-analyse`;

-- `score-analyse`.`user` definition

CREATE TABLE `user`
(
    `username` varchar(100)          NOT NULL,
    `password` varchar(200)          NOT NULL,
    `role`     enum ('admin','user') NOT NULL,
    PRIMARY KEY (`username`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- `score-analyse`.`generate-certificate` definition

CREATE TABLE `generate-certificate`
(
    `CertificateNumber` varchar(100) NOT NULL,
    `StudentNumber`     varchar(100) NOT NULL,
    `StudentName`       varchar(100) NOT NULL,
    `PassedType`        varchar(100) NOT NULL,
    PRIMARY KEY (`StudentNumber`),
    UNIQUE KEY `generate_certificate_un` (`CertificateNumber`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

