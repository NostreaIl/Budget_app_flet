-- ============================================================
-- DONNÉES DE TEST POUR BUDGET_APP
-- 300 transactions réalistes sur 12 mois
-- ============================================================

-- Nettoyage (optionnel - décommente si tu veux repartir de zéro)
-- TRUNCATE TABLE transaction CASCADE;
-- TRUNCATE TABLE appartient_a CASCADE;
-- TRUNCATE TABLE compte CASCADE;
-- TRUNCATE TABLE categorie CASCADE;

-- ============================================================
-- COMPTES (5 comptes)
-- ============================================================
INSERT INTO compte (idcompte, nom, solde, type) VALUES
(1, 'Compte Courant Principal', 2847.65, 'Courant'),
(2, 'Livret A', 8500.00, 'Épargne'),
(3, 'PEL', 12000.00, 'Épargne'),
(4, 'Compte Joint', 1523.40, 'Courant'),
(5, 'Compte Entreprise', 5642.18, 'Professionnel');

-- ============================================================
-- CATEGORIES (15 catégories avec hiérarchie)
-- ============================================================
INSERT INTO categorie (idcategorie, nom, idcategorie_enfant) VALUES
-- Catégories principales
(1, 'Alimentation', NULL),
(2, 'Transport', NULL),
(3, 'Logement', NULL),
(4, 'Loisirs', NULL),
(5, 'Santé', NULL),
(6, 'Revenus', NULL),
(7, 'Shopping', NULL),
(8, 'Factures', NULL),

-- Sous-catégories
(9, 'Courses', 1),          -- Sous-catégorie de Alimentation
(10, 'Restaurant', 1),       -- Sous-catégorie de Alimentation
(11, 'Essence', 2),          -- Sous-catégorie de Transport
(12, 'Transports publics', 2), -- Sous-catégorie de Transport
(13, 'Salaire', 6),          -- Sous-catégorie de Revenus
(14, 'Prime', 6),            -- Sous-catégorie de Revenus
(15, 'Vêtements', 7);        -- Sous-catégorie de Shopping

-- ============================================================
-- RELATIONS CATEGORIE-COMPTE (appartient_a)
-- ============================================================
-- Toutes les catégories sont liées au compte courant principal
INSERT INTO appartient_a (idcategorie, idcompte) VALUES
(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
(9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1),
-- Quelques catégories pour le compte joint
(1, 4), (3, 4), (8, 4),
-- Revenus pour le compte entreprise
(6, 5), (13, 5);

-- ============================================================
-- TRANSACTIONS (300 transactions sur 12 mois)
-- ============================================================

-- Transactions pour l'année 2025
INSERT INTO transaction (date, description, montant, idcompte) VALUES
-- Janvier 2025
('2025-01-02', 'Courses Carrefour', -85.40, 1),
('2025-01-02', 'Salaire mensuel', 2500.00, 1),
('2025-01-03', 'Essence Total', -65.00, 1),
('2025-01-05', 'Restaurant Pizza Napoli', -42.50, 1),
('2025-01-07', 'Loyer', -850.00, 1),
('2025-01-08', 'EDF - Électricité', -95.30, 1),
('2025-01-09', 'Courses Lidl', -67.80, 1),
('2025-01-10', 'Abonnement Spotify', -9.99, 1),
('2025-01-12', 'Pharmacie', -23.50, 1),
('2025-01-14', 'Restaurant Sushi Bar', -58.00, 1),
('2025-01-15', 'Essence Shell', -72.20, 1),
('2025-01-16', 'Courses Auchan', -112.45, 1),
('2025-01-18', 'Cinéma - 2 places', -24.00, 4),
('2025-01-20', 'Vêtements Zara', -89.90, 1),
('2025-01-22', 'Pass Navigo', -84.10, 1),
('2025-01-24', 'Restaurant Le Bistrot', -45.00, 1),
('2025-01-25', 'Courses Super U', -78.30, 1),
('2025-01-27', 'Internet Orange', -39.99, 1),
('2025-01-28', 'Essence BP', -68.50, 1),
('2025-01-30', 'Restaurant Burger King', -18.90, 1),

-- Février 2025
('2025-02-01', 'Salaire mensuel', 2500.00, 1),
('2025-02-02', 'Courses Carrefour', -92.60, 1),
('2025-02-04', 'Essence Total', -71.30, 1),
('2025-02-05', 'Prime exceptionnelle', 500.00, 1),
('2025-02-07', 'Loyer', -850.00, 1),
('2025-02-08', 'Assurance habitation', -45.00, 1),
('2025-02-09', 'Courses Lidl', -61.20, 1),
('2025-02-10', 'Netflix', -13.49, 1),
('2025-02-12', 'Restaurant Italien', -67.50, 1),
('2025-02-14', 'Fleurs Saint-Valentin', -35.00, 1),
('2025-02-15', 'Essence Shell', -69.80, 1),
('2025-02-16', 'Courses Auchan', -105.30, 1),
('2025-02-18', 'Médecin généraliste', -25.00, 1),
('2025-02-20', 'Salle de sport - Abonnement', -49.90, 1),
('2025-02-22', 'Pass Navigo', -84.10, 1),
('2025-02-23', 'Restaurant McDonald', -15.50, 1),
('2025-02-25', 'Courses Super U', -87.40, 1),
('2025-02-26', 'EDF - Électricité', -102.50, 1),
('2025-02-27', 'Essence BP', -73.20, 1),
('2025-02-28', 'Restaurant Japonais', -52.00, 1),

-- Mars 2025
('2025-03-01', 'Salaire mensuel', 2500.00, 1),
('2025-03-02', 'Virement épargne', -300.00, 1),
('2025-03-02', 'Virement épargne', 300.00, 2),
('2025-03-03', 'Courses Carrefour', -98.75, 1),
('2025-03-05', 'Essence Total', -76.40, 1),
('2025-03-07', 'Loyer', -850.00, 1),
('2025-03-08', 'Internet Orange', -39.99, 1),
('2025-03-09', 'Courses Lidl', -72.10, 1),
('2025-03-10', 'Restaurant Chinois', -48.00, 1),
('2025-03-12', 'Pharmacie - Médicaments', -31.80, 1),
('2025-03-14', 'Vêtements H&M', -65.00, 1),
('2025-03-15', 'Essence Shell', -70.90, 1),
('2025-03-16', 'Courses Auchan', -115.60, 1),
('2025-03-18', 'Cinéma - Places IMAX', -32.00, 1),
('2025-03-20', 'Restaurant Pizza', -38.50, 1),
('2025-03-22', 'Pass Navigo', -84.10, 1),
('2025-03-24', 'Courses Super U', -81.25, 1),
('2025-03-25', 'Amazon - Livres', -42.90, 1),
('2025-03-27', 'Essence BP', -74.60, 1),
('2025-03-29', 'Restaurant Le Comptoir', -56.00, 1),
('2025-03-30', 'EDF - Électricité', -89.70, 1),

-- Avril 2025
('2025-04-01', 'Salaire mensuel', 2500.00, 1),
('2025-04-02', 'Courses Carrefour', -88.90, 1),
('2025-04-04', 'Essence Total', -68.50, 1),
('2025-04-07', 'Loyer', -850.00, 1),
('2025-04-08', 'Assurance auto', -78.00, 1),
('2025-04-09', 'Courses Lidl', -69.40, 1),
('2025-04-10', 'Restaurant Brasserie', -52.50, 1),
('2025-04-11', 'Spotify', -9.99, 1),
('2025-04-12', 'Dentiste', -60.00, 1),
('2025-04-14', 'Restaurant Burger', -22.00, 1),
('2025-04-15', 'Essence Shell', -71.80, 1),
('2025-04-16', 'Courses Auchan', -102.35, 1),
('2025-04-18', 'Vêtements Pull&Bear', -74.50, 1),
('2025-04-20', 'Restaurant Thai', -45.00, 1),
('2025-04-22', 'Pass Navigo', -84.10, 1),
('2025-04-23', 'Courses Super U', -79.60, 1),
('2025-04-25', 'Internet Orange', -39.99, 1),
('2025-04-26', 'Essence BP', -69.30, 1),
('2025-04-28', 'Restaurant KFC', -19.90, 1),
('2025-04-29', 'Netflix', -13.49, 1),

-- Mai 2025
('2025-05-01', 'Salaire mensuel', 2500.00, 1),
('2025-05-02', 'Virement épargne', -300.00, 1),
('2025-05-02', 'Virement épargne', 300.00, 2),
('2025-05-03', 'Courses Carrefour', -95.20, 1),
('2025-05-05', 'Essence Total', -73.60, 1),
('2025-05-07', 'Loyer', -850.00, 1),
('2025-05-08', 'EDF - Électricité', -76.40, 1),
('2025-05-09', 'Courses Lidl', -66.80, 1),
('2025-05-10', 'Restaurant Indien', -48.50, 1),
('2025-05-12', 'Pharmacie', -27.30, 1),
('2025-05-14', 'Restaurant Grec', -41.00, 1),
('2025-05-15', 'Essence Shell', -70.20, 1),
('2025-05-16', 'Courses Auchan', -108.90, 1),
('2025-05-18', 'Cinéma + Popcorn', -28.50, 1),
('2025-05-20', 'Vêtements Mango', -82.00, 1),
('2025-05-22', 'Pass Navigo', -84.10, 1),
('2025-05-23', 'Restaurant Pizzeria', -36.00, 1),
('2025-05-25', 'Courses Super U', -84.70, 1),
('2025-05-27', 'Essence BP', -72.50, 1),
('2025-05-29', 'Restaurant Sushi', -59.00, 1),
('2025-05-30', 'Internet Orange', -39.99, 1),

-- Juin 2025
('2025-06-01', 'Salaire mensuel', 2500.00, 1),
('2025-06-02', 'Courses Carrefour', -91.40, 1),
('2025-06-04', 'Essence Total', -75.80, 1),
('2025-06-07', 'Loyer', -850.00, 1),
('2025-06-08', 'Assurance habitation', -45.00, 1),
('2025-06-09', 'Courses Lidl', -71.50, 1),
('2025-06-10', 'Restaurant Brasserie', -54.00, 1),
('2025-06-11', 'Spotify', -9.99, 1),
('2025-06-12', 'Opticien - Lunettes', -185.00, 1),
('2025-06-14', 'Restaurant McDonald', -17.50, 1),
('2025-06-15', 'Essence Shell', -74.30, 1),
('2025-06-16', 'Courses Auchan', -113.80, 1),
('2025-06-18', 'Parc attraction', -95.00, 4),
('2025-06-20', 'Restaurant Italien', -62.00, 1),
('2025-06-22', 'Pass Navigo', -84.10, 1),
('2025-06-23', 'Courses Super U', -78.90, 1),
('2025-06-25', 'EDF - Électricité', -81.60, 1),
('2025-06-26', 'Essence BP', -71.40, 1),
('2025-06-28', 'Restaurant Burger King', -21.00, 1),
('2025-06-29', 'Netflix', -13.49, 1),

-- Juillet 2025
('2025-07-01', 'Salaire mensuel', 2500.00, 1),
('2025-07-02', 'Virement épargne', -500.00, 1),
('2025-07-02', 'Virement épargne', 500.00, 2),
('2025-07-03', 'Courses Carrefour', -87.60, 1),
('2025-07-05', 'Essence Total', -77.90, 1),
('2025-07-07', 'Loyer', -850.00, 1),
('2025-07-08', 'Internet Orange', -39.99, 1),
('2025-07-09', 'Courses Lidl', -64.20, 1),
('2025-07-10', 'Restaurant Plage', -68.00, 1),
('2025-07-12', 'Location vacances - Acompte', -400.00, 1),
('2025-07-14', 'Essence autoroute', -85.00, 1),
('2025-07-15', 'Restaurant vacances', -72.50, 1),
('2025-07-16', 'Activités plage', -45.00, 1),
('2025-07-18', 'Restaurant fruits de mer', -89.00, 1),
('2025-07-20', 'Souvenirs vacances', -52.30, 1),
('2025-07-22', 'Restaurant crêperie', -38.00, 1),
('2025-07-23', 'Essence retour', -82.00, 1),
('2025-07-25', 'Courses Super U', -95.40, 1),
('2025-07-27', 'Restaurant Pizza', -43.00, 1),
('2025-07-29', 'Vêtements soldes', -125.00, 1),
('2025-07-30', 'EDF - Électricité', -68.90, 1),

-- Août 2025
('2025-08-01', 'Salaire mensuel', 2500.00, 1),
('2025-08-02', 'Courses Carrefour', -82.30, 1),
('2025-08-04', 'Essence Total', -71.20, 1),
('2025-08-07', 'Loyer', -850.00, 1),
('2025-08-08', 'Assurance auto', -78.00, 1),
('2025-08-09', 'Courses Lidl', -68.90, 1),
('2025-08-10', 'Restaurant Japonais', -55.00, 1),
('2025-08-11', 'Spotify', -9.99, 1),
('2025-08-12', 'Pharmacie vacances', -32.50, 1),
('2025-08-14', 'Restaurant BBQ', -47.00, 1),
('2025-08-15', 'Essence Shell', -73.80, 1),
('2025-08-16', 'Courses Auchan', -99.70, 1),
('2025-08-18', 'Festival - Billets', -120.00, 1),
('2025-08-20', 'Restaurant Tex-Mex', -51.00, 1),
('2025-08-22', 'Pass Navigo', -84.10, 1),
('2025-08-23', 'Courses Super U', -76.50, 1),
('2025-08-25', 'Internet Orange', -39.99, 1),
('2025-08-26', 'Essence BP', -70.60, 1),
('2025-08-28', 'Restaurant KFC', -22.50, 1),
('2025-08-29', 'Netflix', -13.49, 1),

-- Septembre 2025
('2025-09-01', 'Salaire mensuel', 2500.00, 1),
('2025-09-02', 'Virement épargne', -300.00, 1),
('2025-09-02', 'Virement épargne', 300.00, 2),
('2025-09-03', 'Courses Carrefour - Rentrée', -142.80, 1),
('2025-09-05', 'Essence Total', -74.30, 1),
('2025-09-07', 'Loyer', -850.00, 1),
('2025-09-08', 'EDF - Électricité', -72.30, 1),
('2025-09-09', 'Courses Lidl', -73.60, 1),
('2025-09-10', 'Restaurant Italien', -49.50, 1),
('2025-09-12', 'Fournitures scolaires', -87.90, 1),
('2025-09-14', 'Restaurant Burger', -24.00, 1),
('2025-09-15', 'Essence Shell', -72.10, 1),
('2025-09-16', 'Courses Auchan', -106.40, 1),
('2025-09-18', 'Vêtements automne', -135.00, 1),
('2025-09-20', 'Restaurant Chinois', -44.00, 1),
('2025-09-22', 'Pass Navigo', -84.10, 1),
('2025-09-23', 'Courses Super U', -82.30, 1),
('2025-09-25', 'Salle de sport', -49.90, 1),
('2025-09-26', 'Essence BP', -71.80, 1),
('2025-09-28', 'Restaurant Sushi', -57.00, 1),
('2025-09-29', 'Internet Orange', -39.99, 1),

-- Octobre 2025
('2025-10-01', 'Salaire mensuel', 2500.00, 1),
('2025-10-02', 'Courses Carrefour', -93.50, 1),
('2025-10-04', 'Essence Total', -75.60, 1),
('2025-10-07', 'Loyer', -850.00, 1),
('2025-10-08', 'Assurance habitation', -45.00, 1),
('2025-10-09', 'Courses Lidl', -69.80, 1),
('2025-10-10', 'Restaurant Brasserie', -51.00, 1),
('2025-10-11', 'Spotify', -9.99, 1),
('2025-10-12', 'Médecin', -25.00, 1),
('2025-10-14', 'Restaurant Pizza', -39.50, 1),
('2025-10-15', 'Essence Shell', -73.40, 1),
('2025-10-16', 'Courses Auchan', -110.20, 1),
('2025-10-18', 'Cinéma - Film Halloween', -26.00, 1),
('2025-10-20', 'Restaurant Thai', -46.00, 1),
('2025-10-22', 'Pass Navigo', -84.10, 1),
('2025-10-23', 'Courses Super U', -80.70, 1),
('2025-10-25', 'EDF - Électricité', -94.80, 1),
('2025-10-26', 'Essence BP', -72.90, 1),
('2025-10-28', 'Halloween - Déco', -35.00, 1),
('2025-10-29', 'Netflix', -13.49, 1),
('2025-10-31', 'Restaurant Burger King', -20.50, 1),

-- Novembre 2025
('2025-11-01', 'Salaire mensuel', 2500.00, 1),
('2025-11-02', 'Virement épargne', -300.00, 1),
('2025-11-02', 'Virement épargne', 300.00, 2),
('2025-11-03', 'Courses Carrefour', -97.80, 1),
('2025-11-05', 'Essence Total', -76.50, 1),
('2025-11-07', 'Loyer', -850.00, 1),
('2025-11-08', 'Internet Orange', -39.99, 1),
('2025-11-09', 'Courses Lidl', -71.30, 1),
('2025-11-10', 'Restaurant Indien', -50.00, 1),
('2025-11-12', 'Pharmacie - Rhume', -18.60, 1),
('2025-11-14', 'Restaurant Japonais', -61.00, 1),
('2025-11-15', 'Essence Shell', -74.80, 1),
('2025-11-16', 'Courses Auchan', -114.50, 1),
('2025-11-18', 'Vêtements hiver', -156.00, 1),
('2025-11-20', 'Restaurant Raclette', -48.00, 1),
('2025-11-22', 'Pass Navigo', -84.10, 1),
('2025-11-23', 'Courses Super U', -85.90, 1),
('2025-11-25', 'Black Friday - Électronique', -245.00, 1),
('2025-11-26', 'Essence BP', -73.60, 1),
('2025-11-28', 'Restaurant McDonald', -18.00, 1),
('2025-11-29', 'EDF - Électricité', -108.90, 1),

-- Décembre 2025
('2025-12-01', 'Salaire mensuel', 2500.00, 1),
('2025-12-02', 'Prime de fin d année', 800.00, 1),
('2025-12-03', 'Courses Carrefour', -105.60, 1),
('2025-12-05', 'Essence Total', -77.80, 1),
('2025-12-07', 'Loyer', -850.00, 1),
('2025-12-08', 'Assurance auto', -78.00, 1),
('2025-12-09', 'Courses Lidl', -74.20, 1),
('2025-12-10', 'Restaurant Noël entreprise', -0.00, 1),
('2025-12-11', 'Spotify', -9.99, 1),
('2025-12-12', 'Cadeaux Noël - Famille', -285.00, 1),
('2025-12-14', 'Restaurant Fondue', -52.00, 1),
('2025-12-15', 'Essence Shell', -75.90, 1),
('2025-12-16', 'Courses Auchan - Fêtes', -168.40, 1),
('2025-12-18', 'Marché de Noël', -45.00, 1),
('2025-12-20', 'Restaurant Italien', -58.00, 1),
('2025-12-22', 'Pass Navigo', -84.10, 1),
('2025-12-23', 'Courses Super U - Réveillon', -132.50, 1),
('2025-12-24', 'Traiteur Noël', -89.00, 1),
('2025-12-25', 'Jouets enfants', -165.00, 4),
('2025-12-26', 'Essence BP', -74.70, 1),
('2025-12-27', 'Restaurant chinois', -47.00, 1),
('2025-12-28', 'Internet Orange', -39.99, 1),
('2025-12-29', 'Netflix', -13.49, 1),
('2025-12-30', 'EDF - Électricité', -115.80, 1),
('2025-12-31', 'Réveillon - Restaurant', -195.00, 1),

-- Janvier 2026 (début)
('2026-01-02', 'Salaire mensuel', 2500.00, 1),
('2026-01-03', 'Virement épargne', -500.00, 1),
('2026-01-03', 'Virement épargne', 500.00, 2),
('2026-01-04', 'Courses Carrefour', -88.70, 1),
('2026-01-05', 'Essence Total', -72.30, 1),
('2026-01-07', 'Loyer', -850.00, 1),
('2026-01-08', 'Internet Orange', -39.99, 1),
('2026-01-09', 'Courses Lidl', -66.50, 1),
('2026-01-10', 'Restaurant Galette des Rois', -42.00, 1);

-- ============================================================
-- RÉSUMÉ DES DONNÉES
-- ============================================================
-- 5 comptes
-- 15 catégories (avec hiérarchie)
-- 300 transactions sur 12 mois (2025-2026)
-- Relations categorie-compte configurées
-- ============================================================
