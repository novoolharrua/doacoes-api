-- -----------------------------------------------------
-- Table `mydb`.`region`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donations`.`region` ;

CREATE TABLE IF NOT EXISTS `donations`.`region` (
  `ID_REGION` INT NOT NULL AUTO_INCREMENT,
  `ADDRESS` VARCHAR(255) NOT NULL,
  `NAME` VARCHAR(255) NOT NULL,
  `CREATED_AT` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (`ID_REGION`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`calendar`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donations`.`calendar` ;

CREATE TABLE IF NOT EXISTS `donations`.`calendar` (
  `ID_CALENDAR` INT NOT NULL AUTO_INCREMENT,
  `TYPE` VARCHAR(45) NOT NULL,
  `GCLOUD_ID` VARCHAR(255) NOT NULL,
  `ID_REGION` INT NOT NULL,
  `CREATED_AT` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (`ID_CALENDAR`),
  INDEX `fk_calendar_region_idx` (`ID_REGION` ASC),
  CONSTRAINT `fk_calendar_region`
    FOREIGN KEY (`ID_REGION`)
    REFERENCES `donations`.`region` (`ID_REGION`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;