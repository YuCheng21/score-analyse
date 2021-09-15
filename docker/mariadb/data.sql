USE `score-analyse`;

INSERT INTO `score-analyse`.`user` (username, password, `role`)
VALUES ('admin',
        'pbkdf2:sha256:260000$SBRuUIDDkL2lLIak$9bd41e7580c5598bf39307f29260305e6c8818fc519d6c454be224d37682eeff',
        'admin');