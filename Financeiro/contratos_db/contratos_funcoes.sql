DELIMITER $$

-- -----------------------------------------------------
-- função para adicionar um contrato
-- -----------------------------------------------------
CREATE PROCEDURE adicionarContrato(
    IN cliente_id INT UNSIGNED,
    IN tipo VARCHAR(50),
    IN valor DECIMAL(10, 2),
    IN data_inicio DATE,
    IN data_fim DATE,
    IN status VARCHAR(20)
)
BEGIN
    -- verifica se o cliente existe
    IF (SELECT COUNT(*) FROM usersdb.Usuarios WHERE user_id = cliente_id) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cliente não encontrado';
    END IF;

    -- insere o contrato na tabela Contratos
    INSERT INTO usersdb.Contratos (cliente_id, tipo, valor, data_inicio, data_fim, status)
    VALUES (cliente_id, tipo, valor, data_inicio, data_fim, status);
END$$


-- -----------------------------------------------------
-- função para atualizar um contrato
-- -----------------------------------------------------
CREATE PROCEDURE atualizarContrato(
    IN contrato_id INT UNSIGNED,
    IN novo_tipo VARCHAR(50),
    IN novo_valor DECIMAL(10, 2),
    IN nova_data_inicio DATE,
    IN nova_data_fim DATE,
    IN novo_status VARCHAR(20)
)
BEGIN
    -- verifica se o contrato existe
    IF (SELECT COUNT(*) FROM usersdb.Contratos WHERE contrato_id = contrato_id) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Contrato não encontrado';
    END IF;

    -- atualiza os dados do contrato
    UPDATE usersdb.Contratos
    SET tipo = novo_tipo,
        valor = novo_valor,
        data_inicio = nova_data_inicio,
        data_fim = nova_data_fim,
        status = novo_status
    WHERE contrato_id = contrato_id;
END$$


-- -----------------------------------------------------
-- função para deletar um contrato
-- -----------------------------------------------------
CREATE PROCEDURE deletarContrato(
    IN contrato_id INT UNSIGNED
)
BEGIN
    -- Verifica se o contrato existe
    IF (SELECT COUNT(*) FROM usersdb.Contratos WHERE contrato_id = contrato_id) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Contrato não encontrado';
    END IF;

    -- Remove o contrato
    DELETE FROM usersdb.Contratos WHERE contrato_id = contrato_id;
END$$

DELIMITER ;
