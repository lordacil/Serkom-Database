/*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: perpustakaan
-- ------------------------------------------------------
-- Server version	11.4.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `Anggota`
--

DROP TABLE IF EXISTS `Anggota`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Anggota` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  `alamat` text NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Anggota`
--

LOCK TABLES `Anggota` WRITE;
/*!40000 ALTER TABLE `Anggota` DISABLE KEYS */;
INSERT INTO `Anggota` VALUES
(1,'rizky nugraha','ciktim rt02/11','2001-01-28','rizky@gmail.com'),
(2,'aliando nugraha','sydney manado','2001-01-01','aliando@gmail.com'),
(3,'Salsabilla Tya Vella','kerinci, jambi, sumatera barat','2006-08-08','salsa@gmail.com'),
(4,'Arch Linux Enjoyer','Miami, EU States origin','1895-11-20','arch@yahoo.com'),
(5,'Megan Trainor','Sydney Rt02/11','1995-02-05','megan12@gmail.com'),
(8,'test','test','2001-01-01','test');
/*!40000 ALTER TABLE `Anggota` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Buku`
--

DROP TABLE IF EXISTS `Buku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Buku` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `judul` varchar(255) NOT NULL,
  `pengarang` varchar(100) NOT NULL,
  `tahun_terbit` year(4) NOT NULL,
  `kategori_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `kategori_id` (`kategori_id`),
  CONSTRAINT `Buku_ibfk_1` FOREIGN KEY (`kategori_id`) REFERENCES `Kategori` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Buku`
--

LOCK TABLES `Buku` WRITE;
/*!40000 ALTER TABLE `Buku` DISABLE KEYS */;
INSERT INTO `Buku` VALUES
(1,'Ancika 1998','Fidi baiq',2020,2),
(2,'The Dragon Republic','R. F. Kuang',2020,3),
(3,'Misteri Danau Limo','Sulastri W.A',1945,4);
/*!40000 ALTER TABLE `Buku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Kategori`
--

DROP TABLE IF EXISTS `Kategori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Kategori` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Kategori`
--

LOCK TABLES `Kategori` WRITE;
/*!40000 ALTER TABLE `Kategori` DISABLE KEYS */;
INSERT INTO `Kategori` VALUES
(1,'Fiksi'),
(2,'Cyberpunk'),
(3,'Fantasy, Sci-fi, Dungeon'),
(4,'Horror'),
(5,'Anime');
/*!40000 ALTER TABLE `Kategori` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Peminjaman`
--

DROP TABLE IF EXISTS `Peminjaman`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Peminjaman` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `buku_id` int(11) DEFAULT NULL,
  `anggota_id` int(11) DEFAULT NULL,
  `tanggal_pinjam` date NOT NULL,
  `tanggal_kembali` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `buku_id` (`buku_id`),
  KEY `anggota_id` (`anggota_id`),
  CONSTRAINT `Peminjaman_ibfk_1` FOREIGN KEY (`buku_id`) REFERENCES `Buku` (`id`),
  CONSTRAINT `Peminjaman_ibfk_2` FOREIGN KEY (`anggota_id`) REFERENCES `Anggota` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Peminjaman`
--

LOCK TABLES `Peminjaman` WRITE;
/*!40000 ALTER TABLE `Peminjaman` DISABLE KEYS */;
INSERT INTO `Peminjaman` VALUES
(2,1,1,'2024-08-03','2024-08-10'),
(4,1,3,'2001-08-08','2001-08-10'),
(5,1,1,'2001-01-01','2001-02-02'),
(6,1,2,'2001-01-01','2001-02-02'),
(7,1,3,'2001-02-03','2001-02-05'),
(9,1,4,'2024-08-05','2024-08-10');
/*!40000 ALTER TABLE `Peminjaman` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `anggota_id` int(11) DEFAULT NULL,
  `role` enum('admin','anggota') DEFAULT 'anggota',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `anggota_id` (`anggota_id`),
  CONSTRAINT `Users_ibfk_1` FOREIGN KEY (`anggota_id`) REFERENCES `Anggota` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES
(1,'admin','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3',1,'admin'),
(2,'rizky','59e19706d51d39f66711c2653cd7eb1291c94d9b55eb14bda74ce4dc636d015a',2,'anggota'),
(3,'salsa','8fc8c88b0d3e4d8485bdb394cb05b79d7a893b1201ebaf4b31eebfa394333aa9',3,'anggota'),
(4,'linux','890cabe271136403326f8252c59cfdd47160fa63fe7a37801d3bffc1dbbf03f3',4,'anggota');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'perpustakaan'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-08-06 19:24:09
