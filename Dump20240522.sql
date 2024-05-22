CREATE DATABASE  IF NOT EXISTS `appflask` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `appflask`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: appflask
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'Kevin DJ','Kevin12345','Administrador'),(2,'Carla Martinez','Carla012345','Cajero'),(17,'Maria Estevez','Maria12345','Cajero'),(20,'Leo Puente','Leo12345','Almacenista');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` varchar(30) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio` float NOT NULL,
  `cantidad_disponible` int NOT NULL,
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `nombre_UNIQUE` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES ('4542655000005','GALLETAS CHISPAS C/CHOCO 24PZ',17,50),('75001759','BOING MANGO 250ML',18,10),('7503030199681','CHIPS BARCEL FUEGO 55GR',23,27);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `idventas` int NOT NULL AUTO_INCREMENT,
  `total` varchar(100) NOT NULL,
  `fecha` datetime NOT NULL,
  PRIMARY KEY (`idventas`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (2,'809.5','2024-05-05 20:52:54'),(3,'120.0','2024-05-05 20:58:43'),(4,'160.0','2024-05-06 09:49:26'),(5,'46.0','2024-05-06 12:39:38'),(6,'69.0','2024-05-06 12:40:59'),(7,'554.5','2024-05-06 14:07:50'),(8,'115.0','2024-05-13 13:53:06'),(9,'115.0','2024-05-13 13:53:40'),(10,'115.0','2024-05-13 13:54:03'),(11,'30.0','2024-05-15 20:55:33'),(12,'72.0','2024-05-20 13:51:20');
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_productos`
--

DROP TABLE IF EXISTS `ventas_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_productos` (
  `venta_id` int NOT NULL,
  `producto_id` varchar(100) NOT NULL,
  `cantidad` varchar(100) NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_productos`
--

LOCK TABLES `ventas_productos` WRITE;
/*!40000 ALTER TABLE `ventas_productos` DISABLE KEYS */;
INSERT INTO `ventas_productos` VALUES (2,'CHIPS BARCEL FUEGO 55GR','4','2024-05-05 20:52:54'),(2,'BOING MANGO 250ML','4','2024-05-05 20:52:54'),(2,'GALLETAS CHISPAS C/CHOCO 24PZ','5','2024-05-05 20:52:54'),(3,'BOING MANGO 250ML','8','2024-05-05 20:58:43'),(4,'BOING MANGO 250ML','3','2024-05-06 09:49:26'),(4,'CHIPS BARCEL FUEGO 55GR','5','2024-05-06 09:49:26'),(5,'CHIPS BARCEL FUEGO 55GR','2','2024-05-06 12:39:38'),(6,'CHIPS BARCEL FUEGO 55GR','3','2024-05-06 12:40:59'),(7,'CHIPS BARCEL FUEGO 55GR','5','2024-05-06 14:07:50'),(7,'BOING MANGO 250ML','3','2024-05-06 14:07:50'),(7,'GALLETAS CHISPAS C/CHOCO 24PZ','3','2024-05-06 14:07:50'),(8,'CHIPS BARCEL FUEGO 55GR','5','2024-05-13 13:53:06'),(9,'CHIPS BARCEL FUEGO 55GR','5','2024-05-13 13:53:40'),(10,'CHIPS BARCEL FUEGO 55GR','5','2024-05-13 13:54:03'),(11,'BOING MANGO 250ML','2','2024-05-15 20:55:33'),(12,'BOING MANGO 250ML','4','2024-05-20 13:51:20');
/*!40000 ALTER TABLE `ventas_productos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-22 10:28:14
