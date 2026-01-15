-- ----------------------------------------------------------
-- Script POSTGRESQL pour Budget App
-- Schema mis à jour avec CATEGORIE/SOUS_CATEGORIE séparées
-- ----------------------------------------------------------


-- ----------------------------
-- Table: COMPTE
-- ----------------------------
CREATE TABLE COMPTE (
  idCompte INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nom TEXT NOT NULL,
  solde NUMERIC(10,2) NOT NULL,
  type VARCHAR(50) NOT NULL,
  CONSTRAINT COMPTE_PK PRIMARY KEY (idCompte)
);


-- ----------------------------
-- Table: CATEGORIE
-- ----------------------------
CREATE TABLE CATEGORIE (
  nomCategorie VARCHAR(50) NOT NULL,
  CONSTRAINT CATEGORIE_PK PRIMARY KEY (nomCategorie)
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
  nomSousCategorie VARCHAR(50) NOT NULL,
  nomCategorie VARCHAR(50) NOT NULL,
  CONSTRAINT SOUS_CATEGORIE_PK PRIMARY KEY (nomSousCategorie),
  CONSTRAINT SOUS_CATEGORIE_nomCategorie_FK FOREIGN KEY (nomCategorie) REFERENCES CATEGORIE (nomCategorie)
);


-- ----------------------------
-- Table: OPERATION
-- ----------------------------
CREATE TABLE OPERATION (
  idTransaction INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  date DATE NOT NULL,
  description TEXT NOT NULL,
  montant NUMERIC(10,2) NOT NULL,
  idCompte INTEGER NOT NULL,
  idType INTEGER NOT NULL,
  nomSousCategorie VARCHAR(50),
  CONSTRAINT OPERATION_PK PRIMARY KEY (idTransaction),
  CONSTRAINT OPERATION_idCompte_FK FOREIGN KEY (idCompte) REFERENCES COMPTE (idCompte),
  CONSTRAINT OPERATION_idType_FK FOREIGN KEY (idType) REFERENCES TYPE (idType),
  CONSTRAINT OPERATION_nomSousCategorie_FK FOREIGN KEY (nomSousCategorie) REFERENCES SOUS_CATEGORIE (nomSousCategorie)
);


-- ----------------------------
-- Insertion des types par défaut
-- ----------------------------
INSERT INTO TYPE (nom) VALUES
  ('depense'),
  ('revenu'),
  ('transfert')
ON CONFLICT (nom) DO NOTHING;


-- ----------------------------
-- Catégories par défaut
-- ----------------------------
INSERT INTO CATEGORIE (nomCategorie) VALUES
  ('Alimentation'),
  ('Transport'),
  ('Logement'),
  ('Loisirs'),
  ('Santé'),
  ('Revenus'),
  ('Shopping'),
  ('Factures')
ON CONFLICT DO NOTHING;


-- ----------------------------
-- Sous-catégories par défaut
-- ----------------------------
INSERT INTO SOUS_CATEGORIE (nomSousCategorie, nomCategorie) VALUES
  ('Courses', 'Alimentation'),
  ('Restaurant', 'Alimentation'),
  ('Essence', 'Transport'),
  ('Transports publics', 'Transport'),
  ('Salaire', 'Revenus'),
  ('Prime', 'Revenus'),
  ('Vêtements', 'Shopping')
ON CONFLICT DO NOTHING;
