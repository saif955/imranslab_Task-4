from manim import *
from pathlib import Path
import numpy as np

# Assets

# Theme
COLOR_BG = "#000000"
COLOR_METAL_DARK = "#1a1a1a"
COLOR_METAL = "#9e9e9e"
COLOR_OUTLINE = "#ffffff"
COLOR_ACCENT = "#00f7ff"
COLOR_THRUST = "#ff7a00"
COLOR_THRUST_CORE = "#ffd000"

# Space colors
COLOR_STAR_NEAR = "#ffffff"
COLOR_STAR_MID = "#cfd8ff"
COLOR_STAR_FAR = "#9aa4ff"
COLOR_EARTH_OCEAN = "#0b3d91"
COLOR_EARTH_OUTLINE = "#1e90ff"


class StarshipBuild(MovingCameraScene):
    def construct(self):
        # Background
        bg = Rectangle(width=16, height=9).set_fill(COLOR_BG, opacity=1).set_stroke(width=0)
        self.add(bg)
        # Slight zoom-out to avoid a too-tight framing
        self.camera.frame.scale(1.15)

        # Parallax star layers
        def make_star_layer(count: int, color: str, radius_range=(0.01, 0.03), seed: int = 0) -> VGroup:
            rng = np.random.default_rng(seed)
            stars = VGroup()
            for _ in range(count):
                x = rng.uniform(-7.8, 7.8)
                y = rng.uniform(-4.4, 4.4)
                r = rng.uniform(radius_range[0], radius_range[1])
                star = Dot(point=np.array([x, y, 0.0]), radius=r, color=color)
                stars.add(star)
            return stars

        stars_far = make_star_layer(120, COLOR_STAR_FAR, (0.006, 0.014), seed=1)
        stars_mid = make_star_layer(90, COLOR_STAR_MID, (0.008, 0.018), seed=2)
        stars_near = make_star_layer(70, COLOR_STAR_NEAR, (0.010, 0.024), seed=3)
        self.play(LaggedStart(FadeIn(stars_far, shift=0.1 * DOWN), FadeIn(stars_mid, shift=0.15 * DOWN), FadeIn(stars_near, shift=0.2 * DOWN), lag_ratio=0.2, run_time=0.8))

        # Earth (smaller for 1080p)
        earth_radius = 1.4
        earth = Circle(radius=earth_radius).set_fill(COLOR_EARTH_OCEAN, opacity=1).set_stroke(COLOR_EARTH_OUTLINE, 2)
        earth.move_to(DOWN * 1.8 + LEFT * 2.5)
        self.play(FadeIn(earth, shift=0.3 * DOWN), run_time=0.6)

        # Define orbit geometry (start directly in orbit)
        orbit_radius = earth_radius + 1.0
        start_angle = -PI / 2 + 0.2

        # Rocket proportions (smaller for 1080p)
        body_height = 3.2
        body_width = 0.8
        nose_height = 0.8
        fin_span = 1.8
        fin_height = 0.7

        # Body
        body = RoundedRectangle(
            corner_radius=0.18,
            width=body_width,
            height=body_height,
        )
        body.set_fill(color=COLOR_METAL, opacity=1)
        body.set_stroke(color=COLOR_OUTLINE, width=2, opacity=1)

        # Nose cone (semi-elliptical cap)
        nose_top = UP * (body_height / 2 + nose_height / 2)
        nose = ArcPolygon(
            LEFT * (body_width / 2) + UP * (body_height / 2),
            UP * (body_height / 2 + nose_height),
            RIGHT * (body_width / 2) + UP * (body_height / 2),
            stroke_color=COLOR_OUTLINE,
            stroke_width=2,
            fill_color=COLOR_METAL,
            fill_opacity=1,
        )

        # Window portholes (scaled down)
        window1 = Circle(radius=0.08).set_fill(COLOR_ACCENT, opacity=1).set_stroke(COLOR_OUTLINE, 1)
        window2 = Circle(radius=0.07).set_fill(COLOR_ACCENT, opacity=1).set_stroke(COLOR_OUTLINE, 1)
        window3 = Circle(radius=0.07).set_fill(COLOR_ACCENT, opacity=1).set_stroke(COLOR_OUTLINE, 1)
        window1.move_to(UP * 0.7)
        window2.move_to(UP * 0.25)
        window3.move_to(DOWN * 0.2)

        # Fins (left and right)
        left_fin = Polygon(
            LEFT * (body_width / 2),
            LEFT * (body_width / 2 + fin_span * 0.35) + DOWN * (fin_height * 0.55),
            LEFT * (body_width / 2) + DOWN * (fin_height),
        )
        right_fin = left_fin.copy().apply_matrix(np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]]))
        left_fin.set_fill(color=COLOR_METAL, opacity=1).set_stroke(COLOR_OUTLINE, 2)
        right_fin.set_fill(color=COLOR_METAL, opacity=1).set_stroke(COLOR_OUTLINE, 2)

        # Engines (three bells, scaled down)
        bell_radius = 0.12
        engine_offsets = [-0.25, 0.0, 0.25]
        bells = VGroup(
            *[
                Circle(radius=bell_radius)
                .set_fill(COLOR_METAL_DARK, opacity=1)
                .set_stroke(COLOR_OUTLINE, 2)
                .move_to(DOWN * (body_height / 2 + 0.15) + RIGHT * x)
                for x in engine_offsets
            ]
        )

        # Thrust flames (stylized Bezier shapes)
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

        # Flat 2D rocket group (no glow)
        rocket = VGroup(body, nose, left_fin, right_fin, window1, window2, window3, bells)

        # Place rocket at the start of orbit and orient tangentially
        orbit_center = earth.get_center()
        start_point = orbit_center + orbit_radius * np.array([np.cos(start_angle), np.sin(start_angle), 0.0])
        rocket.move_to(start_point)
        tangent_angle = start_angle + PI / 2
        rocket.rotate(tangent_angle - PI / 2)
        self.add(rocket)
        self.add(flames)
        flames.set_opacity(0)

        # HUD counters (altitude km, velocity km/s, mission time s)
        altitude = ValueTracker(0.0)
        velocity = ValueTracker(0.0)
        mission_t = ValueTracker(0.0)

        hud_bg = RoundedRectangle(corner_radius=0.12, width=5.8, height=1.4).set_fill(COLOR_BG, 0.5).set_stroke(COLOR_OUTLINE, 1)
        hud_bg.to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.3)

        label_alt = Text("ALT", font_size=24)
        label_vel = Text("VEL", font_size=24)
        label_tim = Text("T+", font_size=24)
        label_alt.next_to(hud_bg.get_left(), RIGHT, buff=0.25)
        label_vel.next_to(label_alt, RIGHT, buff=0.8)
        label_tim.next_to(label_vel, RIGHT, buff=0.8)

        alt_num = Text("0 km", font_size=28)
        vel_num = Text("0.00 km/s", font_size=28)
        tim_num = Text("0.0 s", font_size=28)
        alt_num.next_to(label_alt, DOWN, buff=0.12)
        vel_num.next_to(label_vel, DOWN, buff=0.12)
        tim_num.next_to(label_tim, DOWN, buff=0.12)

        def update_alt(m: Text):
            m.set_text(f"{int(altitude.get_value()):,} km")
            m.next_to(label_alt, DOWN, buff=0.12)

        def update_vel(m: Text):
            m.set_text(f"{velocity.get_value():.2f} km/s")
            m.next_to(label_vel, DOWN, buff=0.12)

        def update_time(m: Text):
            m.set_text(f"{mission_t.get_value():.1f} s")
            m.next_to(label_tim, DOWN, buff=0.12)

        alt_num.add_updater(update_alt)
        vel_num.add_updater(update_vel)
        tim_num.add_updater(update_time)

        status_launch = Text("LAUNCH", font_size=22, color=COLOR_ACCENT)
        status_orbit = Text("ORBIT", font_size=22, color=COLOR_ACCENT)
        status_launch.next_to(hud_bg.get_right(), LEFT, buff=0.25).shift(UP * 0.2)
        status_orbit.move_to(status_launch)
        status_orbit.set_opacity(0)

        # Show ORBIT status from the start
        status_launch.set_opacity(0)
        status_orbit.set_opacity(1)
        hud = VGroup(hud_bg, label_alt, label_vel, label_tim, alt_num, vel_num, tim_num, status_launch, status_orbit)
        self.play(FadeIn(hud, shift=0.2 * UP), run_time=0.4)

        # Orbit-only traced path
        trace = TracedPath(lambda: rocket.get_center(), stroke_color=COLOR_ACCENT, stroke_width=2)
        self.add(trace)

        # Set initial values and trigger updaters
        altitude.set_value(500.0)
        velocity.set_value(7.3)
        mission_t.set_value(480.0)
        # Force initial update
        update_alt(alt_num)
        update_vel(vel_num)
        update_time(tim_num)

        # Build orbit arc and draw it
        orbit_arc = Arc(
            radius=orbit_radius,
            start_angle=start_angle,
            angle=PI * 1.3,
        ).move_arc_center_to(earth.get_center())
        orbit_path_draw = orbit_arc.copy().set_stroke(COLOR_OUTLINE, 1, opacity=0.35)
        self.play(FadeIn(orbit_path_draw), run_time=0.3)

        # First orbit with gradual HUD updates
        def update_hud_first(alpha):
            alt_val = 500.0 + alpha * 40.0
            vel_val = 7.3 + alpha * 0.3
            time_val = 480.0 + alpha * 60.0
            altitude.set_value(alt_val)
            velocity.set_value(vel_val)
            mission_t.set_value(time_val)
            # Force text updates
            alt_num.set_text(f"{int(alt_val):,} km")
            vel_num.set_text(f"{vel_val:.2f} km/s")
            tim_num.set_text(f"{time_val:.1f} s")
        
        self.play(
            AnimationGroup(
                MoveAlongPath(rocket, orbit_arc),
                stars_near.animate.shift(1.0 * LEFT),
                stars_mid.animate.shift(0.6 * LEFT),
                stars_far.animate.shift(0.3 * LEFT),
                UpdateFromAlphaFunc(altitude, lambda m, a: update_hud_first(a)),
                run_time=4.0,
            )
        )

        # Second orbit loop (longer, more parallax)
        orbit_arc2 = Arc(
            radius=orbit_radius,
            start_angle=start_angle + PI * 1.3,
            angle=PI * 1.8,
        ).move_arc_center_to(earth.get_center())
        
        # Second orbit with gradual HUD updates
        def update_hud_second(alpha):
            alt_val = 540.0 + alpha * 40.0
            vel_val = 7.6 + alpha * 0.2
            time_val = 540.0 + alpha * 180.0
            altitude.set_value(alt_val)
            velocity.set_value(vel_val)
            mission_t.set_value(time_val)
            # Force text updates
            alt_num.set_text(f"{int(alt_val):,} km")
            vel_num.set_text(f"{vel_val:.2f} km/s")
            tim_num.set_text(f"{time_val:.1f} s")
        
        self.play(
            AnimationGroup(
                MoveAlongPath(rocket, orbit_arc2),
                stars_near.animate.shift(2.2 * LEFT + 0.4 * DOWN),
                stars_mid.animate.shift(1.4 * LEFT + 0.2 * DOWN),
                stars_far.animate.shift(0.8 * LEFT + 0.1 * DOWN),
                UpdateFromAlphaFunc(altitude, lambda m, a: update_hud_second(a)),
                run_time=5.5,
            )
        )

        # Transition to orbital view (slight zoom out effect via transform on Earth)
        earth_bigger = earth.copy().scale(1.05)
        self.play(Transform(earth, earth_bigger), run_time=0.4)

        # Hold and fade
        self.wait(0.8)
        self.play(
            LaggedStart(
                FadeOut(rocket),
                FadeOut(flames),
                FadeOut(trace),
                FadeOut(orbit_path_draw),
                FadeOut(hud),
                FadeOut(stars_near),
                FadeOut(stars_mid),
                FadeOut(stars_far),
                FadeOut(earth),
                lag_ratio=0.1,
                run_time=0.8,
            )
        )


