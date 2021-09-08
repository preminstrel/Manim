from manim import *
class scene1(Scene):
    def construct(self):
        Electron = ImageMobject("Electron.png").scale(0.2)
        title = Tex("Drawing Electron Cloud with Matlab").scale(1.4)
        author = Tex("@author Hanshi Sun").shift(DOWN)
        Electron.move_to(UP*2)
        self.play(
            FadeIn(Electron,shift=UP),
            Write(title),
            FadeIn(author, shift=UP),
        )
        self.wait(1)


        ref = Tex("Reference")
        ref.to_corner(UP + LEFT)
        article = Tex("Drawing Angular Part of Atomic Orbital and Hybrid Orbital\\\ By Using MATLAB").scale(0.9)
        scholar = SVGMobject("Google_Scholar_logo.svg").scale(0.5)
        scholar.next_to(ref,RIGHT)
        matlab = ImageMobject("Matlab_Logo (1).png").scale(0.6)
        matlab.next_to(article,DOWN)
        article_author = Tex("LV Shenzhuang").scale(0.7)
        article_author.next_to(matlab,DOWN)
        openword = Tex("My project is based on the article below:").scale(0.8)
        openword.move_to(UP*1.5)
        self.play(
            Electron.animate.to_corner(UR),
            Transform(title, ref),
            #LaggedStart(*[FadeOutAndShift(obj, direction=DOWN) for obj in author]),
            FadeOut(author),
        )

        self.play(FadeIn(openword,shift=UP),Create(scholar),FadeIn(article, shift=DOWN),FadeIn(matlab,shift=LEFT),FadeIn(article_author,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Electron),FadeOut(openword),Uncreate(scholar),FadeOut(title),FadeOut(matlab),FadeOut(article),FadeOut(article_author))

class scene2(ThreeDScene):
    def construct(self):
        text3d = Tex("The drawing ability of MATLAB is very powerful, \\\ which can help us draw all kinds of complex 3D images")
        text3d.to_corner(UL)
        self.play(Write(text3d))
        self.add_fixed_in_frame_mobjects(text3d)

        resolution_fa = 22
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)

        def param_plane(u, v):
            x = u
            y = v
            z = 0
            return np.array([x, y, z])

        plane = ParametricSurface(
            param_plane,
            resolution=(resolution_fa, resolution_fa),
            v_min=-2,
            v_max=+2,
            u_min=-2,
            u_max=+2,
        )
        plane.scale_about_point(2, ORIGIN)

        def param_gauss(u, v):
            x = u
            y = v
            d = np.sqrt(x * x + y * y)
            sigma, mu = 0.4, 0.0
            z = np.exp(-((d - mu) ** 2 / (2.0 * sigma ** 2)))
            return np.array([x, y, z])

        gauss_plane = ParametricSurface(
            param_gauss,
            resolution=(resolution_fa, resolution_fa),
            v_min=-2,
            v_max=+2,
            u_min=-2,
            u_max=+2,
        )

        gauss_plane.scale_about_point(2, ORIGIN)
        gauss_plane.set_style(fill_opacity=1)
        gauss_plane.set_style(stroke_color=GREEN)
        gauss_plane.set_fill_by_checkerboard(GREEN, BLUE, opacity=0.1)

        axes = ThreeDAxes()

        self.play(Create(axes))
        self.play(Write(plane))
        self.play(Transform(plane, gauss_plane))
        self.wait()

class scene3(Scene):
    def construct(self):
        t1 = Tex("Pictures below").move_to(3*UP)
        s = Tex("s orbit").move_to(3*UP)
        Ys = ImageMobject("Ys.jpg").move_to(3*LEFT)
        Ys0 = ImageMobject("Ys0.jpg").move_to(3*RIGHT)

        px = MathTex("p_x \\text{ orbit}").move_to(3*UP)
        Ypx = ImageMobject("Ypx.jpg").move_to(3*LEFT)
        Ypx0 = ImageMobject("Ypx0.jpg").move_to(3*RIGHT)

        py = MathTex("p_y \\text{ orbit}").move_to(3*UP)
        Ypy = ImageMobject("Ypy.jpg").move_to(3*LEFT)
        Ypy0 = ImageMobject("Ypy0.jpg").move_to(3*RIGHT)

        pz = MathTex("p_z \\text{ orbit}").move_to(3*UP)
        Ypz = ImageMobject("Ypz.jpg").move_to(3*LEFT)
        Ypz0 = ImageMobject("Ypz0.jpg").move_to(3*RIGHT)

        dxy = MathTex("d_{xy} \\text{ orbit}").move_to(3*UP)
        Ydxy = ImageMobject("Ydxy.jpg").move_to(3*LEFT)
        Ydxy0 = ImageMobject("Ydxy0.jpg").move_to(3*RIGHT)

        dxz = MathTex("d_{xz} \\text{ orbit}").move_to(3*UP)
        Ydxz = ImageMobject("Ydxz.jpg").move_to(3*LEFT)
        Ydxz0 = ImageMobject("Ydxz0.jpg").move_to(3*RIGHT)

        dyz = MathTex("d_{yz} \\text{ orbit}").move_to(3*UP)
        Ydyz = ImageMobject("Ydyz.jpg").move_to(3*LEFT)
        Ydyz0 = ImageMobject("Ydyz0.jpg").move_to(3*RIGHT)

        dx2y2 = MathTex("d_{x^2-y^2} \\text{ orbit}").move_to(3*UP)
        Ydx2y2 = ImageMobject("Ydx2y2.jpg").move_to(3*LEFT)
        Ydx2y20 = ImageMobject("Ydx2y20.jpg").move_to(3*RIGHT)

        dz2 = MathTex("d_{z^2} \\text{ orbit}").move_to(3*UP)
        Ydz2 = ImageMobject("Ydz2.jpg").move_to(3*LEFT)
        Ydz20 = ImageMobject("Ydz20.jpg").move_to(3*RIGHT)

        fz3 = MathTex("f_{z^3} \\text{ orbit}").move_to(3*UP)
        Yfz3 = ImageMobject("Yfz3.jpg").move_to(3*LEFT)
        Yfz30 = ImageMobject("Yfz30.jpg").move_to(3*RIGHT)

        fxz2 = MathTex("f_{xz^2} \\text{ orbit}").move_to(3*UP)
        Yfxz2 = ImageMobject("Yfxz2.jpg").move_to(3*LEFT)
        Yfxz20 = ImageMobject("Yfxz20.jpg").move_to(3*RIGHT)
       
        fyz2 = MathTex("f_{yz^2} \\text{ orbit}").move_to(3*UP)
        Yfyz2 = ImageMobject("Yfyz2.jpg").move_to(3*LEFT)
        Yfyz20 = ImageMobject("Yfyz20.jpg").move_to(3*RIGHT)

        fxyz = MathTex("f_{xyz} \\text{ orbit}").move_to(3*UP)
        Yfxyz = ImageMobject("Yfzxy.jpg").move_to(3*LEFT)
        Yfxyz0 = ImageMobject("Yfzxy0.jpg").move_to(3*RIGHT)

        fzx2_y2 = MathTex("f_{z(x^2-y^2)} \\text{ orbit}").move_to(3*UP)
        Yfzx2_y2 = ImageMobject("Yfzx2_y2.jpg").move_to(3*LEFT)
        Yfzx2_y20 = ImageMobject("Yfzx2_y20.jpg").move_to(3*RIGHT)

        fxx2_y2 = MathTex("f_{x(x^2-3y^2)} \\text{ orbit}").move_to(3*UP)
        Yfxx2_y2 = ImageMobject("Yfxx2_y2.jpg").move_to(3*LEFT)
        Yfxx2_y20 = ImageMobject("Yfxx2_y20.jpg").move_to(3*RIGHT)
  
        sp_1 = MathTex("sp_1 \\text{ orbit}").move_to(3*UP)
        Ysp_1 = ImageMobject("Ysp_1.jpg").move_to(3*LEFT)
        Ysp_10 = ImageMobject("Ysp_10.jpg").move_to(3*RIGHT)

        sp_2 = MathTex("sp_2 \\text{ orbit}").move_to(3*UP)
        Ysp_2 = ImageMobject("Ysp_2.jpg").move_to(3*LEFT)
        Ysp_20 = ImageMobject("Ysp_20.jpg").move_to(3*RIGHT)  

        sp2_1 = MathTex("sp^2_1 \\text{ orbit}").move_to(3*UP)
        Ysp2_1 = ImageMobject("Ysp2_1.jpg").move_to(3*LEFT)
        Ysp2_10 = ImageMobject("Ysp2_10.jpg").move_to(3*RIGHT) 

        sp2_2 = MathTex("sp^2_2 \\text{ orbit}").move_to(3*UP)
        Ysp2_2 = ImageMobject("Ysp2_2.jpg").move_to(3*LEFT)
        Ysp2_20 = ImageMobject("Ysp2_20.jpg").move_to(3*RIGHT)                       

        sp2_3 = MathTex("sp^2_3 \\text{ orbit}").move_to(3*UP)
        Ysp2_3 = ImageMobject("Ysp2_3.jpg").move_to(3*LEFT)
        Ysp2_30 = ImageMobject("Ysp2_30.jpg").move_to(3*RIGHT)   


        sp3_1 = MathTex("sp^3_1 \\text{ orbit}").move_to(3*UP)
        Ysp3_1 = ImageMobject("Ysp3_1.jpg").move_to(3*LEFT)
        Ysp3_10 = ImageMobject("Ysp3_10.jpg").move_to(3*RIGHT)

        sp3_2 = MathTex("sp^3_2 \\text{ orbit}").move_to(3*UP)
        Ysp3_2 = ImageMobject("Ysp3_2.jpg").move_to(3*LEFT)
        Ysp3_20 = ImageMobject("Ysp3_20.jpg").move_to(3*RIGHT)

        sp3_3 = MathTex("sp^3_3 \\text{ orbit}").move_to(3*UP)
        Ysp3_3 = ImageMobject("Ysp3_3.jpg").move_to(3*LEFT)
        Ysp3_30 = ImageMobject("Ysp3_30.jpg").move_to(3*RIGHT)

        sp3_4 = MathTex("sp^3_4 \\text{ orbit}").move_to(3*UP)
        Ysp3_4 = ImageMobject("Ysp3_4.jpg").move_to(3*LEFT)
        Ysp3_40 = ImageMobject("Ysp3_40.jpg").move_to(3*RIGHT)

        self.play(Write(t1))
        self.play(t1.animate.to_corner(UL))
        self.play(FadeIn(Ys,shift=LEFT),FadeIn(Ys0,shift=RIGHT),Write(s))
        self.wait(1)
        self.play(FadeOut(Ys),FadeOut(Ys0))
        self.play(ReplacementTransform(s, px),FadeIn(Ypx,shift=LEFT),FadeIn(Ypx0,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ypx),FadeOut(Ypx0))
        self.play(ReplacementTransform(px, py),FadeIn(Ypy,shift=LEFT),FadeIn(Ypy0,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ypy),FadeOut(Ypy0))
        self.play(ReplacementTransform(py, pz),FadeIn(Ypz,shift=LEFT),FadeIn(Ypz0,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ypz),FadeOut(Ypz0))

        self.play(ReplacementTransform(pz, dxy),FadeIn(Ydxy,shift=LEFT),FadeIn(Ydxy0,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ydxy),FadeOut(Ydxy0))
        self.play(ReplacementTransform(dxy, dxz),FadeIn(Ydxz,shift=LEFT),FadeIn(Ydxz0,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ydxz),FadeOut(Ydxz0))
        self.play(ReplacementTransform(dxz, dyz),FadeIn(Ydyz,shift=LEFT),FadeIn(Ydyz0,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ydyz),FadeOut(Ydyz0))

        self.play(ReplacementTransform(dyz, fz3),FadeIn(Yfz3,shift=LEFT),FadeIn(Yfz30,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Yfz3),FadeOut(Yfz30))
        self.play(ReplacementTransform(fz3, fxz2),FadeIn(Yfxz2,shift=LEFT),FadeIn(Yfxz20,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Yfxz2),FadeOut(Yfxz20))
        self.play(ReplacementTransform(fxz2, fyz2),FadeIn(Yfyz2,shift=LEFT),FadeIn(Yfyz20,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Yfyz2),FadeOut(Yfyz20))
        self.play(ReplacementTransform(fyz2, fxyz),FadeIn(Yfxyz,shift=LEFT),FadeIn(Yfxyz0,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Yfxyz),FadeOut(Yfxyz0))
        self.play(ReplacementTransform(fxyz, fzx2_y2),FadeIn(Yfzx2_y2,shift=LEFT),FadeIn(Yfzx2_y20,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Yfzx2_y2),FadeOut(Yfzx2_y20))
        self.play(ReplacementTransform(fzx2_y2, fxx2_y2),FadeIn(Yfxx2_y2,shift=LEFT),FadeIn(Yfxx2_y20,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Yfxx2_y2),FadeOut(Yfxx2_y20))


        self.play(ReplacementTransform(fxx2_y2, sp_1),FadeIn(Ysp_1,shift=LEFT),FadeIn(Ysp_10,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ysp_1),FadeOut(Ysp_10))
        self.play(ReplacementTransform(sp_1, sp_2),FadeIn(Ysp_2,shift=LEFT),FadeIn(Ysp_20,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ysp_2),FadeOut(Ysp_20))
        self.play(ReplacementTransform(sp_2, sp2_1),FadeIn(Ysp2_1,shift=LEFT),FadeIn(Ysp2_10,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ysp2_1),FadeOut(Ysp2_10))
        self.play(ReplacementTransform(sp2_1, sp2_2),FadeIn(Ysp2_2,shift=LEFT),FadeIn(Ysp2_20,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ysp2_2),FadeOut(Ysp2_20))
        self.play(ReplacementTransform(sp2_2, sp2_3),FadeIn(Ysp2_3,shift=LEFT),FadeIn(Ysp2_30,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ysp2_3),FadeOut(Ysp2_30))        
        self.play(ReplacementTransform(sp2_3, sp3_1),FadeIn(Ysp3_1,shift=LEFT),FadeIn(Ysp3_10,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ysp3_1),FadeOut(Ysp3_10))
        self.play(ReplacementTransform(sp3_1, sp3_2),FadeIn(Ysp3_2,shift=LEFT),FadeIn(Ysp3_20,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ysp3_2),FadeOut(Ysp3_20))
        self.play(ReplacementTransform(sp3_2, sp3_3),FadeIn(Ysp3_3,shift=LEFT),FadeIn(Ysp3_30,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ysp3_3),FadeOut(Ysp3_30))
        self.play(ReplacementTransform(sp3_3, sp3_4),FadeIn(Ysp3_4,shift=LEFT),FadeIn(Ysp3_40,shift=RIGHT))
        self.wait(1)
        self.play(FadeOut(Ysp3_4),FadeOut(Ysp3_40))


class scene4(Scene):
    def construct(self):
        contact = Tex("Contact me").scale(2)
        contact.move_to(UP*3)
        github = Tex("https://github.com/preminstrel")
        github.move_to(UP+RIGHT)
        mail = Tex("preminstrel@gmail.com")
        mail.move_to(DOWN+RIGHT)
        github_png = ImageMobject("Github.png").scale(0.1)
        github_png.move_to(UP)
        mail_svg = SVGMobject("Gmail.svg").scale(0.5)
        mail_svg.move_to(DOWN)
        self.play(Create(mail_svg),FadeIn(github_png),Write(contact))
        self.play(mail_svg.animate.move_to(LEFT*3.5+DOWN),github_png.animate.move_to(LEFT*3.5+UP))
        github.next_to(github_png, RIGHT,buff = 1)
        mail.next_to(mail_svg,RIGHT,buff = 1)
        self.play(Write(mail),Write(github))
        self.wait(1)