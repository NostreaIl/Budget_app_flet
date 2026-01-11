# ui/theme/colors.py - Couleurs DA 2025 exactes pour BudgetApp
"""
Couleurs DA 2025 identiques au fichier colors.qml
Palette complète avec bleu nuit profond et violet lumineux
"""


class COLORS:
    """
    Classe contenant toutes les couleurs DA 2025 exactes
    Reproduit fidèlement le système de couleurs du QML
    """

    # ===== COULEURS PRINCIPALES =====
    # Arrière-plans
    BACKGROUND_PRINCIPAL = "#0F0F23"  # Bleu nuit profond
    BACKGROUND_SECONDAIRE = "#1A1A2E"  # Bleu nuit moyen
    CARTES_COMPOSANTS = "#2A2A3E"  # Bleu nuit clair
    BORDURES = "#3A3A54"  # Bleu gris pour bordures

    # Textes
    TEXTE_PRINCIPAL = "#FFFFFF"  # Blanc pur
    TEXTE_SECONDAIRE = "#B8B8CC"  # Gris bleuté clair
    TEXTE_DESACTIVE = "#666688"  # Gris bleuté foncé

    # Accents principaux
    ACCENT_PRINCIPAL = "#00E5FF"  # Cyan électrique
    ACCENT_SECONDAIRE = "#0091EA"  # Bleu cyan

    # États et catégories
    SUCCESS_REVENUS = "#4ECDC4"  # Turquoise (revenus)
    AVERTISSEMENT = "#FFE66D"  # Jaune doré (avertissement)
    ERREUR_DEPENSES = "#FF6B6B"  # Rouge corail (dépenses)

    # Violet lumineux (signature DA 2025)
    VIOLET_LUMINEUX = "#9C27B0"  # Violet principal
    VIOLET_GLOW = "#E1BEE7"  # Violet lumineux
    VIOLET_TRANSPARENT = "#9C27B015"  # Violet très transparent
    VIOLET_SOMBRE = "#6A1B7B"  # Violet sombre

    # ===== COULEURS ÉTENDUES =====
    # Variations d'arrière-plan
    SURFACE_ELEVATION_1 = "#252540"  # Surface légèrement élevée
    SURFACE_ELEVATION_2 = "#303050"  # Surface moyennement élevée
    SURFACE_ELEVATION_3 = "#3A3A60"  # Surface très élevée

    # Variations de texte
    TEXTE_ACCENT = "#00FFE5"  # Texte avec accent cyan
    TEXTE_SUCCES = "#00E676"  # Texte de succès
    TEXTE_ERREUR = "#FF5252"  # Texte d'erreur
    TEXTE_AVERTISSEMENT = "#FFAB00"  # Texte d'avertissement

    # Couleurs spécifiques aux catégories
    ALIMENTATION = "#FF7043"  # Orange alimentaire
    TRANSPORT = "#42A5F5"  # Bleu transport
    LOISIRS = "#AB47BC"  # Violet loisirs
    SANTE = "#26A69A"  # Teal santé
    EDUCATION = "#FFA726"  # Orange éducation
    SHOPPING = "#EC407A"  # Rose shopping
    FACTURES = "#78909C"  # Gris factures
    SALAIRE = "#66BB6A"  # Vert salaire
    EPARGNE = "#29B6F6"  # Bleu épargne
    AUTRE = "#8D6E63"  # Marron autre

    # ===== COULEURS UTILITAIRES =====
    # Transparences
    TRANSPARENT = "transparent"
    SEMI_TRANSPARENT = "#FFFFFF20"
    OVERLAY_SOMBRE = "#00000050"
    OVERLAY_CLAIR = "#FFFFFF10"

    # Dégradés (pour les effets visuels)
    GRADIENT_VIOLET = ["#9C27B0", "#E1BEE7"]
    GRADIENT_CYAN = ["#00E5FF", "#0091EA"]
    GRADIENT_BACKGROUND = ["#0F0F23", "#1A1A2E"]
    GRADIENT_SURFACE = ["#2A2A3E", "#3A3A54"]

    # ===== MÉTHODES UTILITAIRES =====
    @classmethod
    def get_category_color(cls, category_name: str) -> str:
        """
        Retourne la couleur associée à une catégorie

        Args:
            category_name: Nom de la catégorie

        Returns:
            str: Code couleur hexadécimal
        """
        category_colors = {
            "alimentation": cls.ALIMENTATION,
            "transport": cls.TRANSPORT,
            "loisirs": cls.LOISIRS,
            "santé": cls.SANTE,
            "education": cls.EDUCATION,
            "shopping": cls.SHOPPING,
            "factures": cls.FACTURES,
            "salaire": cls.SALAIRE,
            "épargne": cls.EPARGNE,
            "autre": cls.AUTRE
        }

        return category_colors.get(category_name.lower(), cls.AUTRE)

    @classmethod
    def get_status_color(cls, status: str) -> str:
        """
        Retourne la couleur associée à un statut

        Args:
            status: Statut (success, warning, error, info)

        Returns:
            str: Code couleur hexadécimal
        """
        status_colors = {
            "success": cls.SUCCESS_REVENUS,
            "warning": cls.AVERTISSEMENT,
            "error": cls.ERREUR_DEPENSES,
            "info": cls.ACCENT_PRINCIPAL
        }

        return status_colors.get(status.lower(), cls.TEXTE_SECONDAIRE)

    @classmethod
    def add_transparency(cls, color: str, opacity: float = 0.1) -> str:
        """
        Ajoute de la transparence à une couleur

        Args:
            color: Couleur hexadécimal (#RRGGBB)
            opacity: Opacité (0.0 à 1.0)

        Returns:
            str: Couleur avec transparence
        """
        if color.startswith('#'):
            # Convertir l'opacité en hexadécimal (0-255)
            alpha = int(opacity * 255)
            return f"{color}{alpha:02X}"

        return color

    @classmethod
    def is_dark_theme(cls) -> bool:
        """
        Indique si le thème est sombre

        Returns:
            bool: True (thème DA 2025 est sombre)
        """
        return True

    @classmethod
    def get_contrast_color(cls, background_color: str) -> str:
        """
        Retourne la couleur de texte appropriée pour un arrière-plan

        Args:
            background_color: Couleur d'arrière-plan

        Returns:
            str: Couleur de texte (blanc ou noir selon le contraste)
        """
        # Pour le thème DA 2025, on utilise principalement du blanc
        dark_backgrounds = [
            cls.BACKGROUND_PRINCIPAL,
            cls.BACKGROUND_SECONDAIRE,
            cls.CARTES_COMPOSANTS,
            cls.VIOLET_LUMINEUX,
            cls.VIOLET_SOMBRE
        ]

        if background_color in dark_backgrounds:
            return cls.TEXTE_PRINCIPAL
        else:
            return cls.BACKGROUND_PRINCIPAL