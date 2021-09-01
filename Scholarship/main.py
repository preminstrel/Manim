from manim import *
config.background_color = WHITE
class scene1(Scene):
    def construct(self):
        SEU = ImageMobject("SEU.jpg").scale(0.7)
        SEU2 = ImageMobject("SEU.jpg").scale(0.7)
        title = Tex("\\textbf{国家奖学金答辩}", tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(1.7)
        author = Tex("06219109 孙寒石", tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).shift(DOWN)
        date = Tex("Oct 2021",color="BLACK").scale(0.4)
        institution = Tex("\emph{School of EE(Wuxi Branch)}",color="BLACK").scale(0.5)
        SEU.move_to(UP*2)
        institution.move_to(DOWN*2.5)
        date.move_to(DOWN*3.5)
        self.play(
            FadeInFrom(SEU,UP),
            Write(title),
            FadeInFrom(author, UP),
            Write(date),
            Write(institution),
        )
        self.wait(2)

# END of Frist Page

        SEU2.scale(0.6)
        SEU2.to_corner(UP+RIGHT)
        self.play(
            Transform(SEU, SEU2),
            FadeOut(title),
            FadeOut(author),
            FadeOut(institution),
        )
        self.wait(2)