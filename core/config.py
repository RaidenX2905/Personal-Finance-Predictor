"""Black and White Monochromatic Design Tokens — Light Mode Only."""

# Pure Monochromatic Light Mode Palette
COLOR_BG = "#FFFFFF"              # Crisp pure white paper canvas
COLOR_SURFACE = "#FAFAFA"         # Subtle off-white surface
COLOR_SURFACE_ALT = "#F4F4F4"     # Secondary table row / subtle tint
COLOR_PRIMARY_TEXT = "#000000"    # Pure stark black ink
COLOR_SECONDARY_TEXT = "#4A4A4A"  # Deep charcoal body
COLOR_MUTED_LABELS = "#888888"    # Mid-grey architectural overlines
COLOR_BORDERS = "#E0E0E0"         # 1px hairline precision divider rules
COLOR_ACCENT_WHITE = "#000000"    # Inverted stark focus element
COLOR_WHITE = "#FFFFFF"

# Black & White Chart Tokens (Light Mode)
CHART_BG = "rgba(0,0,0,0)"
CHART_LINE = "#000000"
CHART_BAR_PRIMARY = "#000000"
CHART_BAR_SECONDARY = "#CCCCCC"
CHART_BAR_TERTIARY = "#888888"
CHART_GRID = "#F0F0F0"
CHART_BORDER = "#E0E0E0"

# Standard Categories
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
