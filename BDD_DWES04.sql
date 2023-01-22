-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dwes04
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clients` (
  `idclient` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(30) NOT NULL,
  `llinatges` varchar(50) NOT NULL,
  `telefon` varchar(12) NOT NULL,
  PRIMARY KEY (`idclient`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (1,'Miquel','Mir','632452314'),(2,'Joana','Pons','656998877'),(3,'Laura ','Gonzalez','696568423'),(4,'Fernando','Gomez','55500051'),(5,'Pere','Pol','74412551');
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pistes`
--

DROP TABLE IF EXISTS `pistes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pistes` (
  `idpista` int NOT NULL AUTO_INCREMENT,
  `tipo` enum('Coberta','Exterior','','') NOT NULL,
  `preu` int NOT NULL,
  PRIMARY KEY (`idpista`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pistes`
--

LOCK TABLES `pistes` WRITE;
/*!40000 ALTER TABLE `pistes` DISABLE KEYS */;
INSERT INTO `pistes` VALUES (1,'Coberta',12),(2,'Exterior',8);
/*!40000 ALTER TABLE `pistes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserves`
--

DROP TABLE IF EXISTS `reserves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserves` (
  `data` datetime NOT NULL,
  `idpista` int NOT NULL,
  `idclient` int NOT NULL,
  PRIMARY KEY (`data`,`idpista`),
  KEY `idclient` (`idclient`),
  KEY `idpista` (`idpista`),
  CONSTRAINT `reserves_ibfk_2` FOREIGN KEY (`idpista`) REFERENCES `pistes` (`idpista`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserves`
--

LOCK TABLES `reserves` WRITE;
/*!40000 ALTER TABLE `reserves` DISABLE KEYS */;
INSERT INTO `reserves` VALUES ('2015-00-00 00:00:00',2,1),('2021-01-17 15:00:00',1,1),('2021-01-17 16:00:00',1,1),('2021-11-04 16:00:00',2,1),('2021-11-22 15:00:00',1,1),('2022-12-01 15:00:00',1,1),('2022-12-08 15:00:00',2,1),('2022-12-13 18:00:00',1,1),('2022-12-14 15:00:00',1,1),('2022-12-14 15:00:00',2,1),('2022-12-15 15:00:00',1,1),('2022-12-23 15:00:00',1,1),('2022-12-27 15:00:00',2,1),('2022-12-29 15:00:00',1,1),('2021-10-20 18:00:00',2,2),('2021-11-01 19:00:00',1,2),('2022-12-14 16:00:00',2,2),('2022-12-28 16:00:00',1,2),('2021-10-20 18:00:00',1,3),('2022-12-06 16:00:00',2,3);
/*!40000 ALTER TABLE `reserves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuaris`
--

DROP TABLE IF EXISTS `usuaris`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuaris` (
  `idusuari` int NOT NULL AUTO_INCREMENT,
  `cuenta` varchar(15) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `llinatges` varchar(50) NOT NULL,
  `pwd` varchar(200) DEFAULT NULL,
  `alta` date DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefon` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`idusuari`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuaris`
--

LOCK TABLES `usuaris` WRITE;
/*!40000 ALTER TABLE `usuaris` DISABLE KEYS */;
INSERT INTO `usuaris` VALUES (1,'gomez.romano','Fernando','Gomez','pbkdf2:sha256:260000$i8cyzDCo$b1506314c0e571280925689ca0816de1774066b29cd25abbc35ec5ad4b6fa1b2','2023-01-20','gomez_romano@yahoo.es','(0034)661381170');
/*!40000 ALTER TABLE `usuaris` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-20 23:38:12
