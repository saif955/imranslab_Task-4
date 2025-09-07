from manim import *
import numpy as np

# Theme
COLOR_BG = "#000000"
COLOR_METAL_DARK = "#1a1a1a"
COLOR_METAL = "#9e9e9e"
COLOR_OUTLINE = "#ffffff"
COLOR_ACCENT = "#00f7ff"
COLOR_THRUST = "#ff7a00"
COLOR_THRUST_CORE = "#ffd000"
COLOR_GROUND = "#0b0b0b"


class StarshipLiftoff(Scene):
    def construct(self):
        # Background
        bg = Rectangle(width=16, height=9).set_fill(COLOR_BG, opacity=1).set_stroke(width=0)
        self.add(bg)

        # Simple ground/pad
        ground = Rectangle(width=16, height=1.2).set_fill(COLOR_GROUND, 1).set_stroke(width=0)
        ground.to_edge(DOWN)
        self.add(ground)

        # Rocket proportions
        body_height = 5.0
        body_width = 1.2
        nose_height = 1.2
        fin_span = 2.6
        fin_height = 1.0

        # Body
        body = RoundedRectangle(
            corner_radius=0.18,
            width=body_width,
            height=body_height,
        )
        body.set_fill(color=COLOR_METAL, opacity=1)
        body.set_stroke(color=COLOR_OUTLINE, width=2, opacity=1)

        # Nose cone
        nose = ArcPolygon(
            LEFT * (body_width / 2) + UP * (body_height / 2),
            UP * (body_height / 2 + nose_height),
            RIGHT * (body_width / 2) + UP * (body_height / 2),
            stroke_color=COLOR_OUTLINE,
            stroke_width=2,
            fill_color=COLOR_METAL,
            fill_opacity=1,
        )

        # Windows
        window1 = Circle(radius=0.12).set_fill(COLOR_ACCENT, opacity=1).set_stroke(COLOR_OUTLINE, 1)
        window2 = Circle(radius=0.10).set_fill(COLOR_ACCENT, opacity=1).set_stroke(COLOR_OUTLINE, 1)
        window3 = Circle(radius=0.10).set_fill(COLOR_ACCENT, opacity=1).set_stroke(COLOR_OUTLINE, 1)
        window1.move_to(UP * 1.1)
        window2.move_to(UP * 0.4)
        window3.move_to(DOWN * 0.3)

        # Fins
        left_fin = Polygon(
            LEFT * (body_width / 2),
            LEFT * (body_width / 2 + fin_span * 0.35) + DOWN * (fin_height * 0.55),
            LEFT * (body_width / 2) + DOWN * (fin_height),
        )
        right_fin = left_fin.copy().apply_matrix(np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]]))
        left_fin.set_fill(color=COLOR_METAL, opacity=1).set_stroke(COLOR_OUTLINE, 2)
        right_fin.set_fill(color=COLOR_METAL, opacity=1).set_stroke(COLOR_OUTLINE, 2)

        # Engine bells
        bell_radius = 0.18
        engine_offsets = [-0.35, 0.0, 0.35]
        bells = VGroup(
            *[
                Circle(radius=bell_radius)
                .set_fill(COLOR_METAL_DARK, opacity=1)
                .set_stroke(COLOR_OUTLINE, 2)
                .move_to(DOWN * (body_height / 2 + 0.15) + RIGHT * x)
                for x in engine_offsets
            ]
        )

        # Thrust flames
        def make_flame(x_offset: float, peak: float = 1.3, base: float = 0.35) -> VMobject:
            flame = VMobject(stroke_width=0)
            flame.set_fill(color=COLOR_THRUST, opacity=0.85)
            p0 = DOWN * (body_height / 2 + 0.15) + RIGHT * x_offset + DOWN * 0.05 + LEFT * base
            p1 = p0 + DOWN * peak + RIGHT * base
            p2 = DOWN * (body_height / 2 + 0.15) + RIGHT * x_offset + DOWN * 0.05 + RIGHT * base
            p3 = p2 + DOWN * peak + LEFT * base
            flame.set_points_smoothly([p0, p1, p2, p3, p0])
            core = flame.copy().set_fill(COLOR_THRUST_CORE, opacity=0.75).scale(0.6, about_point=p0)
            return VGroup(flame, core)

        flames = VGroup(*[make_flame(x) for x in engine_offsets])
        flames.set_opacity(0)

        # Final rocket group
        rocket = VGroup(body, nose, left_fin, right_fin, window1, window2, window3, bells)

        # Position rocket on pad center
        rocket.move_to(ground.get_top() + UP * (body_height / 2))
        self.add(rocket)
        self.add(flames)

        # Rocket is already visible immediately

        # Countdown overlay before ignition
        countdown = Text("3", font_size=96, color=COLOR_OUTLINE)
        countdown_bg = Rectangle(width=4.2, height=2.2).set_fill(COLOR_BG, opacity=0.5).set_stroke(width=0)
        countdown_group = VGroup(countdown_bg, countdown).move_to(ORIGIN + UP * 1.5)
        self.play(FadeIn(countdown_group), run_time=0.2)
        self.wait(0.2)
        self.play(Transform(countdown, Text("2", font_size=96, color=COLOR_OUTLINE)), run_time=0.25)
        self.play(Transform(countdown, Text("1", font_size=96, color=COLOR_OUTLINE)), run_time=0.25)
        self.play(Transform(countdown, Text("0", font_size=96, color=COLOR_OUTLINE)), run_time=0.25)
        self.play(FadeOut(countdown_group), run_time=0.2)

        # Ignite engines
        self.play(*[flame.animate.set_opacity(1) for flame in flames], run_time=0.25)

        # Lift-off straight up until out of frame
        self.play(
            rocket.animate.shift(4.5 * UP),
            flames.animate.shift(4.5 * UP),
            rate_func=rate_functions.ease_in_sine,
            run_time=1.8,
        )

        # Exit fade
        self.play(FadeOut(VGroup(rocket, flames)), run_time=0.4)


