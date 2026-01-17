-- ----------------------------------------------------------
-- Script POSTGRESQL pour Budget App (avec RLS)
-- ----------------------------------------------------------

-- ----------------------------
-- Table: UTILISATEUR
-- ----------------------------
CREATE TABLE UTILISATEUR (
  idUtilisateur INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  email VARCHAR(255) NOT NULL,
  mot_de_passe_hash VARCHAR(255) NOT NULL,
  nom_affichage VARCHAR(100),
  date_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  derniere_connexion TIMESTAMP,
  actif BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT UTILISATEUR_PK PRIMARY KEY (idUtilisateur),
  CONSTRAINT email_UNQ UNIQUE (email)
);

-- ----------------------------
-- Table: COMPTE
-- ----------------------------
CREATE TABLE COMPTE (
  idCompte INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nom TEXT NOT NULL,
  solde NUMERIC(10,2) NOT NULL DEFAULT 0,
  type VARCHAR(50) NOT NULL,
  idUtilisateur INTEGER NOT NULL,
  CONSTRAINT COMPTE_PK PRIMARY KEY (idCompte),
  CONSTRAINT nom_compte_par_user_UNQ UNIQUE (nom, idUtilisateur),
  CONSTRAINT COMPTE_idUtilisateur_FK FOREIGN KEY (idUtilisateur)
    REFERENCES UTILISATEUR (idUtilisateur) ON DELETE CASCADE
);

-- ----------------------------
-- Table: CATEGORIE
-- ----------------------------
CREATE TABLE CATEGORIE (
  idCategorie INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nomCategorie VARCHAR(50) NOT NULL,
  idUtilisateur INTEGER NOT NULL,
  CONSTRAINT CATEGORIE_PK PRIMARY KEY (idCategorie),
  CONSTRAINT nomCategorie_par_user_UNQ UNIQUE (nomCategorie, idUtilisateur),
  CONSTRAINT CATEGORIE_idUtilisateur_FK FOREIGN KEY (idUtilisateur)
    REFERENCES UTILISATEUR (idUtilisateur) ON DELETE CASCADE
);

-- ----------------------------
-- Table: TYPE
-- ----------------------------
CREATE TABLE TYPE (
  idType INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nom VARCHAR(50) NOT NULL,
  idUtilisateur INTEGER NOT NULL,
  CONSTRAINT TYPE_PK PRIMARY KEY (idType),
  CONSTRAINT nom_type_par_user_UNQ UNIQUE (nom, idUtilisateur),
  CONSTRAINT TYPE_idUtilisateur_FK FOREIGN KEY (idUtilisateur)
    REFERENCES UTILISATEUR (idUtilisateur) ON DELETE CASCADE
);

-- ----------------------------
-- Table: SOUS_CATEGORIE
-- ----------------------------
CREATE TABLE SOUS_CATEGORIE (
  idSousCategorie INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nomSousCategorie VARCHAR(50) NOT NULL,
  idCategorie INTEGER NOT NULL,
  CONSTRAINT SOUS_CATEGORIE_PK PRIMARY KEY (idSousCategorie),
  CONSTRAINT sous_cat_unique UNIQUE (nomSousCategorie, idCategorie),
  CONSTRAINT SOUS_CATEGORIE_idCategorie_FK FOREIGN KEY (idCategorie)
    REFERENCES CATEGORIE (idCategorie) ON DELETE CASCADE
);

-- ----------------------------
-- Table: OPERATION
-- ----------------------------
CREATE TABLE OPERATION (
  idOperation INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  description TEXT NOT NULL,
  montant NUMERIC(10,2) NOT NULL,
  idCompte INTEGER NOT NULL,
  idType INTEGER NOT NULL,
  idSousCategorie INTEGER,
  CONSTRAINT OPERATION_PK PRIMARY KEY (idOperation),
  CONSTRAINT OPERATION_idCompte_FK FOREIGN KEY (idCompte)
    REFERENCES COMPTE (idCompte) ON DELETE RESTRICT,
  CONSTRAINT OPERATION_idType_FK FOREIGN KEY (idType)
    REFERENCES TYPE (idType) ON DELETE RESTRICT,
  CONSTRAINT OPERATION_idSousCategorie_FK FOREIGN KEY (idSousCategorie)
    REFERENCES SOUS_CATEGORIE (idSousCategorie) ON DELETE SET NULL
);

-- ----------------------------
-- Index de performance
-- ----------------------------
CREATE INDEX idx_compte_utilisateur ON COMPTE (idUtilisateur);
CREATE INDEX idx_categorie_utilisateur ON CATEGORIE (idUtilisateur);
CREATE INDEX idx_type_utilisateur ON TYPE (idUtilisateur);
CREATE INDEX idx_operation_date ON OPERATION (date);
CREATE INDEX idx_operation_compte ON OPERATION (idCompte);

-- ===========================================================
-- ROW LEVEL SECURITY (RLS)
-- ===========================================================

-- Activer RLS sur les tables
ALTER TABLE COMPTE ENABLE ROW LEVEL SECURITY;
ALTER TABLE CATEGORIE ENABLE ROW LEVEL SECURITY;
ALTER TABLE TYPE ENABLE ROW LEVEL SECURITY;
ALTER TABLE SOUS_CATEGORIE ENABLE ROW LEVEL SECURITY;
ALTER TABLE OPERATION ENABLE ROW LEVEL SECURITY;

-- ----------------------------
-- Politiques pour COMPTE
-- ----------------------------
CREATE POLICY compte_select ON COMPTE
  FOR SELECT USING (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

CREATE POLICY compte_insert ON COMPTE
  FOR INSERT WITH CHECK (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

CREATE POLICY compte_update ON COMPTE
  FOR UPDATE USING (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

CREATE POLICY compte_delete ON COMPTE
  FOR DELETE USING (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

-- ----------------------------
-- Politiques pour CATEGORIE
-- ----------------------------
CREATE POLICY categorie_select ON CATEGORIE
  FOR SELECT USING (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

CREATE POLICY categorie_insert ON CATEGORIE
  FOR INSERT WITH CHECK (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

CREATE POLICY categorie_update ON CATEGORIE
  FOR UPDATE USING (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

CREATE POLICY categorie_delete ON CATEGORIE
  FOR DELETE USING (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

-- ----------------------------
-- Politiques pour TYPE
-- ----------------------------
CREATE POLICY type_select ON TYPE
  FOR SELECT USING (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

CREATE POLICY type_insert ON TYPE
  FOR INSERT WITH CHECK (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

CREATE POLICY type_update ON TYPE
  FOR UPDATE USING (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

CREATE POLICY type_delete ON TYPE
  FOR DELETE USING (idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER);

-- ----------------------------
-- Politiques pour SOUS_CATEGORIE (via CATEGORIE)
-- ----------------------------
CREATE POLICY sous_categorie_select ON SOUS_CATEGORIE
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM CATEGORIE c
      WHERE c.idCategorie = SOUS_CATEGORIE.idCategorie
      AND c.idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER
    )
  );

CREATE POLICY sous_categorie_insert ON SOUS_CATEGORIE
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM CATEGORIE c
      WHERE c.idCategorie = SOUS_CATEGORIE.idCategorie
      AND c.idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER
    )
  );

CREATE POLICY sous_categorie_update ON SOUS_CATEGORIE
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM CATEGORIE c
      WHERE c.idCategorie = SOUS_CATEGORIE.idCategorie
      AND c.idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER
    )
  );

CREATE POLICY sous_categorie_delete ON SOUS_CATEGORIE
  FOR DELETE USING (
    EXISTS (
      SELECT 1 FROM CATEGORIE c
      WHERE c.idCategorie = SOUS_CATEGORIE.idCategorie
      AND c.idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER
    )
  );

-- ----------------------------
-- Politiques pour OPERATION (via COMPTE)
-- ----------------------------
CREATE POLICY operation_select ON OPERATION
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM COMPTE c
      WHERE c.idCompte = OPERATION.idCompte
      AND c.idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER
    )
  );

CREATE POLICY operation_insert ON OPERATION
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM COMPTE c
      WHERE c.idCompte = OPERATION.idCompte
      AND c.idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER
    )
  );

CREATE POLICY operation_update ON OPERATION
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM COMPTE c
      WHERE c.idCompte = OPERATION.idCompte
      AND c.idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER
    )
  );

CREATE POLICY operation_delete ON OPERATION
  FOR DELETE USING (
    EXISTS (
      SELECT 1 FROM COMPTE c
      WHERE c.idCompte = OPERATION.idCompte
      AND c.idUtilisateur = current_setting('app.user_id', TRUE)::INTEGER
    )
  );

-- ===========================================================
-- RÔLE APPLICATIF (optionnel mais recommandé)
-- ===========================================================

-- Créer un rôle pour l'application (pas superuser)
-- CREATE ROLE budget_app_role LOGIN PASSWORD 'ton_mot_de_passe';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO budget_app_role;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO budget_app_role;