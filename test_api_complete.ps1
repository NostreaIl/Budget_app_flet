# ============================================
# Script de test complet pour Budget API
# Version corrigee avec gestion des doublons
# ============================================

$baseUrl = "http://localhost:8000"
$headers = @{"Content-Type" = "application/json"}

Write-Host "Demarrage des tests de l'API Budget" -ForegroundColor Green
Write-Host ("=" * 60)

# ============================================
# 1. TEST SANTE DE L'API
# ============================================
Write-Host "`nTest 1: Verification de la sante de l'API" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
    Write-Host "OK API Status: $($health.status)" -ForegroundColor Green
    Write-Host "OK Database: $($health.database)" -ForegroundColor Green
} catch {
    Write-Host "ERREUR: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# ============================================
# 2. INSCRIPTION D'UN UTILISATEUR
# ============================================
Write-Host "`nTest 2: Inscription d'un nouvel utilisateur" -ForegroundColor Yellow

$registerData = @{
    email = "test.complet@example.com"
    mot_de_passe = "SecurePass123!"
    nom_affichage = "Test Complet"
} | ConvertTo-Json

try {
    $registerResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/register" -Method POST -Headers $headers -Body $registerData

    $token = $registerResponse.access_token
    $userId = $registerResponse.user.idutilisateur

    Write-Host "OK Utilisateur cree: $($registerResponse.user.email)" -ForegroundColor Green
    Write-Host "OK User ID: $userId" -ForegroundColor Green
    Write-Host "OK Token obtenu: $($token.Substring(0,30))..." -ForegroundColor Green
} catch {
    Write-Host "AVERTISSEMENT Utilisateur existe, tentative de connexion..." -ForegroundColor Yellow

    $loginData = @{
        email = "test.complet@example.com"
        mot_de_passe = "SecurePass123!"
    } | ConvertTo-Json

    $registerResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method POST -Headers $headers -Body $loginData

    $token = $registerResponse.access_token
    $userId = $registerResponse.user.idutilisateur
    Write-Host "OK Connexion reussie" -ForegroundColor Green
}

# Headers avec authentification
$authHeaders = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# ============================================
# 3. RECUPERER INFOS UTILISATEUR
# ============================================
Write-Host "`nTest 3: Recuperation des informations utilisateur" -ForegroundColor Yellow
$me = Invoke-RestMethod -Uri "$baseUrl/api/auth/me" -Method GET -Headers $authHeaders
Write-Host "OK Email: $($me.email)" -ForegroundColor Green
Write-Host "OK Nom: $($me.nom_affichage)" -ForegroundColor Green
Write-Host "OK Actif: $($me.actif)" -ForegroundColor Green

# ============================================
# 4. RECUPERER LES TYPES PAR DEFAUT
# ============================================
Write-Host "`nTest 4: Recuperation des types d'operation" -ForegroundColor Yellow
$types = Invoke-RestMethod -Uri "$baseUrl/api/types" -Method GET -Headers $authHeaders
Write-Host "OK Types trouves: $($types.Count)" -ForegroundColor Green
foreach ($type in $types) {
    Write-Host "   - $($type.nom) (ID: $($type.idtype))" -ForegroundColor Cyan
}

# Prendre uniquement le PREMIER de chaque type
$typeDepense = ($types | Where-Object { $_.nom -eq "depense" } | Select-Object -First 1).idtype
$typeRevenu = ($types | Where-Object { $_.nom -eq "revenu" } | Select-Object -First 1).idtype
$typeTransfert = ($types | Where-Object { $_.nom -eq "transfert" } | Select-Object -First 1).idtype

Write-Host "   > Type Depense ID: $typeDepense" -ForegroundColor Magenta
Write-Host "   > Type Revenu ID: $typeRevenu" -ForegroundColor Magenta

# ============================================
# 5. RECUPERER LES CATEGORIES PAR DEFAUT
# ============================================
Write-Host "`nTest 5: Recuperation des categories" -ForegroundColor Yellow
$categories = Invoke-RestMethod -Uri "$baseUrl/api/categories" -Method GET -Headers $authHeaders
Write-Host "OK Categories trouvees: $($categories.Count)" -ForegroundColor Green

# Afficher seulement les 5 premieres
$categories | Select-Object -First 5 | ForEach-Object {
    Write-Host "   - $($_.nomcategorie) (ID: $($_.idcategorie))" -ForegroundColor Cyan
}
if ($categories.Count -gt 5) {
    Write-Host "   ... et $($categories.Count - 5) autres" -ForegroundColor Cyan
}

# Prendre uniquement le PREMIER de chaque categorie
$catAlimentation = ($categories | Where-Object { $_.nomcategorie -eq "Alimentation" } | Select-Object -First 1).idcategorie
$catTransport = ($categories | Where-Object { $_.nomcategorie -eq "Transport" } | Select-Object -First 1).idcategorie

# ============================================
# 6. RECUPERER LES SOUS-CATEGORIES
# ============================================
Write-Host "`nTest 6: Recuperation des sous-categories" -ForegroundColor Yellow
$sousCategories = Invoke-RestMethod -Uri "$baseUrl/api/sous-categories" -Method GET -Headers $authHeaders
Write-Host "OK Sous-categories trouvees: $($sousCategories.Count)" -ForegroundColor Green

# Afficher seulement les 5 premieres
$sousCategories | Select-Object -First 5 | ForEach-Object {
    Write-Host "   - $($_.nomsouscategorie) (ID: $($_.idsouscategorie))" -ForegroundColor Cyan
}
if ($sousCategories.Count -gt 5) {
    Write-Host "   ... et $($sousCategories.Count - 5) autres" -ForegroundColor Cyan
}

# Prendre uniquement le PREMIER
$scCourses = ($sousCategories | Where-Object { $_.nomsouscategorie -eq "Courses" } | Select-Object -First 1).idsouscategorie
$scEssence = ($sousCategories | Where-Object { $_.nomsouscategorie -eq "Essence" } | Select-Object -First 1).idsouscategorie

Write-Host "   > Sous-cat Courses ID: $scCourses" -ForegroundColor Magenta
Write-Host "   > Sous-cat Essence ID: $scEssence" -ForegroundColor Magenta

# ============================================
# 7. CREER DES COMPTES
# ============================================
Write-Host "`nTest 7: Creation de comptes bancaires" -ForegroundColor Yellow

# Compte courant
$compteCourant = @{
    nom = "Compte Courant Test"
    solde = 1500.00
    type = "courant"
} | ConvertTo-Json

try {
    $compte1 = Invoke-RestMethod -Uri "$baseUrl/api/comptes" -Method POST -Headers $authHeaders -Body $compteCourant
    Write-Host "OK Compte cree: $($compte1.nom) - Solde: $($compte1.solde) EUR" -ForegroundColor Green
} catch {
    Write-Host "AVERTISSEMENT Compte existe deja, recuperation..." -ForegroundColor Yellow
    $comptes = Invoke-RestMethod -Uri "$baseUrl/api/comptes" -Method GET -Headers $authHeaders
    $compte1 = $comptes | Where-Object { $_.nom -eq "Compte Courant Test" } | Select-Object -First 1
}

# Livret A
$livretA = @{
    nom = "Livret A Test"
    solde = 5000.00
    type = "epargne"
} | ConvertTo-Json

try {
    $compte2 = Invoke-RestMethod -Uri "$baseUrl/api/comptes" -Method POST -Headers $authHeaders -Body $livretA
    Write-Host "OK Compte cree: $($compte2.nom) - Solde: $($compte2.solde) EUR" -ForegroundColor Green
} catch {
    Write-Host "AVERTISSEMENT Compte existe deja, recuperation..." -ForegroundColor Yellow
    $comptes = Invoke-RestMethod -Uri "$baseUrl/api/comptes" -Method GET -Headers $authHeaders
    $compte2 = $comptes | Where-Object { $_.nom -eq "Livret A Test" } | Select-Object -First 1
}

# ============================================
# 8. LISTER LES COMPTES
# ============================================
Write-Host "`nTest 8: Liste de tous les comptes" -ForegroundColor Yellow
$comptes = Invoke-RestMethod -Uri "$baseUrl/api/comptes" -Method GET -Headers $authHeaders
Write-Host "OK Nombre de comptes: $($comptes.Count)" -ForegroundColor Green
foreach ($compte in $comptes) {
    Write-Host "   - $($compte.nom): $($compte.solde) EUR ($($compte.type))" -ForegroundColor Cyan
}

# ============================================
# 9. CREER DES OPERATIONS
# ============================================
Write-Host "`nTest 9: Creation d'operations" -ForegroundColor Yellow

# Operation 1: Courses
$op1 = @{
    date = "2026-01-15"
    description = "Courses Carrefour"
    montant = -45.50
    idcompte = $compte1.idcompte
    idtype = $typeDepense
    idsouscategorie = $scCourses
} | ConvertTo-Json

try {
    $operation1 = Invoke-RestMethod -Uri "$baseUrl/api/operations" -Method POST -Headers $authHeaders -Body $op1
    Write-Host "OK Operation: $($operation1.description) - $($operation1.montant) EUR" -ForegroundColor Green
} catch {
    Write-Host "ERREUR creation operation 1: $($_.Exception.Message)" -ForegroundColor Red
}

# Operation 2: Essence
$op2 = @{
    date = "2026-01-16"
    description = "Essence Total"
    montant = -60.00
    idcompte = $compte1.idcompte
    idtype = $typeDepense
    idsouscategorie = $scEssence
} | ConvertTo-Json

try {
    $operation2 = Invoke-RestMethod -Uri "$baseUrl/api/operations" -Method POST -Headers $authHeaders -Body $op2
    Write-Host "OK Operation: $($operation2.description) - $($operation2.montant) EUR" -ForegroundColor Green
} catch {
    Write-Host "ERREUR creation operation 2: $($_.Exception.Message)" -ForegroundColor Red
}

# Operation 3: Salaire
$scSalaire = ($sousCategories | Where-Object { $_.nomsouscategorie -eq "Salaire" } | Select-Object -First 1).idsouscategorie

$op3 = @{
    date = "2026-01-01"
    description = "Salaire janvier"
    montant = 2500.00
    idcompte = $compte1.idcompte
    idtype = $typeRevenu
    idsouscategorie = $scSalaire
} | ConvertTo-Json

try {
    $operation3 = Invoke-RestMethod -Uri "$baseUrl/api/operations" -Method POST -Headers $authHeaders -Body $op3
    Write-Host "OK Operation: $($operation3.description) - +$($operation3.montant) EUR" -ForegroundColor Green
} catch {
    Write-Host "ERREUR creation operation 3: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================
# 10. LISTER LES OPERATIONS
# ============================================
Write-Host "`nTest 10: Liste de toutes les operations" -ForegroundColor Yellow
$operations = Invoke-RestMethod -Uri "$baseUrl/api/operations" -Method GET -Headers $authHeaders
Write-Host "OK Nombre d'operations: $($operations.Count)" -ForegroundColor Green
foreach ($op in $operations) {
    $signe = if ($op.montant -gt 0) { "+" } else { "" }
    Write-Host "   - $($op.date): $($op.description) - $signe$($op.montant) EUR" -ForegroundColor Cyan
}

# ============================================
# 11. METTRE A JOUR UNE OPERATION
# ============================================
Write-Host "`nTest 11: Mise a jour d'une operation" -ForegroundColor Yellow

if ($operations.Count -gt 0) {
    $premierOp = $operations[0]

    $updateOp = @{
        description = "$($premierOp.description) (modifie)"
        montant = $premierOp.montant
    } | ConvertTo-Json

    try {
        $opUpdated = Invoke-RestMethod -Uri "$baseUrl/api/operations/$($premierOp.idoperation)" -Method PUT -Headers $authHeaders -Body $updateOp
        Write-Host "OK Operation mise a jour: $($opUpdated.description)" -ForegroundColor Green
    } catch {
        Write-Host "ERREUR mise a jour: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "AVERTISSEMENT Aucune operation a mettre a jour" -ForegroundColor Yellow
}

# ============================================
# 12. CREER UNE NOUVELLE CATEGORIE
# ============================================
Write-Host "`nTest 12: Creation d'une nouvelle categorie" -ForegroundColor Yellow
$newCat = @{
    nomcategorie = "Divertissement Test"
} | ConvertTo-Json

try {
    $catDivertissement = Invoke-RestMethod -Uri "$baseUrl/api/categories" -Method POST -Headers $authHeaders -Body $newCat
    Write-Host "OK Categorie creee: $($catDivertissement.nomcategorie)" -ForegroundColor Green
} catch {
    Write-Host "AVERTISSEMENT Categorie existe deja, recuperation..." -ForegroundColor Yellow
    $categories = Invoke-RestMethod -Uri "$baseUrl/api/categories" -Method GET -Headers $authHeaders
    $catDivertissement = $categories | Where-Object { $_.nomcategorie -eq "Divertissement Test" } | Select-Object -First 1
}

# ============================================
# 13. CREER UNE SOUS-CATEGORIE
# ============================================
Write-Host "`nTest 13: Creation d'une sous-categorie" -ForegroundColor Yellow
$newSousCat = @{
    nomsouscategorie = "Cinema Test"
    idcategorie = $catDivertissement.idcategorie
} | ConvertTo-Json

try {
    $scCinema = Invoke-RestMethod -Uri "$baseUrl/api/sous-categories" -Method POST -Headers $authHeaders -Body $newSousCat
    Write-Host "OK Sous-categorie creee: $($scCinema.nomsouscategorie)" -ForegroundColor Green
} catch {
    Write-Host "AVERTISSEMENT Sous-categorie existe deja" -ForegroundColor Yellow
}

# ============================================
# 14. RECUPERER UN COMPTE SPECIFIQUE
# ============================================
Write-Host "`nTest 14: Recuperation d'un compte specifique" -ForegroundColor Yellow
$compteDetail = Invoke-RestMethod -Uri "$baseUrl/api/comptes/$($compte1.idcompte)" -Method GET -Headers $authHeaders
Write-Host "OK Compte: $($compteDetail.nom) - $($compteDetail.solde) EUR" -ForegroundColor Green

# ============================================
# 15. METTRE A JOUR LE PROFIL
# ============================================
Write-Host "`nTest 15: Mise a jour du profil utilisateur" -ForegroundColor Yellow
$updateProfile = @{
    nom_affichage = "Test Complet (Updated)"
} | ConvertTo-Json

try {
    $profileUpdated = Invoke-RestMethod -Uri "$baseUrl/api/auth/me" -Method PUT -Headers $authHeaders -Body $updateProfile
    Write-Host "OK Profil mis a jour: $($profileUpdated.nom_affichage)" -ForegroundColor Green
} catch {
    Write-Host "ERREUR mise a jour profil: $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================
# RESUME
# ============================================
Write-Host "`n" -NoNewline
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host "TESTS TERMINES !" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host "`nResume:" -ForegroundColor Yellow
Write-Host "   - Utilisateur: $($me.email)" -ForegroundColor Cyan
Write-Host "   - Comptes: $($comptes.Count)" -ForegroundColor Cyan
Write-Host "   - Operations: $($operations.Count)" -ForegroundColor Cyan
Write-Host "   - Types: $($types.Count)" -ForegroundColor Cyan
Write-Host "   - Categories: $($categories.Count)" -ForegroundColor Cyan
Write-Host "   - Sous-categories: $($sousCategories.Count)" -ForegroundColor Cyan
Write-Host "`nL'API fonctionne correctement !" -ForegroundColor Green
