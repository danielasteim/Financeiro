-- -----------------------------------------------------
-- Table `usersdb`.`Contratos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `usersdb`.`Contratos` (
  `contrato_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `cliente_id` INT UNSIGNED NOT NULL,
  `tipo` VARCHAR(50) NOT NULL, -- mensal, trimestral, anual
  `valor` DECIMAL(10,2) NOT NULL,
  `data_inicio` DATE NOT NULL,
  `data_fim` DATE NOT NULL,
  `status` VARCHAR(20) NOT NULL, -- ativo, inativo
  PRIMARY KEY (`contrato_id`),
  CONSTRAINT `fk_Contratos_Usuarios`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `usersdb`.`Usuarios` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;

-- histórias de exemplo
INSERT INTO `usersdb`.`Contratos` (`cliente_id`, `tipo`, `valor`, `data_inicio`, `data_fim`, `status`) VALUES
(1, 'mensal', 100.00, '2024-12-01', '2024-12-31', 'Ativo'),
(2, 'anual', 1000.00, '2024-01-01', '2024-12-31', 'Ativo');
