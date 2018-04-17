CREATE TABLE `students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `last_name_second` varchar(100) DEFAULT NULL,
  `NIA` varchar(9) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `professors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `last_name_second` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `assigments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `course` varchar(100) DEFAULT NULL,
  `id_professor` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `professor_idx` (`id_professor`),
  CONSTRAINT `professor` FOREIGN KEY (`id_professor`) REFERENCES `professors` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

CREATE TABLE `sections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_assigment` int(11) DEFAULT NULL,
  `order_in_assigment` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `text` text,
  PRIMARY KEY (`id`),
  KEY `assigment_idx` (`id_assigment`),
  CONSTRAINT `assigment` FOREIGN KEY (`id_assigment`) REFERENCES `assigments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;


CREATE TABLE `doubts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text,
  `section` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `section_idx` (`section`),
  CONSTRAINT `section` FOREIGN KEY (`section`) REFERENCES `sections` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=212 DEFAULT CHARSET=utf8 COMMENT='This table represents the students'' doubts';

CREATE TABLE `doubt_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doubt` int(11) NOT NULL,
  `student` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_idx` (`student`),
  KEY `doubt` (`doubt`),
  CONSTRAINT `doubt` FOREIGN KEY (`doubt`) REFERENCES `doubts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `student` FOREIGN KEY (`student`) REFERENCES `students` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;


CREATE TABLE `answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `doubt` int(11) NOT NULL,
  `text` text NOT NULL,
  `aproved` int(11) DEFAULT NULL COMMENT 'Check if the answer is aproved by a proffesor, and how did it.',
  PRIMARY KEY (`id`),
  KEY `doubt_idx` (`doubt`),
  KEY `answers_aproved_idx` (`aproved`),
  CONSTRAINT `answer_doubt_fk` FOREIGN KEY (`doubt`) REFERENCES `doubts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `answers_aproved` FOREIGN KEY (`aproved`) REFERENCES `professors` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `answer_resolvers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answer` int(11) NOT NULL,
  `student` int(11) DEFAULT NULL,
  `professor` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `answer_professor_fk_idx` (`professor`),
  KEY `answer_student_fk_idx` (`student`),
  KEY `answer_idx` (`answer`),
  CONSTRAINT `answer` FOREIGN KEY (`answer`) REFERENCES `answers` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `answer_professor_fk` FOREIGN KEY (`professor`) REFERENCES `professors` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `answer_student_fk` FOREIGN KEY (`student`) REFERENCES `students` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
