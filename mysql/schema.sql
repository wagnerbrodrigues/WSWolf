CREATE TABLE `info_acoes` (
	`data_coleta` datetime NOT NULL,
  `acao` char(6) NOT NULL,
  `valor_atual` double NOT NULL,
  `volume_diario` double NOT NULL,
  `dy` double NOT NULL,
  `pl` double NOT NULL,
  `setor` varchar(45) NOT NULL,
  `pvp` double NOT NULL,
  `vpa` double NOT NULL,
  `roe` double NOT NULL,
  `lpa` double NOT NULL,
  `pebit` double NOT NULL,
  `valor_intrinseco` double DEFAULT NULL,
  `bazin12` double DEFAULT NULL,
  `bazin36` double DEFAULT NULL,
  `bazin60` double DEFAULT NULL,
  `score` int DEFAULT NULL,
  PRIMARY KEY (`acao`, `data_coleta`)
)

CREATE TABLE `dividendos` (
  `acao` char(6) NOT NULL,
  `data_comunicado` datetime NOT NULL,
  `data_pagamento` datetime NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `valor` double NOT NULL,
  `dividendoscol` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


