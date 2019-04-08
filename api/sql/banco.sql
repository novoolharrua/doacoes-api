-- MySQL Script generated by MySQL Workbench
-- Dom 07 Abr 2019 18:40:39 -03
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`region`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`region` ;

CREATE TABLE IF NOT EXISTS `mydb`.`region` (
  `ID_REGION` INT NOT NULL AUTO_INCREMENT,
  `ADDRESS` VARCHAR(255) NOT NULL,
  `NAME` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`ID_REGION`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`calendar`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`calendar` ;

CREATE TABLE IF NOT EXISTS `mydb`.`calendar` (
  `ID_CALENDAR` INT NOT NULL AUTO_INCREMENT,
  `TYPE` VARCHAR(45) NOT NULL,
  `region_ID_REGION` INT NOT NULL,
  PRIMARY KEY (`ID_CALENDAR`),
  INDEX `fk_calendar_region_idx` (`region_ID_REGION` ASC),
  CONSTRAINT `fk_calendar_region`
    FOREIGN KEY (`region_ID_REGION`)
    REFERENCES `mydb`.`region` (`ID_REGION`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`user` ;

CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `username` (16) NOT NULL,
  `email` (255) NULL,
  `password` (32) NOT NULL,
  `create_time`  NULL DEFAULT CURRENT_TIMESTAMP,
  `ID_USER` BIGINT(255) NOT NULL,
  PRIMARY KEY (`ID_USER`));


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;