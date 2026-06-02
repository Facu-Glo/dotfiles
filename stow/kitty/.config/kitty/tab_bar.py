# pyright: reportMissingImports=false
import subprocess
from kitty.boss import get_boss
from kitty.fast_data_types import Screen
from kitty.tab_bar import (
    DrawData,
    ExtraData,
    TabBarData,
    TabAccessor,
    as_rgb,
    draw_tab_with_separator,
)

# -------------------------
# Git: contar cambios
# -------------------------
def get_git_changes(cwd: str) -> list[tuple[str, int]]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=1,
        )
        if result.returncode != 0:
            return []

        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=1,
        )
        if status_result.returncode != 0:
            return []

        lines = [line.rstrip("\n") for line in status_result.stdout.splitlines() if line]
        if not lines:
            return []

        staged     = sum(1 for l in lines if l[0] not in " ?")
        modified   = sum((l[0] == "M") + (l[1] == "M") for l in lines if not l.startswith("??"))
        deleted    = sum((l[0] == "D") + (l[1] == "D") for l in lines if not l.startswith("??"))
        untracked  = sum(1 for l in lines if l.startswith("??"))

        result_list = []
        if staged > 0:
            result_list.append((f" {staged}", 0x96E364))
        if modified > 0:
            result_list.append((f" {modified}", 0xE3B419))
        if deleted > 0:
            result_list.append((f" {deleted}", 0xE33C19))
        if untracked > 0:
            result_list.append((f" {untracked}", 0xD795F4))

        return result_list

    except Exception:
        return []

# -------------------------
# Dibujar parte izquierda (icono + separador + título)
# -------------------------
def _draw_left_status(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    active_id = get_boss().active_tab.id
    active_tab = TabAccessor(active_id)

    old_fg = screen.cursor.fg
    old_bg = screen.cursor.bg

    # Ícono en la primera tab
    if index == 1:
        title = active_tab.active_oldest_exe
        screen.cursor.italic = False
        screen.cursor.bold = True
        screen.cursor.fg = as_rgb(0x81C8BE)
        screen.cursor.bg = as_rgb(int(draw_data.inactive_bg))
        # screen.cursor.bg = as_rgb(0x232634)
        # cell = " "
        # cell = f"  {title}"
        cell = f"  {title}"
        screen.draw(cell)

    # Separador izquierdo
    if tab.is_active:
        screen.cursor.fg = as_rgb(int(draw_data.active_bg))
        screen.cursor.bg = as_rgb(int(draw_data.inactive_bg))
        screen.draw(" ▐█")
    elif extra_data.prev_tab is None or extra_data.prev_tab.tab_id != active_id:
        screen.cursor.bg = as_rgb(int(draw_data.inactive_bg))
        screen.cursor.fg = as_rgb(0x626880)
        screen.draw(" │ ")

    screen.cursor.fg = old_fg
    screen.cursor.bg = old_bg

    # Título
    return draw_tab_with_separator(
        draw_data,
        screen,
        tab,
        before,
        max_title_length,
        index,
        is_last,
        extra_data,
    )

# -------------------------
# Dibujar parte derecha (separador + estado git)
# -------------------------
def _draw_right_status(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    is_last: bool,
) -> int:
    active_id = get_boss().active_tab.id
    active_tab = TabAccessor(active_id)

    # Separador derecho
    if tab.is_active:
        screen.cursor.fg = as_rgb(int(draw_data.active_bg))
        if not is_last:
            bg_color = int(draw_data.inactive_bg)
        else:
            bg_color = int(draw_data.default_bg)
        screen.cursor.bg = as_rgb(bg_color)
        screen.draw("█▌ ")
    elif is_last:
        screen.cursor.fg = as_rgb(int(draw_data.inactive_bg))
        screen.cursor.bg = as_rgb(int(draw_data.default_bg))
        screen.draw("█▌ ")

    # Git status solo en la última tab
    if is_last:
        cwd = active_tab.active_oldest_wd or ""
        changes = get_git_changes(cwd)
        if changes:
            git_text = " ".join([t[0] for t in changes])
            screen.cursor.x = max(0, screen.columns - len(git_text) - 1)
            for text, color in changes:
                screen.cursor.fg = as_rgb(color)
                screen.cursor.bg = as_rgb(int(draw_data.default_bg))
                screen.draw(text + " ")

    return screen.cursor.x

# -------------------------
# Función principal
# -------------------------
def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    _draw_left_status(draw_data, screen, tab, before, max_title_length, index, is_last, extra_data)
    return _draw_right_status(draw_data, screen, tab, is_last)
