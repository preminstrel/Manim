from manim import *
config.background_color = WHITE

class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number,  **kwargs)
        # Set start and end
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)

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
        Contents = Tex("\\textbf{Contents}",color="BLACK").scale(1.5)
        Contents.to_corner(UP+LEFT)

        Content1 = Tex("学习\quad Study",tex_template=TexTemplateLibrary.ctex,color="BLACK")
        Content2 = Tex("科研\quad Research",tex_template=TexTemplateLibrary.ctex,color="BLACK")
        Content3 = Tex("荣誉\quad Honors",tex_template=TexTemplateLibrary.ctex,color="BLACK")
        Content4 = Tex("生活\quad Life",tex_template=TexTemplateLibrary.ctex,color="BLACK")
        gen1 = Square(color=BLUE, fill_opacity=1)

        self.play(
            Transform(SEU, SEU2),
            FadeOut(title),
            FadeOut(author),
            FadeOut(institution),
            Transform(title, Contents),
            #FadeIn(Contents),
        )
        self.add(Contents)
        #self.wait(2)
        #self.play(FadeIn(gen1))
        

        Content1.move_to(LEFT*2.15+UP*1)
        Content2.move_to(RIGHT*2.45+UP*1)
        Content3.move_to(LEFT*2+DOWN*1)
        Content4.move_to(RIGHT*2+DOWN*1)
        
        self.play(
            Write(Content1),
            Write(Content2),
            Write(Content3),
            Write(Content4),
        )

        # END of Page 2

        self.play(
            FadeOut(Contents),
            FadeOut(Content4),
            FadeOut(Content2),
            FadeOut(Content3),
        )
        Study = Text("Study").scale(1.2)
        for letter in Study:
            letter.set_color(random_bright_color())
        self.play(Transform(Content1,Study))
        Study_copy = Study.shift(UP)
        self.play(
            #FadeOut(Content1),
            ApplyMethod(Content1.shift,UP*3),
            #Transform(Content1,Study_copy)  Mind the Difference!!
        )
        
        # Create Decimal Number and add it to scene
        number = DecimalNumber().set_color(BLUE)
        # Add an updater to keep the DecimalNumber centered as its value changes
        number.add_updater(lambda number: number.move_to(RIGHT+UP))
        number.move_to(RIGHT+UP)
        Average = Tex("Average Score",color="BLACK")
        Average.move_to(LEFT*2+UP)
        self.play(Write(Average))
        self.add(number)
        # Play the Count Animation to count from 0 to 100 in 4 seconds
        self.play(Count(number, 0, 93.80), run_time=4, rate_func=linear)

        number2 = DecimalNumber().set_color(RED)
        number2.add_updater(lambda number2: number2.move_to(RIGHT))
        number2.move_to(RIGHT)
        GPA=Tex("GPA",color="BLACK")
        GPA.move_to(LEFT*2)
        self.play(Write(GPA))
        self.add(number2)
        self.play(Count(number2,0,4.36),run_time=4,rate_func=linear)
        self.wait(2)
