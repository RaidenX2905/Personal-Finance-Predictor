"""Black and White Monochromatic Design Tokens and Theme Configuration."""

# Pure Monochromatic Palette
COLOR_BG = "#000000"              # Deep Pitch Black canvas
COLOR_SURFACE = "#0A0A0A"         # Slightly elevated dark plane
COLOR_SURFACE_ALT = "#121212"     # Subtle card/row tint
COLOR_PRIMARY_TEXT = "#F4F4F4"    # Pure stark white / off-white text
COLOR_SECONDARY_TEXT = "#A0A0A0"  # Neutral mid-grey body
COLOR_MUTED_LABELS = "#666666"    # Subtle technical dark grey labels
COLOR_BORDERS = "#242424"         # 1px hairline precision architectural borders
COLOR_ACCENT_WHITE = "#FFFFFF"    # Maximum contrast focus element
COLOR_WHITE = "#FFFFFF"

# Black & White Chart Tokens
CHART_BG = "rgba(0,0,0,0)"
CHART_LINE = "#FFFFFF"
CHART_BAR_PRIMARY = "#FFFFFF"
CHART_BAR_SECONDARY = "#333333"
CHART_BAR_TERTIARY = "#666666"
CHART_GRID = "#1A1A1A"
CHART_BORDER = "#242424"

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
