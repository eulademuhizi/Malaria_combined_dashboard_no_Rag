# utils.py - Shared constants and utilities to eliminate duplication

# Month names - used across multiple files (REMOVED from chart_visualizations.py)
MONTH_NAMES = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

# Common utility functions
def get_month_name(month: int) -> str:
    """Convert month number to name - centralized function"""
    return MONTH_NAMES.get(month, str(month))

def format_number_with_commas(num) -> str:
    """Format number with commas for display"""
    if isinstance(num, (int, float)):
        return f"{num:,.0f}"
    return str(num)

def calculate_percentage_change(current: float, previous: float) -> float:
    """Calculate percentage change between two values"""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100