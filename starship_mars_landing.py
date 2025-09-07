from manim import *
import numpy as np

# Mars Landing Scene Colors
COLOR_MARS_SURFACE = "#CD5C5C"      # Mars red surface
COLOR_MARS_SKY = "#2F1B14"          # Dark red Martian sky
COLOR_MARS_DUST = "#8B4513"         # Dust brown
COLOR_STARSHIP = "#C0C0C0"          # Silver starship
COLOR_FLAME = "#FF4500"             # Orange flame
COLOR_HUD = "#00FF00"               # Green HUD
COLOR_BG = "#000000"                # Space black

class StarshipMarsLanding(MovingCameraScene):
    def construct(self):
        # Set background to space
        self.camera.background_color = COLOR_BG
        
        # Create Mars surface
        mars_surface = Rectangle(
            width=config.frame_width * 2,
            height=2.0,
            fill_color=COLOR_MARS_SURFACE,
            fill_opacity=1.0,
            stroke_width=0
        ).move_to(DOWN * 3.5)
        
        # Add Martian terrain features
        def create_martian_terrain():
            terrain = VGroup()
            for i in range(8):
                # Create rocky formations
                rock = Circle(
                    radius=np.random.uniform(0.1, 0.3),
                    fill_color=COLOR_MARS_DUST,
                    fill_opacity=0.8,
                    stroke_width=0
                )
                rock.move_to(
                    mars_surface.get_top() + 
                    RIGHT * np.random.uniform(-6, 6) + 
                    UP * np.random.uniform(0, 0.5)
                )
                terrain.add(rock)
            return terrain
        
        terrain = create_martian_terrain()
        
        # Create Mars sky with dust
        mars_sky = Rectangle(
            width=config.frame_width * 2,
            height=config.frame_height,
            fill_color=COLOR_MARS_SKY,
            fill_opacity=0.3,
            stroke_width=0
        ).move_to(UP * 2)
        
        # Add dust particles in atmosphere
        def create_dust_particles():
            dust = VGroup()
            for _ in range(50):
                particle = Dot(
                    radius=np.random.uniform(0.01, 0.03),
                    color=COLOR_MARS_DUST
                )
                particle.set_opacity(np.random.uniform(0.2, 0.6))
                particle.move_to(
                    np.array([
                        np.random.uniform(-8, 8),
                        np.random.uniform(-2, 4),
                        0
                    ])
                )
                dust.add(particle)
            return dust
        
        dust_particles = create_dust_particles()
        
        # Create Starship (similar to previous scenes but with landing gear)
        def create_starship():
            # Main body
            body = Rectangle(
                width=0.8,
                height=3.2,
                fill_color=COLOR_STARSHIP,
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=2
            )
            
            # Nose cone
            nose = Polygon(
                UP * 1.6,
                RIGHT * 0.4,
                DOWN * 0.1,
                LEFT * 0.4,
                fill_color=COLOR_STARSHIP,
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=2
            ).next_to(body, UP, buff=0)
            
            # Landing legs
            leg1 = Rectangle(width=0.1, height=0.8, fill_color=COLOR_STARSHIP).next_to(body, DOWN + LEFT * 0.3, buff=0)
            leg2 = Rectangle(width=0.1, height=0.8, fill_color=COLOR_STARSHIP).next_to(body, DOWN + RIGHT * 0.3, buff=0)
            leg3 = Rectangle(width=0.1, height=0.8, fill_color=COLOR_STARSHIP).next_to(body, DOWN, buff=0)
            
            # Landing pads
            pad1 = Circle(radius=0.15, fill_color=COLOR_STARSHIP).next_to(leg1, DOWN, buff=0)
            pad2 = Circle(radius=0.15, fill_color=COLOR_STARSHIP).next_to(leg2, DOWN, buff=0)
            pad3 = Circle(radius=0.15, fill_color=COLOR_STARSHIP).next_to(leg3, DOWN, buff=0)
            
            # Retro-rocket flames
            flame1 = Polygon(
                DOWN * 0.3,
                LEFT * 0.1,
                RIGHT * 0.1,
                fill_color=COLOR_FLAME,
                fill_opacity=0.8,
                stroke_width=0
            ).next_to(leg1, UP, buff=0)
            
            flame2 = Polygon(
                DOWN * 0.3,
                LEFT * 0.1,
                RIGHT * 0.1,
                fill_color=COLOR_FLAME,
                fill_opacity=0.8,
                stroke_width=0
            ).next_to(leg2, UP, buff=0)
            
            flame3 = Polygon(
                DOWN * 0.3,
                LEFT * 0.1,
                RIGHT * 0.1,
                fill_color=COLOR_FLAME,
                fill_opacity=0.8,
                stroke_width=0
            ).next_to(leg3, UP, buff=0)
            
            flames = VGroup(flame1, flame2, flame3)
            flames.set_opacity(0)  # Start invisible
            
            starship = VGroup(body, nose, leg1, leg2, leg3, pad1, pad2, pad3, flames)
            return starship, flames
        
        starship, retro_flames = create_starship()
        starship.move_to(UP * 4 + RIGHT * 2)
        
        # Create HUD for landing
        def create_landing_hud():
            hud_bg = RoundedRectangle(
                width=4.0,
                height=2.5,
                corner_radius=0.1,
                fill_color=BLACK,
                fill_opacity=0.8,
                stroke_color=COLOR_HUD,
                stroke_width=2
            ).to_corner(UR, buff=0.3)
            
            # Landing metrics
            alt_label = Text("ALT", font_size=24, color=COLOR_HUD).next_to(hud_bg, UP + LEFT, buff=0.1)
            vel_label = Text("VEL", font_size=24, color=COLOR_HUD).next_to(alt_label, DOWN, buff=0.2)
            fuel_label = Text("FUEL", font_size=24, color=COLOR_HUD).next_to(vel_label, DOWN, buff=0.2)
            status_label = Text("STATUS", font_size=24, color=COLOR_HUD).next_to(fuel_label, DOWN, buff=0.2)
            
            # Values
            alt_value = Text("1200 m", font_size=20, color=WHITE).next_to(alt_label, RIGHT, buff=0.5)
            vel_value = Text("45 m/s", font_size=20, color=WHITE).next_to(vel_label, RIGHT, buff=0.5)
            fuel_value = Text("23%", font_size=20, color=YELLOW).next_to(fuel_label, RIGHT, buff=0.5)
            status_value = Text("DESCENT", font_size=20, color=COLOR_HUD).next_to(status_label, RIGHT, buff=0.5)
            
            hud = VGroup(
                hud_bg, alt_label, vel_label, fuel_label, status_label,
                alt_value, vel_value, fuel_value, status_value
            )
            return hud, alt_value, vel_value, fuel_value, status_value
        
        hud, alt_val, vel_val, fuel_val, status_val = create_landing_hud()
        
        # Animation sequence
        # 1. Show Mars environment
        self.play(
            LaggedStart(
                FadeIn(mars_surface, shift=UP),
                FadeIn(terrain, shift=UP),
                FadeIn(mars_sky, shift=DOWN),
                FadeIn(dust_particles, shift=DOWN),
                lag_ratio=0.3,
                run_time=2.0
            )
        )
        
        # 2. Starship appears from space
        self.play(
            FadeIn(starship, shift=DOWN),
            run_time=1.0
        )
        
        # 3. HUD appears
        self.play(
            FadeIn(hud, shift=LEFT),
            run_time=0.8
        )
        
        # 4. Landing sequence with HUD updates
        def update_landing_hud(alpha):
            # Altitude decreases from 1200m to 0m
            altitude = 1200 - alpha * 1200
            # Velocity decreases from 45 m/s to 0 m/s
            velocity = 45 - alpha * 45
            # Fuel decreases from 23% to 5%
            fuel = 23 - alpha * 18
            # Status changes
            if alpha < 0.7:
                status = "DESCENT"
            elif alpha < 0.9:
                status = "LANDING"
            else:
                status = "LANDED"
            
            alt_val.set_text(f"{int(altitude)} m")
            vel_val.set_text(f"{velocity:.1f} m/s")
            fuel_val.set_text(f"{fuel:.0f}%")
            status_val.set_text(status)
            
            # Change fuel color based on level
            if fuel < 10:
                fuel_val.set_color(RED)
            elif fuel < 15:
                fuel_val.set_color(YELLOW)
            else:
                fuel_val.set_color(WHITE)
        
        # 5. Descent with retro-rockets
        def activate_retro_rockets(mobj, alpha):
            if alpha > 0.3:  # Activate retro-rockets at 30% of descent
                retro_flames.set_opacity(0.8)
            else:
                retro_flames.set_opacity(0)
        
        # 6. Landing animation
        self.play(
            AnimationGroup(
                starship.animate.move_to(mars_surface.get_top() + UP * 0.5),
                UpdateFromAlphaFunc(starship, lambda m, a: update_landing_hud(a)),
                UpdateFromAlphaFunc(starship, activate_retro_rockets),
                dust_particles.animate.shift(0.5 * UP),  # Dust kicked up
                run_time=6.0,
                rate_func=rate_functions.ease_in_sine
            )
        )
        
        # 7. Landing impact effects
        impact_dust = VGroup()
        for _ in range(20):
            particle = Dot(
                radius=np.random.uniform(0.02, 0.05),
                color=COLOR_MARS_DUST
            )
            particle.set_opacity(np.random.uniform(0.4, 0.8))
            particle.move_to(starship.get_bottom() + DOWN * 0.2)
            impact_dust.add(particle)
        
        self.play(
            AnimationGroup(
                *[particle.animate.shift(
                    np.random.uniform(-1, 1) * RIGHT + 
                    np.random.uniform(0.5, 1.5) * UP
                ).set_opacity(0) for particle in impact_dust],
                run_time=1.5
            )
        )
        
        # 8. Final status update
        status_val.set_text("LANDED")
        status_val.set_color(GREEN)
        self.play(
            Transform(status_val, status_val.copy().set_color(GREEN)),
            run_time=0.5
        )
        
        # 9. Hold and fade
        self.wait(2.0)
        self.play(
            LaggedStart(
                FadeOut(starship),
                FadeOut(hud),
                FadeOut(impact_dust),
                FadeOut(dust_particles),
                FadeOut(terrain),
                FadeOut(mars_surface),
                FadeOut(mars_sky),
                lag_ratio=0.2,
                run_time=1.5
            )
        )
