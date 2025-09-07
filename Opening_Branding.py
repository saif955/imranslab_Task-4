from manim import *
from pathlib import Path
import numpy as np

# === Branding Assets ===
BRAND_IMAGE_PATH = Path("assets/branding_image.png")

# === Colors (Neon on Dark) ===
COLOR_TEXT = "#00f7ff"
COLOR_TEXT_ACCENT = "#39ff14"
COLOR_STROKE = "#ff00ea"
COLOR_BG = "#000000"


class OpeningBranding(Scene):
    def construct(self):
        # Background gradient rectangle
        bg = Rectangle(width=14, height=8)
        bg.set_fill(color=COLOR_BG, opacity=1)
        bg.set_stroke(width=0)
        self.add(bg)

        # Try to load logo or fallback text
        visual = None
        if BRAND_IMAGE_PATH.exists():
            try:
                visual = ImageMobject(str(BRAND_IMAGE_PATH)).set_height(3.0)
            except Exception:
                visual = None

        if visual is None:
            visual = Text("Imran's Lab", weight=BOLD, color=COLOR_TEXT).scale(1.2)

        # Rectangle frame around the logo
        rect = SurroundingRectangle(visual, buff=0.25, corner_radius=0.2)
        rect.set_stroke(color=COLOR_STROKE, width=2, opacity=1)
        glow_rect = rect.copy().set_stroke(color=COLOR_STROKE, width=14, opacity=0.25)
        group_main = Group(glow_rect, visual, rect)

        # Tagline text
        tagline = Text(
            "We Are Experts in Design, App, and Development",
            font_size=28,
            color=COLOR_TEXT_ACCENT
        )
        tagline.next_to(group_main, DOWN, buff=0.4)

        # === Animations ===
        # 0–2s: Smooth neon entrance
        self.play(
            LaggedStart(
                FadeIn(visual, scale=0.85, shift=0.3 * DOWN),
                Create(rect),
                lag_ratio=0.2,
                run_time=1.6,
            )
        )
        self.play(glow_rect.animate.set_stroke(opacity=0.3, width=14), run_time=0.6)
        self.play(Write(tagline), run_time=1.2)

        # 2–6s: Neon pulse on glow + gentle scale
        def animate_glow(mobj, alpha):
            mobj.set_stroke(
                width=14 + 6 * np.sin(alpha * PI),
                opacity=0.20 + 0.15 * np.sin(alpha * PI),
            )
        self.play(
            AnimationGroup(
                UpdateFromAlphaFunc(glow_rect, animate_glow),
                group_main.animate.scale(1.04),
                rate_func=there_and_back,
                run_time=2.0,
            )
        )

        # 6–9s: Gentle upward drift + slight parallax tilt
        self.play(
            AnimationGroup(
                group_main.animate.shift(0.35 * UP).rotate(0.02),
                tagline.animate.shift(0.25 * UP),
                run_time=3.0,
            )
        )

        # 9–10s: Outro pop + neon flicker + fade
        self.play(group_main.animate.scale(1.08), run_time=0.4, rate_func=there_and_back)
        self.play(
            AnimationGroup(
                glow_rect.animate.set_stroke(opacity=0.15),
                tagline.animate.set_opacity(0.7),
                run_time=0.25,
            )
        )
        self.play(FadeOut(Group(group_main, tagline, bg)), run_time=0.8)
