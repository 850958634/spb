/*
SQLyog Professional v12.09 (64 bit)
MySQL - 5.7.40-log : Database - spb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`spb` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `spb`;

/*Table structure for table `customer` */

DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(25) DEFAULT NULL,
  `family_name` varchar(25) NOT NULL,
  `email` varchar(320) NOT NULL,
  `phone` varchar(11) NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

/*Data for the table `customer` */

insert  into `customer`(`customer_id`,`first_name`,`family_name`,`email`,`phone`) values (1,'Shannon','Willis','shannon@willis.nz','0211661231'),(2,'Simon','Chambers','simonchambers@gmail.com','033245678'),(3,'Charles','Carmichael','carmichaels@hotmail.com','02754365286'),(4,'Zhe','Wang','zhe.wang@qq.com','0743277893'),(5,'Qi','Qi','qi@qi.co.nz','0294458423'),(6,NULL,'Govindjee','hello@govindjee.nz','034156784'),(7,'liu','hui','443487999@qq.com','15653242829'),(8,'dscsad','dsacds','dcsavds','vdvda'),(9,'gbdb','bfdbf','bf','bfdb'),(10,'aaa','aaa','aaa','aaa');

/*Table structure for table `job` */

DROP TABLE IF EXISTS `job`;

CREATE TABLE `job` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `job_date` date NOT NULL,
  `customer` int(11) NOT NULL,
  `total_cost` decimal(6,2) DEFAULT NULL,
  `completed` tinyint(4) DEFAULT '0',
  `paid` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`job_id`),
  KEY `customer` (`customer`),
  CONSTRAINT `job_ibfk_1` FOREIGN KEY (`customer`) REFERENCES `customer` (`customer_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;

/*Data for the table `job` */

insert  into `job`(`job_id`,`job_date`,`customer`,`total_cost`,`completed`,`paid`) values (1,'2023-11-01',4,'410.22',1,1),(2,'2024-02-02',6,'3409.66',1,1),(3,'2023-12-11',1,NULL,1,0),(4,'2023-12-12',2,NULL,0,0),(5,'2023-12-12',5,NULL,0,0),(6,'2024-01-03',1,NULL,0,0),(7,'2024-01-18',6,NULL,0,0),(8,'2024-01-19',1,NULL,0,0),(9,'2024-01-26',1,NULL,0,0),(10,'2024-01-19',1,NULL,0,0),(11,'2024-01-19',6,NULL,0,0);

/*Table structure for table `job_part` */

DROP TABLE IF EXISTS `job_part`;

CREATE TABLE `job_part` (
  `job_id` int(11) NOT NULL,
  `part_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`job_id`,`part_id`),
  KEY `part_id` (`part_id`),
  CONSTRAINT `job_part_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `job` (`job_id`) ON UPDATE CASCADE,
  CONSTRAINT `job_part_ibfk_2` FOREIGN KEY (`part_id`) REFERENCES `part` (`part_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `job_part` */

insert  into `job_part`(`job_id`,`part_id`,`qty`) values (1,2,3),(1,4,1),(2,1,1),(2,2,0),(2,3,0),(2,4,0),(2,5,5),(2,6,0),(2,7,0),(2,8,0),(2,9,0),(2,10,0);

/*Table structure for table `job_service` */

DROP TABLE IF EXISTS `job_service`;

CREATE TABLE `job_service` (
  `job_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`job_id`,`service_id`),
  KEY `service_id` (`service_id`),
  CONSTRAINT `job_service_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `job` (`job_id`) ON UPDATE CASCADE,
  CONSTRAINT `job_service_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `job_service` */

insert  into `job_service`(`job_id`,`service_id`,`qty`) values (1,2,3),(1,5,1),(2,1,1),(2,2,0),(2,3,0),(2,4,0),(2,5,0),(2,6,0),(2,7,0),(2,8,5),(2,9,0),(2,10,0),(2,11,0);

/*Table structure for table `part` */

DROP TABLE IF EXISTS `part`;

CREATE TABLE `part` (
  `part_id` int(11) NOT NULL AUTO_INCREMENT,
  `part_name` varchar(25) NOT NULL,
  `cost` decimal(5,2) NOT NULL,
  PRIMARY KEY (`part_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;

/*Data for the table `part` */

insert  into `part`(`part_id`,`part_name`,`cost`) values (1,'Windscreen','560.65'),(2,'Headlight','35.65'),(3,'Wiper blade','12.43'),(4,'Left fender','260.76'),(5,'Right fender','260.76'),(6,'Tail light','120.54'),(7,'Hub Cap','22.89'),(8,'aaa','22.14'),(9,'bbb','111.00'),(10,'ccc','111.11'),(11,'aa','11.00');

/*Table structure for table `service` */

DROP TABLE IF EXISTS `service`;

CREATE TABLE `service` (
  `service_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(25) NOT NULL,
  `cost` decimal(5,2) NOT NULL,
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

/*Data for the table `service` */

insert  into `service`(`service_id`,`service_name`,`cost`) values (1,'Sandblast','300.21'),(2,'Minor Fill','43.21'),(3,'Major Fill','125.70'),(4,'Respray','800.33'),(5,'Touch up','34.99'),(6,'Polish','250.00'),(7,'Small Dent Removal','49.99'),(8,'Large Dent Removal','249.00'),(9,'yitiaolong','998.00'),(10,'aaaaa','99.00'),(11,'asddasd','89.56'),(12,'aaa','11.00');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
