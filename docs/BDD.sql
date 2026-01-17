-- ----------------------------------------------------------
-- Script POSTGRESQL pour Budget App
-- ----------------------------------------------------------

-- ----------------------------
-- Table: COMPTE
-- ----------------------------
CREATE TABLE COMPTE (
  idCompte INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nom TEXT NOT NULL,
  solde NUMERIC(10,2) NOT NULL DEFAULT 0,                    -- [1]
  type VARCHAR(50) NOT NULL,
  CONSTRAINT COMPTE_PK PRIMARY KEY (idCompte),
  CONSTRAINT nom_compte_UNQ UNIQUE (nom)                     -- [2]
);

-- ----------------------------
-- Table: CATEGORIE
-- ----------------------------
CREATE TABLE CATEGORIE (
  idCategorie INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nomCategorie VARCHAR(50) NOT NULL,
  CONSTRAINT CATEGORIE_PK PRIMARY KEY (idCategorie),
  CONSTRAINT nomCategorie_UNQ UNIQUE (nomCategorie)
);

-- ----------------------------
-- Table: TYPE
-- ----------------------------
CREATE TABLE TYPE (
  idType INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nom VARCHAR(50) NOT NULL,
  CONSTRAINT TYPE_PK PRIMARY KEY (idType),
  CONSTRAINT nom_UNQ UNIQUE (nom)
);

-- ----------------------------
-- Table: SOUS_CATEGORIE
-- ----------------------------
CREATE TABLE SOUS_CATEGORIE (
  idSousCategorie INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nomSousCategorie VARCHAR(50) NOT NULL,
  idCategorie INTEGER NOT NULL,
  CONSTRAINT SOUS_CATEGORIE_PK PRIMARY KEY (idSousCategorie),
  CONSTRAINT sous_cat_unique UNIQUE (nomSousCategorie, idCategorie),  -- [3]
  CONSTRAINT SOUS_CATEGORIE_idCategorie_FK FOREIGN KEY (idCategorie)
    REFERENCES CATEGORIE (idCategorie) ON DELETE CASCADE              -- [4]
);

-- ----------------------------
-- Table: OPERATION
-- ----------------------------
CREATE TABLE OPERATION (
  idOperation INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  date DATE NOT NULL DEFAULT CURRENT_DATE,                            -- [5]
  description TEXT NOT NULL,
  montant NUMERIC(10,2) NOT NULL,
  idCompte INTEGER NOT NULL,                                          -- [6]
  idType INTEGER NOT NULL,
  idSousCategorie INTEGER,
  CONSTRAINT OPERATION_PK PRIMARY KEY (idOperation),
  CONSTRAINT OPERATION_idCompte_FK FOREIGN KEY (idCompte)
    REFERENCES COMPTE (idCompte) ON DELETE RESTRICT,                  -- [7]
  CONSTRAINT OPERATION_idType_FK FOREIGN KEY (idType)
    REFERENCES TYPE (idType) ON DELETE RESTRICT,                      -- [8]
  CONSTRAINT OPERATION_idSousCategorie_FK FOREIGN KEY (idSousCategorie)
    REFERENCES SOUS_CATEGORIE (idSousCategorie) ON DELETE SET NULL    -- [9]
);

-- ----------------------------
-- Index pour performance
-- ----------------------------
CREATE INDEX idx_operation_date ON OPERATION (date);                  -- [10]
CREATE INDEX idx_operation_compte ON OPERATION (idCompte);            -- [11]
