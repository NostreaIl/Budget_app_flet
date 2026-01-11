-- ============================================================
-- MIGRATION : Ajout de la table TYPE et modification TRANSACTION
-- ============================================================

-- Étape 1 : Créer la table TYPE
CREATE TABLE IF NOT EXISTS TYPE (
  idType INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  nom VARCHAR(50) NOT NULL,
  CONSTRAINT TYPE_PK PRIMARY KEY (idType),
  CONSTRAINT nom_UNQ UNIQUE (nom)
);

-- Étape 2 : Insérer les types de transaction
INSERT INTO TYPE (idType, nom) OVERRIDING SYSTEM VALUE VALUES
  (1, 'depense'),
  (2, 'revenu'),
  (3, 'transfert')
ON CONFLICT (nom) DO NOTHING;  -- Ignore si déjà existant

-- Étape 3 : Ajouter la colonne idType à TRANSACTION (temporairement nullable)
ALTER TABLE transaction
ADD COLUMN IF NOT EXISTS idType INTEGER;

-- Étape 4 : Remplir idType basé sur le montant
UPDATE transaction
SET idType = CASE
  WHEN montant >= 0 THEN 2  -- revenu
  ELSE 1                     -- depense
END
WHERE idType IS NULL;

-- Étape 5 : Rendre idType obligatoire
ALTER TABLE transaction
ALTER COLUMN idType SET NOT NULL;

-- Étape 6 : Ajouter la contrainte de clé étrangère
ALTER TABLE transaction
ADD CONSTRAINT TRANSACTION_idType_FK
FOREIGN KEY (idType) REFERENCES TYPE (idType);

-- ============================================================
-- MIGRATION TERMINÉE !
-- ============================================================
-- Vérification :
SELECT 'TYPE count:' as info, COUNT(*) as count FROM TYPE
UNION ALL
SELECT 'TRANSACTION avec idType:', COUNT(*) FROM TRANSACTION WHERE idType IS NOT NULL;
