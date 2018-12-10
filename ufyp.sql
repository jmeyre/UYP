-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: ufyp
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `class` (
  `title` varchar(255) NOT NULL,
  `lvl` varchar(255) NOT NULL,
  `maxCap` int(11) NOT NULL,
  `curSize` int(11) NOT NULL,
  `instructorID` varchar(255) NOT NULL,
  `room` varchar(255) NOT NULL,
  `timeSlotID` varchar(255) NOT NULL,
  `sessionID` varchar(255) NOT NULL,
  `classID` varchar(255) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`classID`),
  KEY `InstructorID` (`instructorID`),
  KEY `sessionID` (`sessionID`),
  KEY `timeSlotID` (`timeSlotID`),
  CONSTRAINT `class_ibfk_4` FOREIGN KEY (`instructorID`) REFERENCES `users` (`id`),
  CONSTRAINT `class_ibfk_5` FOREIGN KEY (`timeSlotID`) REFERENCES `timeslot` (`id`),
  CONSTRAINT `class_ibfk_6` FOREIGN KEY (`sessionID`) REFERENCES `sessions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `disability`
--

DROP TABLE IF EXISTS `disability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `disability` (
  `studentID` varchar(255) DEFAULT NULL,
  `disability` varchar(255) NOT NULL,
  UNIQUE KEY `studentID_2` (`studentID`,`disability`),
  KEY `studentID` (`studentID`),
  CONSTRAINT `disability_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disability`
--

LOCK TABLES `disability` WRITE;
/*!40000 ALTER TABLE `disability` DISABLE KEYS */;
/*!40000 ALTER TABLE `disability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gt`
--

DROP TABLE IF EXISTS `gt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `gt` (
  `studentID` varchar(255) NOT NULL,
  `schoolID` varchar(255) NOT NULL,
  UNIQUE KEY `schoolID` (`schoolID`,`studentID`),
  KEY `studentID` (`studentID`),
  CONSTRAINT `gt_ibfk_1` FOREIGN KEY (`schoolID`) REFERENCES `school` (`schoolid`),
  CONSTRAINT `gt_ibfk_2` FOREIGN KEY (`studentID`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gt`
--

LOCK TABLES `gt` WRITE;
/*!40000 ALTER TABLE `gt` DISABLE KEYS */;
/*!40000 ALTER TABLE `gt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guardian`
--

DROP TABLE IF EXISTS `guardian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `guardian` (
  `studentID` varchar(255) NOT NULL,
  `fName` varchar(255) NOT NULL,
  `mName` varchar(255) DEFAULT NULL,
  `lName` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip` varchar(255) NOT NULL,
  KEY `studentID` (`studentID`),
  CONSTRAINT `guardian_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guardian`
--

LOCK TABLES `guardian` WRITE;
/*!40000 ALTER TABLE `guardian` DISABLE KEYS */;
INSERT INTO `guardian` VALUES ('722274','asdf','asdff','adsf','1234567890','asdf@asdf.com','asdf','asdf','AL','77777'),('507509','asdf','asdff','asdff','1234567890','asdf@asdf.com','asdf','asdff','AL','77777');
/*!40000 ALTER TABLE `guardian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `healthcondition`
--

DROP TABLE IF EXISTS `healthcondition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `healthcondition` (
  `studentID` varchar(255) DEFAULT NULL,
  `cond` varchar(255) NOT NULL,
  `descript` varchar(255) NOT NULL,
  UNIQUE KEY `studentID_2` (`studentID`,`cond`),
  KEY `studentID` (`studentID`),
  CONSTRAINT `healthcondition_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `healthcondition`
--

LOCK TABLES `healthcondition` WRITE;
/*!40000 ALTER TABLE `healthcondition` DISABLE KEYS */;
/*!40000 ALTER TABLE `healthcondition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mentor`
--

DROP TABLE IF EXISTS `mentor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `mentor` (
  `studentID` varchar(255) NOT NULL,
  `instructorID` varchar(255) NOT NULL,
  `YR` year(4) NOT NULL,
  UNIQUE KEY `studentID` (`studentID`,`instructorID`,`YR`),
  UNIQUE KEY `studentID_2` (`studentID`,`instructorID`,`YR`),
  KEY `instructorID` (`instructorID`),
  CONSTRAINT `mentor_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `students` (`id`),
  CONSTRAINT `mentor_ibfk_2` FOREIGN KEY (`instructorID`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mentor`
--

LOCK TABLES `mentor` WRITE;
/*!40000 ALTER TABLE `mentor` DISABLE KEYS */;
/*!40000 ALTER TABLE `mentor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school`
--

DROP TABLE IF EXISTS `school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `school` (
  `studentID` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `district` varchar(255) NOT NULL,
  `schoolID` varchar(255) NOT NULL,
  PRIMARY KEY (`schoolID`),
  UNIQUE KEY `studentID_2` (`studentID`,`name`),
  KEY `studentID` (`studentID`),
  CONSTRAINT `school_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school`
--

LOCK TABLES `school` WRITE;
/*!40000 ALTER TABLE `school` DISABLE KEYS */;
/*!40000 ALTER TABLE `school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sessions` (
  `id` varchar(255) NOT NULL,
  `year` year(4) NOT NULL,
  `endDate` date NOT NULL,
  `startDate` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `endDate` (`endDate`,`startDate`,`year`),
  UNIQUE KEY `startDate` (`startDate`),
  UNIQUE KEY `endDate_2` (`endDate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `siblings`
--

DROP TABLE IF EXISTS `siblings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `siblings` (
  `studentID` varchar(255) NOT NULL,
  `siblingID` varchar(255) NOT NULL,
  UNIQUE KEY `studentID` (`studentID`,`siblingID`),
  KEY `siblingID` (`siblingID`),
  CONSTRAINT `siblings_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `students` (`id`),
  CONSTRAINT `siblings_ibfk_2` FOREIGN KEY (`siblingID`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `siblings`
--

LOCK TABLES `siblings` WRITE;
/*!40000 ALTER TABLE `siblings` DISABLE KEYS */;
/*!40000 ALTER TABLE `siblings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `staff` (
  `id` varchar(6) NOT NULL,
  `fName` varchar(255) NOT NULL,
  `mName` varchar(255) DEFAULT NULL,
  `lName` varchar(255) NOT NULL,
  `suffix` varchar(255) DEFAULT NULL,
  `phone` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip` varchar(255) NOT NULL,
  KEY `id` (`id`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES ('000001','Bobby',NULL,'Baylor',NULL,'2547103871','Bobby_Baylor@baylor.edu','One Bear Place #97356','Waco','TX','76798');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `students` (
  `id` varchar(6) NOT NULL,
  `fName` varchar(255) DEFAULT NULL,
  `mName` varchar(255) DEFAULT NULL,
  `lName` varchar(255) DEFAULT NULL,
  `suffix` varchar(255) DEFAULT NULL,
  `preferred` varchar(255) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `race` varchar(255) DEFAULT NULL,
  `gradeLevel` varchar(255) DEFAULT NULL,
  `expGradDate` date DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `zip` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `esl` tinyint(1) DEFAULT NULL,
  `gt` tinyint(1) DEFAULT NULL,
  `acceptedYear` year(4) NOT NULL,
  `acceptedBy` varchar(6) NOT NULL,
  `bill` int(11) NOT NULL,
  `NCHI` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `grantFunded` varchar(255) DEFAULT NULL,
  `otherInfo` varchar(8000) DEFAULT NULL,
  `expSchool` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`),
  KEY `acceptedBy` (`acceptedBy`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`id`) REFERENCES `users` (`id`),
  CONSTRAINT `students_ibfk_2` FOREIGN KEY (`acceptedBy`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('507509','asdf','','asdf','','','1998-07-07','Male','Caucasian','12th','0000-00-00','asdf','asdf','AL','77777','','',NULL,NULL,2018,'000001',20,NULL,NULL,NULL,'asldkfjlsadkhfhjfjlqwneflwqefkjjqwfiuhfosadjaskjkjbqwrkjgbqkuhoasdjfnflsadjfbsaldjfb',NULL),('722274','John','','Eyre','','','1998-07-07','Female','African American','6th','2016-06-20','asdf','asdf','TX','77777','','',NULL,NULL,2018,'000001',20,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `takes`
--

DROP TABLE IF EXISTS `takes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `takes` (
  `studentID` varchar(255) NOT NULL,
  `classID` varchar(255) NOT NULL,
  UNIQUE KEY `studentID` (`studentID`,`classID`),
  KEY `classID` (`classID`),
  CONSTRAINT `takes_ibfk_1` FOREIGN KEY (`studentID`) REFERENCES `students` (`id`),
  CONSTRAINT `takes_ibfk_2` FOREIGN KEY (`classID`) REFERENCES `class` (`classid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `takes`
--

LOCK TABLES `takes` WRITE;
/*!40000 ALTER TABLE `takes` DISABLE KEYS */;
/*!40000 ALTER TABLE `takes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timeslot`
--

DROP TABLE IF EXISTS `timeslot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `timeslot` (
  `id` varchar(4) NOT NULL,
  `startTime` time NOT NULL,
  `endTime` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timeslot`
--

LOCK TABLES `timeslot` WRITE;
/*!40000 ALTER TABLE `timeslot` DISABLE KEYS */;
INSERT INTO `timeslot` VALUES ('1234','09:45:00','11:15:00'),('2345','13:15:00','14:45:00');
/*!40000 ALTER TABLE `timeslot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `id` varchar(6) NOT NULL,
  `category` varchar(255) NOT NULL,
  `pword` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('000001','Staff','$2b$12$syivdenDKojWCsPxTU/q2ON2zI6BUBi6XnWXF50rclVTWklreAOci'),('507509','Student','$2b$12$eGzAqKvamMsn24RqvxZOpeygyZMw.cjjl0aZdFmlc6FFIan57LbNy'),('722274','Student','$2b$12$Jtf0aq/MvSyNJlb8pbkesuKIJc295q20Z/9n3E8b8qLLFetf0AIYy');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-10 10:00:21
