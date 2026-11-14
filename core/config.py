"""Design tokens, theme configuration, and global constants for Personal Finance Predictor."""

# Poster Modernist Color System
COLOR_BG = "#E3E2DE"
COLOR_PRIMARY_BLUE = "#1351AA"
COLOR_PRIMARY_TEXT = "#141414"
COLOR_SECONDARY_TEXT = "#444343"
COLOR_MUTED_LABELS = "#7A7A7A"
COLOR_BORDERS = "#C7C7C7"

# Derived UI state colors (strictly flat, non-vibrant)
COLOR_WHITE = "#FFFFFF"
COLOR_SURFACE_ALT = "#D9D8D3"
COLOR_ACCENT_HOVER = "#0F3F85"
COLOR_INCOME_ACCENT = "#1351AA"
COLOR_EXPENSE_ACCENT = "#141414"
COLOR_WARNING_BORDER = "#8A4300"

# Chart Palette (Poster Modernist Editorial Tones)
CHART_PALETTE = [
    "#1351AA",  # Primary Cobalt
    "#141414",  # Heavy Ink
    "#444343",  # Deep Graphite
    "#7A7A7A",  # Slate
    "#9E9D98",  # Stone
    "#BDBBB5",  # Canvas Deep
    "#2A6BC4",  # Sky Cobalt
    "#558AD6",  # Light Cobalt
]

# Standard Transaction Categories
CATEGORIES_EXPENSE = [
    "Food & Drink",
    "Rent",
    "Utilities",
    "Shopping",
    "Entertainment",
    "Health & Fitness",
    "Salary",
    "Travel",
    "Other Expense"
]

CATEGORIES_INCOME = [
    "Salary",
    "Investment",
    "Freelance",
    "Business",
    "Other Income"
]

ALL_CATEGORIES = sorted(list(set(CATEGORIES_EXPENSE + CATEGORIES_INCOME)))
