from manim import *

class LogoOutro(Scene):
    def construct(self):
        # Background like intro.py
        try:
            self.set_background_color(BLACK)
        except Exception:
            self.camera.background_color = BLACK

        # Load SVG from assets folder
        svg_path = "assets/logo.svg"
        
        try:
            # Load SVG; start with transparent fill and visible white stroke
            logo = SVGMobject(svg_path)
            logo.set_fill(WHITE, opacity=0.0)
            logo.set_stroke(WHITE, width=3)
            logo.center().scale(1.25)

            parts = [m for m in logo.family_members_with_points()]

            # Tracing pass (same as intro)
            tracer = VGroup(*[p.copy().set_stroke(WHITE, width=6) for p in parts])
            self.play(
                LaggedStart(*[ShowPassingFlash(t, time_width=0.25) for t in tracer],
                            lag_ratio=0.06),
                run_time=2.2,
            )

            # Solidify outline
            for p in parts:
                p.set_fill(opacity=0.0).set_stroke(WHITE, width=3)
            self.play(LaggedStart(*[Create(p) for p in parts], lag_ratio=0.02), run_time=1.0)

            # Fill in white
            self.play(logo.animate.set_fill(WHITE, opacity=1.0), run_time=0.7, rate_func=smooth)

            # Reduce stroke for clean look
            self.play(logo.animate.set_stroke(width=0), run_time=0.4)
            
        except Exception:
            # Fallback to simple geometric logo if SVG fails
            logo = Polygon(
                UP * 1.5,
                RIGHT * 1.0,
                DOWN * 1.5,
                LEFT * 1.0,
            )
            logo.set_fill(WHITE, opacity=0.0)
            logo.set_stroke(WHITE, width=3)
            logo.center().scale(1.25)
            self.play(Create(logo), run_time=2.2)
            self.play(logo.animate.set_fill(WHITE, opacity=1.0), run_time=0.7, rate_func=smooth)
            self.play(logo.animate.set_stroke(width=0), run_time=0.4)

        self.wait(0.5)

        # Outro text with gradient for a small creative touch
        outro_text = Text("Thank you for watching!", font_size=48)
        outro_text.set_color_by_gradient(BLUE, PURPLE)
        outro_text.next_to(logo, DOWN, buff=0.5)
        self.play(FadeIn(outro_text), run_time=0.8)

        self.wait(1.2)

        # Fade out logo and text
        self.play(FadeOut(VGroup(logo, outro_text)), run_time=1.2)
        self.wait(0.3)
