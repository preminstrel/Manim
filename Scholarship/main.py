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
        #gen1 = Square(color=BLUE, fill_opacity=1)
        Intro = Tex("Introduction",color="BLACK").scale(1.5)
        self.play(
            Transform(SEU, SEU2),
            FadeOut(title),
            FadeOut(author),
            FadeOut(institution),
            Transform(title, Intro),
            #FadeIn(Contents),
        )
        #self.add(Contents)
        #self.wait(2)
        #self.play(FadeIn(gen1))
        
        self.play(ApplyMethod(title.shift,UP*3))
        me = ImageMobject("ME.png").scale(0.13)
        self.play(FadeIn(me))
        self.play(ApplyMethod(me.shift,LEFT*4))
        Name = Tex("Name\qquad 孙寒石",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.9).move_to(UP*0.5)
        Class = Tex("Class\qquad 062191",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.9).move_to(DOWN*0.5)
        self.play(
            Write(Name),
            Write(Class),
        )
        
    ## Contents
        self.play(
            FadeOut(me),
            FadeOut(Name, shift=DOWN * 2, scale=1.5),
            FadeOut(Class, shift=DOWN * 2, scale=1.5),
            Transform(title,Contents)
        )
        #self.add(Contents)
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
            FadeOut(title),
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
        Aver100 = Tex("/100",color="BLUE").move_to(RIGHT*2.5+UP)
        self.play(Write(Average))
        self.add(number)
        self.add(Aver100)
        # Play the Count Animation to count from 0 to 100 in 4 seconds
        self.play(Count(number, 0, 93.80), run_time=1.3, rate_func=linear)

        number2 = DecimalNumber().set_color(RED)
        number2.add_updater(lambda number2: number2.move_to(RIGHT))
        number2.move_to(RIGHT)
        GPA=Tex("GPA",color="BLACK")
        GPA.move_to(LEFT*2)
        GPA4 = Tex("/4.8",color="RED").move_to(RIGHT*2.3)
        self.play(Write(GPA))
        self.add(GPA4)
        self.add(number2)
        self.play(Count(number2,0,4.36),run_time=1.3,rate_func=linear)

        Rank=Tex("Rank",color="BLACK").move_to(LEFT*2+DOWN)
        Rank1=Tex("TOP 1",color="GREEN").move_to(RIGHT*1.5+DOWN)
        self.play(Write(Rank),Write(Rank1))

        ## END of RANK
        maths=Tex("数学分析",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+UP*1.7)
        rectan1=Rectangle(color="BLUE")
        rectan1.surround(maths,buff=0.35)
        group1 = VGroup(maths,rectan1)
        s1=Tex("99",color="BLACK").move_to(LEFT*2.5+UP*1.7)

        linear_a=Tex("线性代数",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+UP*0.5)
        rectan2=Rectangle(color="RED")
        rectan2.surround(linear_a,buff=0.35)
        group2=VGroup(linear_a,rectan2)
        s2=Tex("98",color="BLACK").move_to(LEFT*2.5+UP*0.5)

        Phy=Tex("大学物理",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+DOWN*0.7)
        rectan3=Rectangle(color="YELLOW")
        rectan3.surround(Phy,buff=0.35)
        #group3 = VGroup(Phy,rectan3)
        s3 = Tex("98",color="BLACK").move_to(LEFT*2.5+DOWN*0.7)

        C=Tex("程序设计",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+DOWN*1.9)
        rectan4=Rectangle(color="GREEN")
        rectan4.surround(C,buff=0.35)
        group3=VGroup(Phy,rectan3,C,rectan4)
        s4=Tex("97",color="BLACK").move_to(LEFT*2.5+DOWN*1.9)

        self.play(
            Transform(Average,group1),
            Transform(GPA,group2),
            Transform(Rank,group3),
            FadeOut(Aver100),
            FadeOut(number),
            FadeOut(number2),
            FadeOut(Rank1),
            FadeOut(GPA4),
        )
        self.play(

            Write(s1),
            Write(s2),
            Write(s3),
            Write(s4),
        )
