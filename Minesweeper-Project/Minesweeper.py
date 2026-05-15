import pygame
import random
import sys
import math
import time


# ─────────────────────────────────────────────
#  AI Core: Constraint Satisfaction Logic
# ─────────────────────────────────────────────

class Sentence:
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def known_mines(self):
        if len(self.cells) == self.count:
            return self.cells.copy()
        return set()

    def known_safes(self):
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count


class MinesweeperAI:
    def __init__(self, height=10, width=10):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for s in self.knowledge:
            s.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for s in self.knowledge:
            s.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        count -= 1
                    elif (i, j) not in self.safes:
                        neighbors.add((i, j))

        self.knowledge.append(Sentence(neighbors, count))
        self.infer()

    def infer(self):
        MAX_KNOWLEDGE = 200  # Hard cap — prevents unbounded growth
        changed = True
        while changed:
            changed = False

            # 1. Remove empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]

            # 2. Simple deduction — collect first, then apply
            new_safes, new_mines = set(), set()
            for s in self.knowledge:
                new_safes |= s.known_safes()
                new_mines |= s.known_mines()

            new_safes -= self.safes
            new_mines -= self.mines

            if new_safes:
                changed = True
                for cell in new_safes:
                    self.mark_safe(cell)
            if new_mines:
                changed = True
                for cell in new_mines:
                    self.mark_mine(cell)

            # 3. Subset inference — snapshot before iterating, use frozenset dedup
            if len(self.knowledge) < MAX_KNOWLEDGE:
                existing = frozenset(
                    (frozenset(s.cells), s.count) for s in self.knowledge
                )
                new_sentences = []
                kb = list(self.knowledge)  # snapshot to avoid mutation during loop
                for s1 in kb:
                    for s2 in kb:
                        if s1 is s2 or not s1.cells or not s2.cells:
                            continue
                        if s1.cells.issubset(s2.cells):
                            diff_cells = s2.cells - s1.cells
                            diff_count = s2.count - s1.count
                            key = (frozenset(diff_cells), diff_count)
                            if diff_cells and key not in existing:
                                existing = existing | {key}
                                new_sentences.append(Sentence(diff_cells, diff_count))

                if new_sentences:
                    self.knowledge.extend(new_sentences)
                    changed = True

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self, height, width):
        all_cells = [(r, c) for r in range(height) for c in range(width)]
        random.shuffle(all_cells)
        for cell in all_cells:
            if cell not in self.moves_made and cell not in self.mines:
                return cell
        return None


# ─────────────────────────────────────────────
#  Palette & Design Tokens
# ─────────────────────────────────────────────

# Dark industrial theme
BG_DARK      = (12,  14,  18)    # Near-black background
BG_PANEL     = (18,  22,  30)    # Panel/header
BG_CARD      = (24,  30,  42)    # Card surface
CELL_HIDDEN  = (34,  42,  60)    # Unrevealed cell
CELL_REVEAL  = (220, 225, 235)   # Revealed cell
CELL_SAFE    = (28,  56,  44)    # AI-confirmed safe (subtle green tint)

ACCENT       = (0,   210, 140)   # Teal accent – buttons, highlights
ACCENT_DIM   = (0,   140,  94)   # Dimmed teal
RED_MINE     = (220,  50,  50)   # Mine / danger
RED_DARK     = (140,  20,  20)   # Mine background
YELLOW_FLAG  = (245, 190,  60)   # Flag marker
BLUE_INFO    = ( 80, 160, 240)   # Info color

BORDER_COLOR = (50,   60,  85)
TEXT_BRIGHT  = (220, 225, 240)
TEXT_MID     = (140, 155, 180)
TEXT_DIM     = ( 70,  82, 110)

# Number colors (classic Minesweeper palette, adapted for dark theme)
NUM_COLORS = {
    1: (100, 180, 255),
    2: (80,  210, 130),
    3: (255, 100, 100),
    4: (130, 100, 255),
    5: (255, 160,  60),
    6: ( 60, 210, 200),
    7: (220, 100, 180),
    8: (180, 180, 180),
}


# ─────────────────────────────────────────────
#  Helper: draw rounded rectangle
# ─────────────────────────────────────────────

def draw_rounded_rect(surface, color, rect, radius, border=0, border_color=None):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)


# ─────────────────────────────────────────────
#  Button Component
# ─────────────────────────────────────────────

class Button:
    def __init__(self, rect, label, color=None, text_color=None, font=None):
        self.rect      = pygame.Rect(rect)
        self.label     = label
        self.color     = color or ACCENT
        self.text_color = text_color or BG_DARK
        self.font      = font
        self.hovered   = False

    def draw(self, surface):
        col = tuple(min(255, c + 20) for c in self.color) if self.hovered else self.color
        draw_rounded_rect(surface, col, self.rect, 10)
        if self.font:
            txt = self.font.render(self.label, True, self.text_color)
            surface.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)


# ─────────────────────────────────────────────
#  Main Game Class
# ─────────────────────────────────────────────

class MinesweeperGame:

    # Layout constants
    HEADER_H  = 100
    FOOTER_H  = 90
    CELL_PAD  = 4      # Gap between cells
    WIN_W     = 720
    SIDE_PAD  = 30

    def __init__(self, rows=10, cols=10, mines=15):
        pygame.init()

        self.rows       = rows
        self.cols       = cols
        self.mines_count = mines

        # Dynamic cell size based on grid
        available_w = self.WIN_W - 2 * self.SIDE_PAD
        self.CELL_SIZE = min(52, available_w // cols)
        grid_w = cols * (self.CELL_SIZE + self.CELL_PAD) - self.CELL_PAD
        grid_h = rows * (self.CELL_SIZE + self.CELL_PAD) - self.CELL_PAD

        self.WIN_H = self.HEADER_H + grid_h + self.FOOTER_H + 20
        self.grid_offset_x = (self.WIN_W - grid_w) // 2
        self.grid_offset_y = self.HEADER_H + 10

        # Window
        self.screen = pygame.display.set_mode((self.WIN_W, self.WIN_H))
        pygame.display.set_caption("Minesweeper — AI Agent")

        # Fonts
        self.font_title  = pygame.font.SysFont("Consolas", 24, bold=True)
        self.font_num    = pygame.font.SysFont("Consolas", self.CELL_SIZE // 2 + 2, bold=True)
        self.font_status = pygame.font.SysFont("Consolas", 16)
        self.font_btn    = pygame.font.SysFont("Consolas", 18, bold=True)
        self.font_small  = pygame.font.SysFont("Consolas", 13)
        self.font_counter = pygame.font.SysFont("Consolas", 28, bold=True)

        # Buttons
        btn_y = self.grid_offset_y + grid_h + 18
        self.btn_ai   = Button((self.WIN_W // 2 - 130, btn_y, 120, 46),
                               "AI MOVE", ACCENT, BG_DARK, self.font_btn)
        self.btn_reset = Button((self.WIN_W // 2 + 10, btn_y, 120, 46),
                                "RESET", BORDER_COLOR, TEXT_BRIGHT, self.font_btn)

        # Animation state
        self.anim_cells = {}   # cell -> (start_time, type)  type: 'reveal'|'mine'|'safe'
        self.status_anim = 0.0  # pulse counter
        self.particle_time = 0.0

        self._reset()

    def _reset(self):
        self.mine_positions = set()
        while len(self.mine_positions) < self.mines_count:
            self.mine_positions.add(
                (random.randrange(self.rows), random.randrange(self.cols))
            )

        self.board = [
            [self._count_neighbors(r, c) for c in range(self.cols)]
            for r in range(self.rows)
        ]

        self.revealed     = set()
        self.flags        = set()
        self.game_over    = False
        self.won          = False
        self.ai           = MinesweeperAI(self.rows, self.cols)
        self.status_text  = "Press  AI MOVE  to start"
        self.status_type  = "idle"    # idle | safe | guess | over | win
        self.move_count   = 0
        self.anim_cells   = {}
        self.start_time   = None
        self.end_time     = None

    def _count_neighbors(self, r, c):
        return sum(
            (r + dr, c + dc) in self.mine_positions
            for dr in (-1, 0, 1) for dc in (-1, 0, 1)
            if (dr, dc) != (0, 0)
        )

    # ── Coordinate helpers ────────────────────

    def cell_rect(self, r, c):
        x = self.grid_offset_x + c * (self.CELL_SIZE + self.CELL_PAD)
        y = self.grid_offset_y + r * (self.CELL_SIZE + self.CELL_PAD)
        return pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)

    def pos_to_cell(self, pos):
        """Convert mouse pixel position to (row, col), or None if outside grid."""
        mx, my = pos
        col = (mx - self.grid_offset_x) // (self.CELL_SIZE + self.CELL_PAD)
        row = (my - self.grid_offset_y) // (self.CELL_SIZE + self.CELL_PAD)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            # Make sure we're not in the gap between cells
            rect = self.cell_rect(row, col)
            if rect.collidepoint(pos):
                return (row, col)
        return None

    # ── Game logic ────────────────────────────

    def ai_move(self):
        if self.game_over or self.won:
            return

        if self.start_time is None:
            self.start_time = time.time()

        move = self.ai.make_safe_move()
        is_guess = move is None
        if is_guess:
            move = self.ai.make_random_move(self.rows, self.cols)

        if move is None:
            self.status_text = "No moves available — you win!"
            self.won = True
            self.status_type = "win"
            self.end_time = time.time()
            return

        self.move_count += 1

        if move in self.mine_positions:
            self.revealed.add(move)
            self.game_over = True
            self.status_type = "over"
            self.status_text = f"Move #{self.move_count} — Hit a mine at {move}!"
            self.anim_cells[move] = (time.time(), "mine")
            self.end_time = time.time()
            # Reveal all mines
            for m in self.mine_positions:
                self.anim_cells.setdefault(m, (time.time() + random.uniform(0, 0.4), "mine"))
        else:
            self.revealed.add(move)
            self.ai.add_knowledge(move, self.board[move[0]][move[1]])
            self.anim_cells[move] = (time.time(), "reveal")

            # Mark AI-known safe cells
            for sc in self.ai.safes:
                if sc not in self.revealed:
                    self.anim_cells.setdefault(sc, (time.time(), "safe"))

            # Mark AI-known mine cells as flags
            for mc in self.ai.mines:
                self.flags.add(mc)
                self.anim_cells.setdefault(mc, (time.time(), "flag"))

            if is_guess:
                self.status_type = "guess"
                self.status_text = f"Move #{self.move_count} — Guessing at {move}"
            else:
                self.status_type = "safe"
                self.status_text = f"Move #{self.move_count} — Logical safe move at {move}"

            # Check win
            non_mine = self.rows * self.cols - self.mines_count
            if len(self.revealed) >= non_mine:
                self.won = True
                self.status_type = "win"
                self.status_text = f"AI solved the board in {self.move_count} moves!"
                self.end_time = time.time()

    def manual_move(self, cell):
        """Player clicks a cell manually — left click to reveal."""
        if self.game_over or self.won:
            return
        if cell in self.revealed or cell in self.flags:
            return

        if self.start_time is None:
            self.start_time = time.time()

        self.move_count += 1

        if cell in self.mine_positions:
            self.revealed.add(cell)
            self.game_over = True
            self.status_type = "over"
            self.status_text = f"Move #{self.move_count} — You hit a mine at {cell}!"
            self.anim_cells[cell] = (time.time(), "mine")
            self.end_time = time.time()
            for m in self.mine_positions:
                self.anim_cells.setdefault(m, (time.time() + random.uniform(0, 0.4), "mine"))
        else:
            self.revealed.add(cell)
            self.ai.add_knowledge(cell, self.board[cell[0]][cell[1]])
            self.anim_cells[cell] = (time.time(), "reveal")
            for sc in self.ai.safes:
                if sc not in self.revealed:
                    self.anim_cells.setdefault(sc, (time.time(), "safe"))
            for mc in self.ai.mines:
                self.flags.add(mc)
                self.anim_cells.setdefault(mc, (time.time(), "flag"))

            self.status_type = "safe"
            self.status_text = f"Move #{self.move_count} — You revealed {cell}"

            non_mine = self.rows * self.cols - self.mines_count
            if len(self.revealed) >= non_mine:
                self.won = True
                self.status_type = "win"
                self.status_text = f"You solved the board in {self.move_count} moves!"
                self.end_time = time.time()

    def toggle_flag(self, cell):
        """Right-click to place/remove a flag manually."""
        if self.game_over or self.won:
            return
        if cell in self.revealed:
            return
        if cell in self.ai.mines:
            return  # AI-confirmed mines can't be un-flagged
        if cell in self.flags:
            self.flags.remove(cell)
            self.status_text = f"Flag removed at {cell}"
        else:
            self.flags.add(cell)
            self.status_text = f"Flag placed at {cell}"
        self.status_type = "idle"

    # ── Drawing ───────────────────────────────

    def draw(self):
        now = time.time()
        self.screen.fill(BG_DARK)

        self._draw_header(now)
        self._draw_grid(now)
        self._draw_footer(now)

        mouse = pygame.mouse.get_pos()
        self.btn_ai.update(mouse)
        self.btn_reset.update(mouse)
        self.btn_ai.draw(self.screen)
        self.btn_reset.draw(self.screen)

        pygame.display.flip()

    def _draw_header(self, now):
        # Header panel
        draw_rounded_rect(self.screen, BG_PANEL,
                          (0, 0, self.WIN_W, self.HEADER_H), 0)
        pygame.draw.line(self.screen, BORDER_COLOR,
                         (0, self.HEADER_H - 1), (self.WIN_W, self.HEADER_H - 1), 1)

        # Title
        title = self.font_title.render("MINESWEEPER  ·  AI AGENT", True, TEXT_BRIGHT)
        self.screen.blit(title, (self.SIDE_PAD, 16))

        # Counters row
        elapsed = ""
        if self.start_time:
            t = (self.end_time or now) - self.start_time
            elapsed = f"{t:.1f}s"

        flags_used  = len(self.flags)
        mines_left  = self.mines_count - flags_used
        revealed_pct = (len(self.revealed) / (self.rows * self.cols)) * 100

        self._draw_stat(self.SIDE_PAD,       56, "mine",   str(mines_left),       "mines left")
        self._draw_stat(self.SIDE_PAD + 160, 56, "flag",   str(flags_used),       "flagged")
        self._draw_stat(self.SIDE_PAD + 310, 56, "time",   elapsed or "—",        "time")
        self._draw_stat(self.SIDE_PAD + 460, 56, "reveal", f"{revealed_pct:.0f}%","revealed")

    def _draw_icon(self, x, y, kind):
        """Draw a small pygame shape instead of an emoji."""
        cx, cy = x + 8, y + 8
        if kind == "mine":
            pygame.draw.circle(self.screen, RED_MINE, (cx, cy), 6)
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                x1 = cx + int(5 * math.cos(rad))
                y1 = cy + int(5 * math.sin(rad))
                x2 = cx + int(9 * math.cos(rad))
                y2 = cy + int(9 * math.sin(rad))
                pygame.draw.line(self.screen, RED_MINE, (x1, y1), (x2, y2), 2)
        elif kind == "flag":
            pygame.draw.line(self.screen, TEXT_MID, (cx - 2, cy + 7), (cx - 2, cy - 7), 2)
            pts = [(cx - 2, cy - 7), (cx + 8, cy - 2), (cx - 2, cy + 2)]
            pygame.draw.polygon(self.screen, YELLOW_FLAG, pts)
        elif kind == "time":
            pygame.draw.circle(self.screen, TEXT_MID, (cx, cy), 7, 2)
            pygame.draw.line(self.screen, ACCENT, (cx, cy), (cx, cy - 4), 2)
            pygame.draw.line(self.screen, ACCENT, (cx, cy), (cx + 3, cy + 2), 2)
        elif kind == "reveal":
            pygame.draw.circle(self.screen, BLUE_INFO, (cx, cy), 7, 2)
            pygame.draw.line(self.screen, BLUE_INFO, (cx, cy - 3), (cx, cy + 3), 2)
            pygame.draw.line(self.screen, BLUE_INFO, (cx - 3, cy), (cx + 3, cy), 2)

    def _draw_stat(self, x, y, kind, value, label):
        self._draw_icon(x, y, kind)
        val = self.font_counter.render(value, True, TEXT_BRIGHT)
        lbl = self.font_small.render(label, True, TEXT_DIM)
        self.screen.blit(val, (x + 22, y - 2))
        self.screen.blit(lbl, (x + 22, y + 26))

    def _draw_grid(self, now):
        for r in range(self.rows):
            for c in range(self.cols):
                rect = self.cell_rect(r, c)
                cell = (r, c)
                anim_info = self.anim_cells.get(cell)
                anim_age  = (now - anim_info[0]) if anim_info else 999
                anim_type = anim_info[1] if anim_info else None

                # ── Determine cell state ──
                is_revealed = cell in self.revealed
                is_mine     = cell in self.mine_positions
                is_flag     = cell in self.flags
                is_ai_safe  = cell in self.ai.safes and not is_revealed

                # ── Cell background ──
                if is_revealed and is_mine:
                    # Exploded mine
                    t = min(1.0, anim_age / 0.3)
                    col = self._lerp_color(CELL_HIDDEN, RED_DARK, t)
                    draw_rounded_rect(self.screen, col, rect, 6)
                    # Pulsing border
                    pulse = abs(math.sin(now * 8)) * 180 + 75
                    pygame.draw.rect(self.screen, (int(pulse), 30, 30), rect, 2, border_radius=6)

                elif is_revealed:
                    # Smooth reveal animation
                    t = min(1.0, anim_age / 0.15)
                    col = self._lerp_color(CELL_HIDDEN, CELL_REVEAL, t)
                    draw_rounded_rect(self.screen, col, rect, 6)

                elif is_flag:
                    # AI-flagged mine
                    t = min(1.0, anim_age / 0.2) if anim_type == "flag" else 1.0
                    col = self._lerp_color(CELL_HIDDEN, (50, 28, 15), t)
                    draw_rounded_rect(self.screen, col, rect, 6)
                    pygame.draw.rect(self.screen, (YELLOW_FLAG[0], YELLOW_FLAG[1], YELLOW_FLAG[2], 150),
                                     rect, 1, border_radius=6)

                elif is_ai_safe and not self.game_over:
                    # Subtle safe hint
                    t = min(1.0, anim_age / 0.3) if anim_type == "safe" else 1.0
                    col = self._lerp_color(CELL_HIDDEN, CELL_SAFE, t * 0.6)
                    draw_rounded_rect(self.screen, col, rect, 6)
                    pygame.draw.rect(self.screen, (*ACCENT, 60), rect, 1, border_radius=6)

                else:
                    draw_rounded_rect(self.screen, CELL_HIDDEN, rect, 6,
                                      border=1, border_color=BORDER_COLOR)

                # ── Cell content ──
                if is_revealed and not is_mine:
                    val = self.board[r][c]
                    if val > 0:
                        color = NUM_COLORS.get(val, TEXT_BRIGHT)
                        txt = self.font_num.render(str(val), True, color)
                        self.screen.blit(txt, txt.get_rect(center=rect.center))

                elif is_revealed and is_mine:
                    # Draw mine symbol
                    cx, cy = rect.centerx, rect.centery
                    r_size = self.CELL_SIZE // 4
                    pygame.draw.circle(self.screen, RED_MINE, (cx, cy), r_size)
                    # Spike lines
                    for angle in range(0, 360, 45):
                        rad = math.radians(angle)
                        x1 = cx + int(r_size * 0.7 * math.cos(rad))
                        y1 = cy + int(r_size * 0.7 * math.sin(rad))
                        x2 = cx + int((r_size + 5) * math.cos(rad))
                        y2 = cy + int((r_size + 5) * math.sin(rad))
                        pygame.draw.line(self.screen, RED_MINE, (x1, y1), (x2, y2), 2)

                elif is_flag and not is_revealed:
                    # Draw flag symbol
                    cx, cy = rect.centerx, rect.centery
                    # Flag pole
                    pygame.draw.line(self.screen, TEXT_MID,
                                     (cx - 3, cy + 8), (cx - 3, cy - 9), 2)
                    # Flag shape (triangle)
                    pts = [(cx - 3, cy - 9), (cx + 9, cy - 4), (cx - 3, cy + 1)]
                    pygame.draw.polygon(self.screen, YELLOW_FLAG, pts)

                elif not is_revealed and not is_flag:
                    # Subtle corner dots on unrevealed
                    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                        px = rect.centerx + dx * (self.CELL_SIZE // 4)
                        py = rect.centery + dy * (self.CELL_SIZE // 4)
                        pygame.draw.circle(self.screen, BORDER_COLOR, (px, py), 1)

    def _draw_footer(self, now):
        # Status bar
        status_colors = {
            "idle" : TEXT_DIM,
            "safe" : ACCENT,
            "guess": YELLOW_FLAG,
            "over" : RED_MINE,
            "win"  : ACCENT,
        }
        sc = status_colors.get(self.status_type, TEXT_MID)

        # Pulse effect on status text
        if self.status_type in ("over", "win"):
            pulse = abs(math.sin(now * 3))
            sc = tuple(int(sc[i] * (0.6 + 0.4 * pulse)) for i in range(3))

        # Status indicator dot
        dot_y = self.btn_ai.rect.centery
        dot_x = self.SIDE_PAD
        pygame.draw.circle(self.screen, sc, (dot_x, dot_y), 5)

        # Status text (clipped to left area)
        status = self.font_status.render(self.status_text, True, sc)
        self.screen.blit(status, (dot_x + 14, dot_y - 9))

    @staticmethod
    def _lerp_color(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    # ── Main loop ─────────────────────────────

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over and not self.won:
                        self.ai_move()
                    if event.key == pygame.K_r:
                        self._reset()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_ai.is_clicked(event.pos):
                        self.ai_move()
                    elif self.btn_reset.is_clicked(event.pos):
                        self._reset()
                    else:
                        cell = self.pos_to_cell(event.pos)
                        if cell:
                            if event.button == 1:    # Left click → reveal
                                self.manual_move(cell)
                            elif event.button == 3:  # Right click → flag
                                self.toggle_flag(cell)

            clock.tick(60)


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Adjust grid size / mine count here
    MinesweeperGame(rows=10, cols=10, mines=15).run()