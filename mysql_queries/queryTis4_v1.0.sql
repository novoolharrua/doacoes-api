CREATE TABLE `tb_atendimentos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_visita` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id_regiao` int(11) NOT NULL,
  `tipo_doacao` int(11) NOT NULL,
  `num_atendidos` int(11) NOT NULL,
  `id_recebedor` int(11) NOT NULL,
  `id_fornecedor` int(11) NOT NULL,
  `periodo` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tb_atendimentos_tb_regiao1_idx` (`id_regiao`),
  KEY `fk_tb_atendimentos_tb_grupo_recebedores1_idx` (`id_recebedor`),
  KEY `fk_tb_atendimentos_tb_fornecedores1_idx` (`id_fornecedor`),
  KEY `tb_atendimentos_tb_tipo_doacao_fk` (`tipo_doacao`),
  CONSTRAINT `fk_tb_atendimentos_tb_fornecedores1` FOREIGN KEY (`id_fornecedor`) REFERENCES `tb_fornecedores` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_atendimentos_tb_grupo_recebedores1` FOREIGN KEY (`id_recebedor`) REFERENCES `tb_grupo_recebedores` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_atendimentos_tb_regiao1` FOREIGN KEY (`id_regiao`) REFERENCES `tb_regioes` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `tb_atendimentos_tb_tipo_doacao_fk` FOREIGN KEY (`tipo_doacao`) REFERENCES `tb_tipo_doacao` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tb_fornecedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_representante` int(11) NOT NULL,
  `num_pessoas` int(11) NOT NULL,
  `cp_atendimento_pessoas` int(11) DEFAULT NULL,
  `id_tipo_doacao` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tb_fornecedores_representante1_idx` (`id_representante`),
  KEY `tb_fornecedores_tb_tipo_doacao_fk` (`id_tipo_doacao`),
  CONSTRAINT `fk_tb_fornecedores_representante1` FOREIGN KEY (`id_representante`) REFERENCES `tb_representante` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `tb_fornecedores_tb_tipo_doacao_fk` FOREIGN KEY (`id_tipo_doacao`) REFERENCES `tb_tipo_doacao` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tb_grupo_recebedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_regiao` int(11) DEFAULT NULL,
  `numero_pessoas` int(11) NOT NULL,
  `ultimo_atendimento` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `descricao` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tb_grupo_recebedores_tb_regiao_idx` (`id_regiao`),
  CONSTRAINT `fk_tb_grupo_recebedores_tb_regiao` FOREIGN KEY (`id_regiao`) REFERENCES `tb_regioes` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tb_infos_uteis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `telefone` varchar(20) DEFAULT NULL,
  `endereco` varchar(200) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `descricao` varchar(200) DEFAULT NULL,
  `site` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tb_regioes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  `ponto_A` varchar(200) NOT NULL,
  `ponto_B` varchar(200) NOT NULL,
  `ponto_C` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE `tb_representante` (
  `id` int(11) NOT NULL,
  `nome` varchar(45) NOT NULL,
  `cpf_cnpj` varchar(29) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `empresa` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tb_tipo_doacao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_doacao` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


