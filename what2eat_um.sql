-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: what2eat_um
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `business_hour`
--

DROP TABLE IF EXISTS `business_hour`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `business_hour` (
  `id` int NOT NULL AUTO_INCREMENT,
  `restaurant_id` int NOT NULL,
  `day_of_week` int NOT NULL,
  `open_time` time NOT NULL,
  `close_time` time NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_restaurant_day_uc` (`restaurant_id`,`day_of_week`),
  CONSTRAINT `business_hour_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=332 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_hour`
--

LOCK TABLES `business_hour` WRITE;
/*!40000 ALTER TABLE `business_hour` DISABLE KEYS */;
INSERT INTO `business_hour` VALUES (213,1,0,'08:00:00','22:00:00'),(214,1,1,'08:00:00','22:00:00'),(215,1,2,'08:00:00','22:00:00'),(216,1,3,'08:00:00','22:00:00'),(217,1,4,'08:00:00','22:00:00'),(218,1,5,'08:00:00','22:00:00'),(219,1,6,'08:00:00','22:00:00'),(220,2,0,'08:00:00','22:00:00'),(221,2,1,'08:00:00','22:00:00'),(222,2,2,'08:00:00','22:00:00'),(223,2,3,'08:00:00','22:00:00'),(224,2,4,'08:00:00','22:00:00'),(225,2,5,'08:00:00','22:00:00'),(226,2,6,'08:00:00','22:00:00'),(227,3,0,'08:00:00','20:00:00'),(228,3,1,'08:00:00','20:00:00'),(229,3,2,'08:00:00','20:00:00'),(230,3,3,'08:00:00','20:00:00'),(231,3,4,'08:00:00','20:00:00'),(232,3,5,'08:00:00','20:00:00'),(233,3,6,'08:00:00','20:00:00'),(234,4,0,'08:00:00','22:00:00'),(235,4,1,'08:00:00','22:00:00'),(236,4,2,'08:00:00','22:00:00'),(237,4,3,'08:00:00','22:00:00'),(238,4,4,'08:00:00','22:00:00'),(239,4,5,'08:00:00','22:00:00'),(240,4,6,'08:00:00','22:00:00'),(241,5,0,'08:30:00','21:00:00'),(242,5,1,'08:30:00','21:00:00'),(243,5,2,'08:30:00','21:00:00'),(244,5,3,'08:30:00','21:00:00'),(245,5,4,'08:30:00','21:00:00'),(246,5,5,'08:30:00','21:00:00'),(247,5,6,'08:30:00','21:00:00'),(255,7,0,'10:00:00','22:00:00'),(256,7,1,'10:00:00','22:00:00'),(257,7,2,'10:00:00','22:00:00'),(258,7,3,'10:00:00','22:00:00'),(259,7,4,'10:00:00','22:00:00'),(260,7,5,'10:00:00','22:00:00'),(261,7,6,'10:00:00','22:00:00'),(262,8,0,'10:00:00','22:00:00'),(263,8,1,'10:00:00','22:00:00'),(264,8,2,'10:00:00','22:00:00'),(265,8,3,'10:00:00','22:00:00'),(266,8,4,'10:00:00','22:00:00'),(267,8,5,'10:00:00','22:00:00'),(268,8,6,'10:00:00','22:00:00'),(269,10,0,'10:00:00','22:00:00'),(270,10,1,'10:00:00','22:00:00'),(271,10,2,'10:00:00','22:00:00'),(272,10,3,'10:00:00','22:00:00'),(273,10,4,'10:00:00','22:00:00'),(274,10,5,'10:00:00','22:00:00'),(275,10,6,'10:00:00','22:00:00'),(276,9,0,'10:00:00','22:00:00'),(277,9,1,'10:00:00','22:00:00'),(278,9,2,'10:00:00','22:00:00'),(279,9,3,'10:00:00','22:00:00'),(280,9,4,'10:00:00','22:00:00'),(281,9,5,'10:00:00','22:00:00'),(282,9,6,'10:00:00','22:00:00'),(283,11,0,'10:00:00','22:00:00'),(284,11,1,'10:00:00','22:00:00'),(285,11,2,'10:00:00','22:00:00'),(286,11,3,'10:00:00','22:00:00'),(287,11,4,'10:00:00','22:00:00'),(288,11,5,'10:00:00','22:00:00'),(289,11,6,'10:00:00','22:00:00'),(290,12,0,'10:00:00','22:00:00'),(291,12,1,'10:00:00','22:00:00'),(292,12,2,'10:00:00','22:00:00'),(293,12,3,'10:00:00','22:00:00'),(294,12,4,'10:00:00','22:00:00'),(295,12,5,'10:00:00','22:00:00'),(296,12,6,'10:00:00','22:00:00'),(297,13,0,'10:00:00','22:00:00'),(298,13,1,'10:00:00','22:00:00'),(299,13,2,'10:00:00','22:00:00'),(300,13,3,'10:00:00','22:00:00'),(301,13,4,'10:00:00','22:00:00'),(302,13,5,'10:00:00','22:00:00'),(303,13,6,'10:00:00','22:00:00'),(304,14,0,'07:00:00','23:00:00'),(305,14,1,'07:00:00','23:00:00'),(306,14,2,'07:00:00','23:00:00'),(307,14,3,'07:00:00','23:00:00'),(308,14,4,'07:00:00','23:00:00'),(309,14,5,'07:00:00','23:00:00'),(310,14,6,'07:00:00','23:00:00'),(311,15,0,'11:30:00','20:00:00'),(312,15,1,'11:30:00','20:00:00'),(313,15,2,'11:30:00','20:00:00'),(314,15,3,'11:30:00','20:00:00'),(315,15,4,'11:30:00','20:00:00'),(316,15,5,'11:30:00','20:00:00'),(317,15,6,'11:30:00','20:00:00'),(318,16,0,'08:00:00','22:00:00'),(319,16,1,'08:00:00','22:00:00'),(320,16,2,'08:00:00','22:00:00'),(321,16,3,'08:00:00','22:00:00'),(322,16,4,'08:00:00','22:00:00'),(323,16,5,'08:00:00','22:00:00'),(324,16,6,'08:00:00','22:00:00'),(325,6,0,'11:00:00','20:00:00'),(326,6,1,'11:00:00','20:00:00'),(327,6,2,'11:00:00','20:00:00'),(328,6,3,'11:00:00','20:00:00'),(329,6,4,'11:00:00','20:00:00'),(330,6,5,'11:00:00','20:00:00'),(331,6,6,'11:00:00','20:00:00');
/*!40000 ALTER TABLE `business_hour` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `title` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `promotion_id` int DEFAULT NULL,
  PRIMARY KEY (`notification_id`),
  KEY `user_id` (`user_id`),
  KEY `promotion_id` (`promotion_id`),
  CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `notification_ibfk_2` FOREIGN KEY (`promotion_id`) REFERENCES `promotion` (`promotion_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (1,'4b045935ef243920679945e1b0f9bb6b','New Restaurant Claim','A new claim for 香榭里 Élysée Bakery has been submitted by Eric. Please review it.',0,'2025-05-03 10:21:58',NULL),(2,'ddc5f0cddef0842fbb8ac7fa577b8ea5','Restaurant Claim Approved','Your claim for 香榭里 Élysée Bakery has been approved! You can now manage this restaurant.',0,'2025-05-03 10:23:54',NULL);
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotion`
--

DROP TABLE IF EXISTS `promotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promotion` (
  `promotion_id` int NOT NULL AUTO_INCREMENT,
  `restaurant_id` int NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` varchar(50) NOT NULL,
  PRIMARY KEY (`promotion_id`),
  KEY `restaurant_id` (`restaurant_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `promotion_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`),
  CONSTRAINT `promotion_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotion`
--

LOCK TABLES `promotion` WRITE;
/*!40000 ALTER TABLE `promotion` DISABLE KEYS */;
INSERT INTO `promotion` VALUES (1,1,'考試期間限定優惠','下午茶時段購買麵包或蛋糕加MOP18換購指定咖啡或飲品','2025-05-02 15:00:00','2025-05-19 18:00:00','promotions/80e8d17ce6a5427fa8eb0a2f0521027c_elysee_a3_2025-scaled.jpg','2025-05-03 10:45:45','ddc5f0cddef0842fbb8ac7fa577b8ea5');
/*!40000 ALTER TABLE `promotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reply`
--

DROP TABLE IF EXISTS `reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reply` (
  `reply_id` int NOT NULL AUTO_INCREMENT,
  `review_id` int NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`reply_id`),
  KEY `review_id` (`review_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reply_ibfk_1` FOREIGN KEY (`review_id`) REFERENCES `review` (`review_id`),
  CONSTRAINT `reply_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply`
--

LOCK TABLES `reply` WRITE;
/*!40000 ALTER TABLE `reply` DISABLE KEYS */;
INSERT INTO `reply` VALUES (1,1,'ddc5f0cddef0842fbb8ac7fa577b8ea5','I agree.','2025-05-03 06:36:16',NULL);
/*!40000 ALTER TABLE `reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant` (
  `restaurant_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `location` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `cuisine_type` enum('CHINESE','CANTONESE','WESTERN','ASIAN','FAST_FOOD','VEGETARIAN','DESSERT','BEVERAGE','OTHER') NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `manager_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `restaurant_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant`
--

LOCK TABLES `restaurant` WRITE;
/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` VALUES (1,'香榭里 Élysée Bakery','N1-G005','University of Macau','WESTERN','The Élysée Bakery in Macao is the first restaurant opened by the Champs Elysees Bakery brand. In addition to the well-known traditional French baked bread and desserts, it also provides Western cuisine that combines high-quality European ingredients with French cooking techniques.\r\n\r\nContact: 2843 1881','2025-05-02 15:42:32',1,'ddc5f0cddef0842fbb8ac7fa577b8ea5'),(2,'玫瑰园 Café Rose Garden','E2-G036','University of Macau','ASIAN','The Cafe Rose Garden, which specializes in premium coffee, is located on the ground floor of the North Wing of the University Library E2 and is decorated in a casual and stylish style. It opens for breakfast and offers a wide range of dishes for lunch, afternoon tea, and dinner, including Chinese and Western cuisine, salads, light meals, tea, coffee, desserts, and bakery.\r\n\r\nContact: 2843 1881','2025-05-02 15:46:50',0,NULL),(3,'時光屋 KITCHENext','E5-G081, E6-G091','E5-G081, E6-G091','ASIAN','The \" KITCHENext\" restaurant is located on the ground floor of the Central Teaching Building E5E6. It is stylishly decorated and provides about 300 seats. It serves a selection of dishes in different styles, including Chinese, Western and Japanese.\r\n\r\nContact: 2843 1881','2025-05-02 16:17:09',0,NULL),(4,'賽百味 SUBWAY','S8-G016','S8-G016','FAST_FOOD','Subway is a multinational fast-food chain that primarily sells sandwiches, wraps, salads, drinks and snacks.\r\n\r\nContact: 2825 9231','2025-05-02 16:23:35',0,NULL),(5,'小郡肝 SIU GWAN GON','S8-1008, 1009','S8-1008, 1009','CHINESE','Yinyuan SIU GWAN GON specializes in hot pot mutton and beef, northern stir-fries and noodles.\r\n\r\nContact: 2893 3292\r\n','2025-05-02 16:26:44',0,NULL),(6,'筷子 CHOPSTICKS','S8-1005','S8-1005','ASIAN','Chopsticks is a brand new takeaway store brand under Tangzhu, which combines modern catering management mode with modern store design. It provides a variety of simple light meals and traditional Sichuan-style rice noodles, mainly Japanese rice bowls, ramen, Sichuan spicy rice noodles and spicy hand-shredded chicken.\r\n\r\nContact: 2850 6789','2025-05-02 16:28:03',0,NULL),(7,'包原味 BAOYUANWEI','S8-1001, 1003','S8-1001, 1003','CHINESE','Baoyuanwei provides rice, buns, snacks, pastries, etc.\r\n\r\nContact: 6591 2117 (Koufu Food Court)','2025-05-02 16:29:58',0,NULL),(8,'廣東順德美食 Guangdong Shunde Food','S8-1001, 1003','S8-1001, 1003','CHINESE','Shunde is an important birthplace of Cantonese cuisine and a famous food capital. As the saying goes, \"Food is in Guangzhou, and cooking comes from Fengcheng (Daliang)\". Shunde cuisine is characterized by \"clear, fresh, refreshing, tender and smooth\", and pays attention to color, fragrance and taste. Shunde cuisine also absorbs the local food culture of Macau and focuses on quality.\r\n\r\nContact: 6591 2117 (Koufu Food Court)','2025-05-02 16:31:30',0,NULL),(9,'袁記雲餃 Yuan Ji Dumplings','S8-1001, 1003','S8-1001, 1003','CHINESE','Yuan Ji Dumplings was founded in 2012 and is a Cantonese-style dumpling restaurant chain brand that specializes in freshly made dumplings, wontons and pasta products.\r\n\r\nContact: 6591 2117 (Koufu Food Court)','2025-05-02 16:32:41',0,NULL),(10,'叉燒皇 CHA SIO WONG','S8-1001, 1003','S8-1001, 1003','CHINESE','CHA SIO WONG is a brand that strives to blend traditional and modern barbecue flavors. While fully inheriting the traditional Hong Kong barbecue craftsmanship, it also uses Western cooking styles to add layers and characteristics to the food.\r\n\r\nContact: 6591 2117 (Koufu Food Court)','2025-05-02 16:34:28',0,NULL),(11,'王記腸旺面 Wang Kee Intestine Noodles','S8-1001, 1003','S8-1001, 1003','CHINESE','Contact: 6591 2117 (Koufu Food Court)','2025-05-02 16:35:36',0,NULL),(12,'金富美食 ESTABELECIMENTO DE COMIDAS KAM FU','S8-1001, 1003','S8-1001, 1003','CHINESE','ESTABELECIMENTO DE COMIDAS KAM FU offers customers savory Chinese stir-fries and a variety of fried rice and noodles.\r\n\r\nContact: 6591 2117 (Koufu Food Court)','2025-05-02 16:36:57',0,NULL),(13,'蘭州拉面館 LAN ZHOU LA MIAN GUAN','S8-1001, 1003','S8-1001, 1003','CHINESE','\" LAN ZHOU LA MIAN GUAN \" has been operating in Macau for more than ten years and has several branches. It is famous for its Lanzhou beef noodles. The taste of handmade noodles and the unique soup base will let you feel the charm of Lanzhou Ramen.\r\n\r\nContact: 6591 2117 (Koufu Food Court)','2025-05-02 16:38:13',0,NULL),(14,'麥當勞 McDonald\'s','S1-G016, G017, G018','S1-G016, G017, G018','FAST_FOOD',' McDonald\'s not only provides fast food service, we value your favorite taste, lifestyle, preferences and create every surprise moment for you!\r\nProduct types include breakfast products, burgers, French fries, crispy chicken wings, soda, coffee and desserts, and also provide a variety of value-for-money packages.\r\n\r\nContact: 2884 0788\r\n','2025-05-02 16:39:49',0,NULL),(15,'糖主AZUCAR','N21-G014','N21-G014','ASIAN','Tangzhu provides Chinese, Japanese, Taiwanese, Vietnamese and American casual cuisine for guests to choose from.\r\n\r\nContact: 2892 0567','2025-05-02 16:41:45',0,NULL),(16,'萬豪軒','N1-G006','N1-G006','CANTONESE','\"Man Hou Hin\" is a traditional Cantonese restaurant in Macau with a history of more than 30 years. \"Man Hou Hin\" Macao will integrate modern Cantonese cuisine with tea culture to create a light luxury Cantonese Chinese restaurant. Signature dishes include signature lemon shrimp, first love sweet and sour pork and Kung Fu soup shrimp dumplings, as well as a variety of modern Cantonese dishes, exquisite dim sum and Chinese tea drinks.\r\n\r\nPlease note that 15:00-17:30 will be closed for Monday-Sunday!!!\r\n\r\nContact: 6238 8206','2025-05-02 16:45:29',0,NULL);
/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant_claim`
--

DROP TABLE IF EXISTS `restaurant_claim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant_claim` (
  `claim_id` int NOT NULL AUTO_INCREMENT,
  `restaurant_id` int NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `proof_document` varchar(255) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `processed_at` datetime DEFAULT NULL,
  `processed_by` varchar(50) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`claim_id`),
  KEY `restaurant_id` (`restaurant_id`),
  KEY `user_id` (`user_id`),
  KEY `processed_by` (`processed_by`),
  CONSTRAINT `restaurant_claim_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`),
  CONSTRAINT `restaurant_claim_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `restaurant_claim_ibfk_3` FOREIGN KEY (`processed_by`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant_claim`
--

LOCK TABLES `restaurant_claim` WRITE;
/*!40000 ALTER TABLE `restaurant_claim` DISABLE KEYS */;
INSERT INTO `restaurant_claim` VALUES (1,1,'ddc5f0cddef0842fbb8ac7fa577b8ea5','documents/claims/a6844371682c49f586ae371c20aa6e8b_cis3018HW1.pdf','approved','2025-05-03 10:21:58','2025-05-03 10:23:54','4b045935ef243920679945e1b0f9bb6b','');
/*!40000 ALTER TABLE `restaurant_claim` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant_followers`
--

DROP TABLE IF EXISTS `restaurant_followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant_followers` (
  `user_id` varchar(50) NOT NULL,
  `restaurant_id` int NOT NULL,
  `followed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`restaurant_id`),
  KEY `restaurant_id` (`restaurant_id`),
  CONSTRAINT `restaurant_followers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `restaurant_followers_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant_followers`
--

LOCK TABLES `restaurant_followers` WRITE;
/*!40000 ALTER TABLE `restaurant_followers` DISABLE KEYS */;
/*!40000 ALTER TABLE `restaurant_followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant_photo`
--

DROP TABLE IF EXISTS `restaurant_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant_photo` (
  `photo_id` int NOT NULL AUTO_INCREMENT,
  `restaurant_id` int NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `uploaded_by` varchar(50) NOT NULL,
  `is_approved` tinyint(1) DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  PRIMARY KEY (`photo_id`),
  KEY `restaurant_id` (`restaurant_id`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `restaurant_photo_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`),
  CONSTRAINT `restaurant_photo_ibfk_2` FOREIGN KEY (`uploaded_by`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant_photo`
--

LOCK TABLES `restaurant_photo` WRITE;
/*!40000 ALTER TABLE `restaurant_photo` DISABLE KEYS */;
INSERT INTO `restaurant_photo` VALUES (1,1,'restaurants/ee5421b1a0f944b88111e23a456f34a7_image001.png','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 15:42:32'),(2,1,'restaurants/232f91a18abd4fb98e4e75125bfaeafe_image003.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 15:42:32'),(3,1,'restaurants/9fe4fd97b0694c0ba7be8c0d310f562e_image005.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 15:42:32'),(4,2,'restaurants/b8c7893bcf2e45e9976dba582542e55f_image007.png','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 15:46:50'),(5,2,'restaurants/2d7365f884bf4e25a471c32d878dda8b_image008.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 15:46:50'),(6,2,'restaurants/87e746e191d1402ea51a4b9f46eb3cf6_image010.png','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 15:46:50'),(7,3,'restaurants/49e05468cad74b9e920ce0a245b5e0f9_sgw.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:17:09'),(8,4,'restaurants/741013ca3d534e8999e43757df8774e6_sbw.png','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:23:35'),(9,5,'restaurants/83575697f4894aa2a2cc646bc9206206_xjg.png','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:26:44'),(10,6,'restaurants/bded5343eb8b40ffb8cc46769d173ccd_kz.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:28:03'),(11,7,'restaurants/3d5a516544184b55a5f5044020149225_byy.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:29:58'),(12,8,'restaurants/34c515d9373646fe85678da7d1d72c3c_gdsdms.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:31:30'),(13,9,'restaurants/c53dd2141cfc499c8b55f8e77c61258d_yjyj.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:33:03'),(14,10,'restaurants/c967297c36f54361bde9a0944ba10829_csh.png','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:34:28'),(15,12,'restaurants/4085c81050214729b33b7affdc47cbf1_jfms.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:36:57'),(16,13,'restaurants/01692070e60548de9689c36dad241ce0_lzlmg.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:38:13'),(17,14,'restaurants/05467a14216244e386c4c1bc1267afca_mdl.png','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:39:49'),(18,15,'restaurants/ff634ad50a0b48d5aa7602e230b22be6_tz.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:41:45'),(19,16,'restaurants/3ec2bb340a2d41c58cbea1043806c89a_whx.png','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:48:16'),(20,11,'restaurants/c7bcf4e745ee467d87e4b1e2c30fa950_wjcwm.jpg','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-02 16:51:51'),(21,6,'restaurants/d2280eb889034d74b32b5501a3c30599_s8-chopsticks.png','4b045935ef243920679945e1b0f9bb6b',1,'2025-05-03 13:05:28');
/*!40000 ALTER TABLE `restaurant_photo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `restaurant_id` int NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `rating` int NOT NULL,
  `comment` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  KEY `restaurant_id` (`restaurant_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`),
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,1,'4b045935ef243920679945e1b0f9bb6b',5,'I love this one. Not cheap but excellent quality!','2025-05-02 15:43:32',NULL),(2,5,'4b045935ef243920679945e1b0f9bb6b',4,'Good environment, delicious food!!!','2025-05-02 16:52:52',NULL),(3,15,'4b045935ef243920679945e1b0f9bb6b',5,'Very delicios','2025-05-02 17:03:35',NULL),(4,3,'4b045935ef243920679945e1b0f9bb6b',3,'Okay. Can be cheaper','2025-05-03 12:52:50',NULL),(5,3,'87a088fa061644d244639d970734e8dc',4,'Not bad, but I think it can be better in their food.','2025-05-03 12:56:45',NULL),(6,2,'6308839e2acc77a8f0d30011f6459d36',5,'🍤 Shrimp Fried Rice with Fried Egg Savory fried rice with tender shrimp, topped with a perfectly cooked fried egg—rich, flavorful, and utterly satisfying!🥦 Steamed Mixed Vegetables A healthy side dish featuring fresh broccoli, cauliflower, and mushrooms, lightly steamed to preserve crunch and nutrition!🍋 Lemon Tea Refreshing lemon tea with a delicate balance of sweetness and tanginess—perfect for cleansing the palate!!!','2025-05-03 13:06:04',NULL),(7,2,'6308839e2acc77a8f0d30011f6459d36',5,'This vibrant seafood paella is a feast for the senses! The rice, infused with a rich tomato-based sauce, absorbs all the delicious flavors of the seafood. Plump shrimp, succulent mussels, tender squid, and fresh clams sit beautifully atop the dish, offering a wonderful variety of textures. The addition of black olives and diced bell peppers adds a pop of color and a slight tangy contrast. Each bite is packed with savory goodness, making this dish a must-try for seafood lovers!👍','2025-05-03 13:17:11',NULL),(8,5,'6308839e2acc77a8f0d30011f6459d36',3,'A comforting dish featuring perfectly cooked spaghetti, generously coated in a rich, savory brown sauce. The tender piece of meat, drenched in the same flavorful sauce, adds depth to each bite, offering a delightful contrast to the smooth pasta. But the pasta felt a little too dry. Hopefully it will be better next time.','2025-05-03 13:20:50','2025-05-03 13:21:43'),(9,2,'6308839e2acc77a8f0d30011f6459d36',5,'A mouthwatering combination of sizzling steak, tender pork, juicy shrimp, and a fried egg with a perfectly runny yolk—all served on a hot plate for extra flavor. Paired with a portion of spaghetti coated in a light tomato sauce and accompanied by sweet corn and fresh broccoli, this dish delivers a delightful mix of textures and tastes!','2025-05-03 13:23:22',NULL),(10,6,'ddc5f0cddef0842fbb8ac7fa577b8ea5',4,'Mostly Japanese food. Not expensive. Pretty good.','2025-05-03 15:57:51',NULL);
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review_photo`
--

DROP TABLE IF EXISTS `review_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review_photo` (
  `photo_id` int NOT NULL AUTO_INCREMENT,
  `review_id` int NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  PRIMARY KEY (`photo_id`),
  KEY `review_id` (`review_id`),
  CONSTRAINT `review_photo_ibfk_1` FOREIGN KEY (`review_id`) REFERENCES `review` (`review_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review_photo`
--

LOCK TABLES `review_photo` WRITE;
/*!40000 ALTER TABLE `review_photo` DISABLE KEYS */;
INSERT INTO `review_photo` VALUES (1,6,'reviews/dae6fd45c457426d8f6df39521a2380b_jpg','2025-05-03 13:06:04'),(2,7,'reviews/6a9217240c2a42e19aefa59bb5ad810a_2.jpg','2025-05-03 13:17:11'),(3,8,'reviews/b116299c58fa4197983dfc1bee200f87_jpg','2025-05-03 13:20:50'),(4,9,'reviews/3044354be1af4cee9ebc25ad3d88d16f_1.jpg','2025-05-03 13:23:22');
/*!40000 ALTER TABLE `review_photo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('GENERAL_USER','RESTAURANT_MANAGER','ADMIN') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_email_verified` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('0ea8269fdf19b8c9d9e7677a4765e02a','VatKamHou','cnmrockstars@gmail.com','scrypt:32768:8:1$Ji2BUt29rAJ5bN4m$4e93af7de8e150b9f74e0c14092c64618f7d2e4d1b0d79fa457b15fe80993e80641aa056b651fdf696aeedfa21a3945d2d2772b278ee9243b3f84a4159345260','GENERAL_USER','2025-05-02 17:09:11',NULL,0),('2475ea30e50e02c2156c1e13393ad8db','Sam','3@lric.xyz','scrypt:32768:8:1$chDZyNNV5XMaPiHU$d4bcb3fd4ae0b5e5d26e72435ed4514e6f42e0640852729a19917bbe2dc76e2b5b5ddea77c074fa4fa90db4f140511908301268f6223fcb99700c3fcab63e4dc','GENERAL_USER','2025-05-02 15:23:53','2025-05-03 13:11:16',1),('451c0150aa3a5f5c9c65a7fe6a438d4a','eric10y','1@lric.xyz','scrypt:32768:8:1$Uhrg0PuAb8U0eT4o$bcb0384407f7366d28c7d1a66a95bbfb2db121eef4fe0a544ccb5ce76b600fb349d1635daf160f57124a533779fd1f1d021061aba8df89290c822deefcea7e99','GENERAL_USER','2025-05-02 14:45:11',NULL,0),('4b045935ef243920679945e1b0f9bb6b','Admin','what2eatatum@gmail.com','scrypt:32768:8:1$3GfqNAsXQJpCFzaz$15e2ceddf3a1416cfd414c57b599256793b9fe7d4e2d799ab24379d7c086d86e7d6ba86a2d0d9039723725baaf7c271ec3b7937fe9f36673c85b162c9d992758','ADMIN','2025-05-02 14:42:37','2025-05-03 13:10:37',1),('6308839e2acc77a8f0d30011f6459d36','Popping','5@lric.xyz','scrypt:32768:8:1$cO58yrjBsg5MiWeC$76817be47f77ab14e8405a1f88b1112bc967dfaa414a6b7f08958c8462ace192bd3f0be3d2391734810250b966084d915dcafb561b152298101482429ec59033','GENERAL_USER','2025-05-02 15:26:11','2025-05-03 12:54:36',1),('87a088fa061644d244639d970734e8dc','Angus','4@lric.xyz','scrypt:32768:8:1$jZeZujR1uZeckXoF$0d96894ece85fa5240540747ae626cb9906828e38b630d44e0f8304da2636a4e8935a5a901e39064dd184b6687d08a6915432d4f375590fbc13e627429fe9f6f','GENERAL_USER','2025-05-02 15:23:53','2025-05-03 12:55:26',1),('ddc5f0cddef0842fbb8ac7fa577b8ea5','Eric','2@lric.xyz','scrypt:32768:8:1$Br8vSn5KxTBdtPZU$c1ad0998bdd64834f49a9ac09462c3403606c71290f0c06d44ad6a7c2299124315cc6fa1bb38f4239d967d46f182246873a3f005d32df9f54f0284953882cb3e','RESTAURANT_MANAGER','2025-05-02 15:23:52','2025-05-03 15:57:07',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-07 10:44:09
