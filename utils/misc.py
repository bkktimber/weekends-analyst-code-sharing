from pathlib import Path
from matplotlib import font_manager


def add_font(fontname: str = "Anakotmai") -> None:
    """
    Add font to Matplotlib Cache
    Input: Target Font name. Target font must exist in /fonts
    Output: None
    """

    path = Path(f"fonts/{fontname}")
    font_files = font_manager.findSystemFonts(str(path))
    for f in font_files:
        font_manager.fontManager.addfont(f)
