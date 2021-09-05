from manim import *
import itertools as it
config.background_color = WHITE

class NeuralNetworkMobject(VGroup):
    # Remove CONFIG since it is now deprecated in ManimCE
    # CONFIG = {
    #     "neuron_radius": 0.15,
    #     "neuron_to_neuron_buff": MED_SMALL_BUFF,
    #     "layer_to_layer_buff": LARGE_BUFF,
    #     "output_neuron_color": WHITE,
    #     "input_neuron_color": WHITE,
    #     "hidden_layer_neuron_color": WHITE,
    #     "neuron_stroke_width": 2,
    #     "neuron_fill_color": GREEN,
    #     "edge_color": LIGHT_GREY,
    #     "edge_stroke_width": 2,
    #     "edge_propogation_color": YELLOW,
    #     "edge_propogation_time": 1,
    #     "max_shown_neurons": 16,
    #     "brace_for_large_layers": True,
    #     "average_shown_activation_of_large_layer": True,
    #     "include_output_labels": False,
    #     "arrow": False,
    #     "arrow_tip_size": 0.1,
    #     "left_size": 1,
    #     "neuron_fill_opacity": 1
    # }

    # Constructor with parameters of the neurons in a list
    def __init__(
        self,
        neural_network,
        *args,

            neuron_radius=0.15,
            neuron_to_neuron_buff=MED_SMALL_BUFF,
            layer_to_layer_buff=LARGE_BUFF,
            output_neuron_color=WHITE,
            input_neuron_color=WHITE,
            hidden_layer_neuron_color=WHITE,
            neuron_stroke_width=2,
            neuron_fill_color=GREEN,
            edge_color=LIGHT_GREY,
            edge_stroke_width=2,
            edge_propogation_color=YELLOW,
            edge_propogation_time=1,
            max_shown_neurons=16,
            brace_for_large_layers=True,
            average_shown_activation_of_large_layer=True,
            include_output_labels=False,
            arrow=False,
            arrow_tip_size=0.1,
            left_size=1,
            neuron_fill_opacity=1,

            **kwargs,
    ):
        VGroup.__init__(self, *args, **kwargs)

        self.neuron_radius = neuron_radius
        self.neuron_to_neuron_buff = neuron_to_neuron_buff
        self.layer_to_layer_buff = layer_to_layer_buff
        self.output_neuron_color = output_neuron_color
        self.input_neuron_color = input_neuron_color
        self.hidden_layer_neuron_color = hidden_layer_neuron_color
        self.neuron_stroke_width = neuron_stroke_width
        self.neuron_fill_color = neuron_fill_color
        self.edge_color = edge_color
        self.edge_stroke_width = edge_stroke_width
        self.edge_propogation_color = edge_propogation_color
        self.edge_propogation_time = edge_propogation_time
        self.max_shown_neurons = max_shown_neurons
        self.brace_for_large_layers = brace_for_large_layers
        self.average_shown_activation_of_large_layer = average_shown_activation_of_large_layer
        self.include_output_labels = include_output_labels
        self.arrow = arrow
        self.arrow_tip_size = arrow_tip_size,
        self.left_size = left_size
        self.neuron_fill_opacity = neuron_fill_opacity

        self.layer_sizes = neural_network
        self.add_neurons()
        self.add_edges()
        self.add_to_back(self.layers)

    # Helper method for constructor
    def add_neurons(self):
        layers = VGroup(*[
            self.get_layer(size, index)
            for index, size in enumerate(self.layer_sizes)
        ])
        layers.arrange_submobjects(RIGHT, buff=self.layer_to_layer_buff)
        self.layers = layers
        if self.include_output_labels:
            self.label_outputs_text()
    # Helper method for constructor

    def get_nn_fill_color(self, index):
        if index == -1 or index == len(self.layer_sizes) - 1:
            return self.output_neuron_color
        if index == 0:
            return self.input_neuron_color
        else:
            return self.hidden_layer_neuron_color
    # Helper method for constructor

    def get_layer(self, size, index=-1):
        layer = VGroup()
        n_neurons = size
        if n_neurons > self.max_shown_neurons:
            n_neurons = self.max_shown_neurons
        neurons = VGroup(*[
            Circle(
                radius=self.neuron_radius,
                stroke_color=self.get_nn_fill_color(index),
                stroke_width=self.neuron_stroke_width,
                fill_color=BLACK,
                fill_opacity=0.3,
            )
            for x in range(n_neurons)
        ])
        neurons.arrange_submobjects(
            DOWN, buff=self.neuron_to_neuron_buff
        )
        for neuron in neurons:
            neuron.edges_in = VGroup()
            neuron.edges_out = VGroup()
        layer.neurons = neurons
        layer.add(neurons)

        if size > n_neurons:
            dots = Tex("\\vdots")
            dots.move_to(neurons)
            VGroup(*neurons[:len(neurons) // 2]).next_to(
                dots, UP, MED_SMALL_BUFF
            )
            VGroup(*neurons[len(neurons) // 2:]).next_to(
                dots, DOWN, MED_SMALL_BUFF
            )
            layer.dots = dots
            layer.add(dots)
            if self.brace_for_large_layers:
                brace = Brace(layer, LEFT)
                brace_label = brace.get_tex(str(size))
                layer.brace = brace
                layer.brace_label = brace_label
                layer.add(brace, brace_label)

        return layer
    # Helper method for constructor

    def add_edges(self):
        self.edge_groups = VGroup()
        for l1, l2 in zip(self.layers[:-1], self.layers[1:]):
            edge_group = VGroup()
            for n1, n2 in it.product(l1.neurons, l2.neurons):
                edge = self.get_edge(n1, n2)
                edge_group.add(edge)
                n1.edges_out.add(edge)
                n2.edges_in.add(edge)
            self.edge_groups.add(edge_group)
        self.add_to_back(self.edge_groups)
    # Helper method for constructor

    def get_edge(self, neuron1, neuron2):
        if self.arrow:
            return Arrow(
                neuron1.get_center(),
                neuron2.get_center(),
                buff=self.neuron_radius,
                stroke_color=self.edge_color,
                stroke_width=self.edge_stroke_width,
                tip_length=self.arrow_tip_size
            )
        return Line(
            neuron1.get_center(),
            neuron2.get_center(),
            buff=self.neuron_radius,
            stroke_color=self.edge_color,
            stroke_width=self.edge_stroke_width,
        )

    # Labels each input neuron with a char l or a LaTeX character
    def label_inputs(self, l):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[0].neurons):
            label =  MathTex(r"{%s}_{{%s}}"%(str(l),str(n+1)))
            label.set_height(0.3 * neuron.get_height())
            label.move_to(neuron)
            self.output_labels.add(label)
        self.add(self.output_labels)

    # Labels each output neuron with a char l or a LaTeX character
    def label_outputs(self, l):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = MathTex(r"{%s}_{{%s}}"%(str(l),str(n+1)))
            label.set_height(0.4 * neuron.get_height())
            label.move_to(neuron)
            self.output_labels.add(label)
        self.add(self.output_labels)

    # Labels each neuron in the output layer with text according to an output list
    def label_outputs_text(self, outputs):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = Tex(outputs,color="BLACK").scale(1.5)
            label.set_height(0.75*neuron.get_height())
            label.move_to(neuron)
            label.shift((neuron.get_width() + label.get_width()/2)*RIGHT)
            self.output_labels.add(label)
        self.add(self.output_labels)

    # Labels the hidden layers with a char l or a LaTeX character
    def label_hidden_layers(self, l):
        self.output_labels = VGroup()
        for layer in self.layers[1:-1]:
            for n, neuron in enumerate(layer.neurons):
                label = MathTex(r"{%s}_{{%s}}"%(str(l),str(n+1))).set_color_by_tex(tex=r"{%s}_{{%s}}"%(str(l),str(n+1)),color="BLACK")
                label.set_height(0.4 * neuron.get_height())
                label.move_to(neuron)
                self.output_labels.add(label)
        self.add(self.output_labels)
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

class S1(Scene):
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
            FadeIn(SEU,shift=UP),
            Write(title),
            FadeIn(author, scale=1.5),
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
        Major = Tex("Major\qquad 电子科学与技术（无锡）",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.9).move_to(UP*0.8+RIGHT*0.9)
        Name = Tex("Name\qquad 孙寒石",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.9)
        Class = Tex("Class\qquad 062191",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.9).move_to(DOWN*0.8)
        self.play(
            Write(Name),
            Write(Class),
            Write(Major),
        )
        
    ## Contents
        self.play(
            FadeOut(Major, shift=DOWN*2,scale=1.5),
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
        #group1 = VGroup(maths,rectan1)
        s1=Tex("99",color="BLACK").move_to(LEFT*2.5+UP*1.7)
        rec1=Circle(color="BLUE")
        rec1.surround(s1)

        linear_a=Tex("线性代数",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+UP*0.5)
        rectan2=Rectangle(color="BROWN")
        rectan2.surround(linear_a,buff=0.35)
        #group2=VGroup(linear_a,rectan2)
        s2=Tex("98",color="BLACK").move_to(LEFT*2.5+UP*0.5)
        rec2=Circle(color="BROWN")
        rec2.surround(s2)

        Phy=Tex("大学物理",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+DOWN*0.7)
        rectan3=Rectangle(color="GRAY")
        rectan3.surround(Phy,buff=0.35)
        #group3 = VGroup(Phy,rectan3)
        s3 = Tex("98",color="BLACK").move_to(LEFT*2.5+DOWN*0.7)
        rec3=Circle(color="GRAY")
        rec3.surround(s3)
        
        C=Tex("程序设计",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+DOWN*1.9)
        rectan4=Rectangle(color="GOLD")
        rectan4.surround(C,buff=0.35)
        group3=VGroup(Phy,C)
        s4=Tex("97",color="BLACK").move_to(LEFT*2.5+DOWN*1.9)
        rec4=Circle(color="GOLD")
        rec4.surround(s4)
        
        maths1=Tex("数据结构",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(RIGHT*1.5+UP*1.7)
        rectan5=Rectangle(color="BLUE")
        rectan5.surround(maths1,buff=0.35)
        #group1 = VGroup(maths,rectan1)
        s5=Tex("99",color="BLACK").move_to(RIGHT*4+UP*1.7)
        rec5=Circle(color="BLUE")
        rec5.surround(s5)
  
        Signal=Tex("信号与系统",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(RIGHT*1.56+UP*0.5)
        rectan7=Rectangle(color="BROWN")
        rectan7.surround(linear_a,buff=0.30)
        #group2=VGroup(linear_a,rectan2)
        s7=Tex("95",color="BLACK").move_to(RIGHT*4+UP*0.5)
        rec7=Circle(color="BROWN")
        rec7.surround(s7)       
        
        Complexf=Tex("复变函数",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(RIGHT*1.5+DOWN*1.9)
        rectan8=Rectangle(color="GOLD")
        rectan8.surround(Complexf,buff=0.35)
        #group4=VGroup(Phy,C)
        s8=Tex("98",color="BLACK").move_to(RIGHT*4+DOWN*1.9)
        rec8=Circle(color="GOLD")
        rec8.surround(s8)
        
        gtwl=Tex("固体物理",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(RIGHT*1.5+DOWN*0.7)
        rectan6=Rectangle(color="GRAY")
        rectan6.surround(gtwl,buff=0.35)
        #group3 = VGroup(Phy,rectan3)
        s6 = Tex("96",color="BLACK").move_to(RIGHT*4+DOWN*0.7)
        rec6=Circle(color="GRAY")
        rec6.surround(s6)
        line1 = Line(UP*2.5,DOWN*3,color="BLACK").set_opacity(0.3)
        self.play(
            Transform(Average,maths),
            Transform(GPA,linear_a),
            Transform(Rank,group3),
            Write(maths1),
            Create(rectan5),
            Write(Complexf),
            Create(rectan8),
            Write(gtwl),
            Write(Signal),
            Create(rectan7),
            Create(rectan6),
            Create(rectan1),
            Create(rectan2),
            Create(rectan3),
            Create(rectan4),
            FadeOut(Aver100),
            FadeOut(number),
            FadeOut(number2),
            FadeOut(Rank1),
            FadeOut(GPA4),
            Create(line1),
        )
        self.play(
            Write(s1),
            Write(s2),
            Write(s3),
            Write(s4),
            Write(s5),
            Write(s6),
            Write(s7),
            Write(s8),
            Transform(rectan1,rec1),
            Transform(rectan2,rec2),
            Transform(rectan3,rec3),
            Transform(rectan4,rec4),
         
            Transform(rectan5,rec5),
            Transform(rectan6,rec6),
            Transform(rectan7,rec7),
            Transform(rectan8,rec8),
        )
### END of Details

        self.play(
            Unwrite(s1),
            Unwrite(s2),
            Unwrite(s3), 
            Unwrite(s4), 
            Unwrite(s5), 
            Unwrite(s6), 
            Unwrite(s7),
            Unwrite(s8),
            Uncreate(rectan1),
            Uncreate(rectan2),
            Uncreate(rectan3),
            Uncreate(rectan4),
            Uncreate(rectan5),
            Uncreate(rectan6),
            Uncreate(rectan7),
            Uncreate(rectan8),
            Uncreate(line1),
            Unwrite(gtwl),
            Unwrite(Signal),
            Unwrite(maths1),
            Unwrite(Rank,run_time=1),
            Unwrite(Complexf),
            Unwrite(Average),
            Unwrite(GPA),
        )

### STRAT OF RESEARCH

        Research = Text("Research").scale(1.2)
        for letter in Research:
            letter.set_color(random_bright_color())
        self.play(Transform(Content1,Research))
        self.play(
            #FadeOut(Content1),
            ApplyMethod(Content1.shift,UP*3),
            #Transform(Content1,Study_copy)  Mind the Difference!!
        )

        R2=Tex("电子束光刻工艺的高精度三维仿真研究（国创）",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(DOWN*0.75)
        R1=Tex("基于神经网络的高能效ECG分类算法研究（省创）",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(UP*0.75)
        Teacher1=Tex("指导教师：刘昊",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.5).move_to(UP*0.15)
        Teacher2=Tex("指导教师：周再发",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.5).move_to(DOWN*1.35)
        Proj=Tex("\\emph{Projects:}",color="BLACK").move_to(LEFT*5+UP*2)
        self.play(
            Write(Teacher1),
            Write(Teacher2),
            Write(R1),
            Write(R2),
            Write(Proj),
        )#        conf={

        self.play(Unwrite(R2),Unwrite(Teacher1),Unwrite(Teacher2),Unwrite(Proj),ApplyMethod(R1.scale,0.6))
        self.play(ApplyMethod(R1.to_corner,DOWN+LEFT))
        conf={
            "output_neuron_color": GREEN,
            "input_neuron_color": ORANGE,
            "hidden_layer_neuron_color": RED,
            "neuron_stroke_width": 3,
            "edge_color": BLUE,
            "edge_stroke_width": 3
        }
        nn = NeuralNetworkMobject([7,5,8,10,6,1],**conf).scale(1).move_to(DOWN*0.5+RIGHT*0.7)
        nn.label_inputs('x')
        nn.label_outputs("\hat{y}")
        nn.label_hidden_layers('a')
        # nn.label_outputs_text('Predict')
        self.play(Create(nn),run_time=5)
       # self.wait(10)
        predict=Tex("Predict",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(RIGHT*5+UP*0.5)
        E17c=Tex("17 classes",color="BLACK").scale(0.7).move_to(RIGHT*5+DOWN*0.5)
        RectanPre=Rectangle(color="RED")
        RectanPre.surround(predict)
        ECG=ImageMobject("ECG.png").scale(0.25).move_to(LEFT*5+DOWN*0.5)
        RectanECG=Rectangle(color="BROWN")
        RectanECG.surround(ECG)
        RectanECG.scale(1.2)
        self.play(Write(predict),FadeIn(ECG),Create(RectanECG),Create(RectanPre),Write(E17c))
        self.play(Uncreate(nn),run_time=3)
        CNN=ImageMobject("CNN.jpg").scale(1.5).move_to(DOWN*0.5)
        self.play(Unwrite(E17c),FadeIn(CNN),ApplyMethod(predict.shift,DOWN*1),ApplyMethod(RectanPre.shift,DOWN*1))
        self.play(Uncreate(RectanPre),Uncreate(RectanECG),FadeOut(CNN),Unwrite(predict),FadeOut(ECG))
        
        work_ECG=Tex("\\emph{My work:}",color="BLACK")
        work_ECG.move_to(LEFT*4+UP*1.6)
        mission1=Tex("\\emph{1.} Data processing with normalization",color="BLACK").move_to(UP*0.5).scale(0.7)
        mission2=Tex("\\emph{2.} Developed a CNN model using tensorflow and keras",color="BLACK").scale(0.7).move_to(DOWN*0.5)
        mission3=Tex("\\emph{3.} Designed a quantization compression method",color="BLACK").move_to(DOWN*1.5).scale(0.7)
        self.play(
            Write(work_ECG),
            Write(mission1),
            Write(mission2),
            Write(mission3),
        )
        self.play(
            Unwrite(work_ECG),
            Unwrite(mission1),
            Unwrite(mission2),
            Unwrite(mission3),
            Unwrite(R1),
        )

        Beam=Tex("电子束光刻工艺的高精度三维仿真研究（国创）",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7)
        self.play(Write(Beam))
        #Beam.scale(0.5)
        self.play(ApplyMethod(Beam.scale,0.6))
        self.play(ApplyMethod(Beam.to_corner,DOWN+LEFT))
        matlab=ImageMobject("Matlab_Logo.png").scale(0.4)
        mat=Tex("Matlab",color="RED").scale(1.2).move_to(LEFT*2.5)
        self.play(FadeIn(matlab,shift=DOWN, scale=0.66))
        Monte = Tex("Monte Carlo Simulation",color="BLUE").scale(1.2).move_to(RIGHT*2.3)
        self.play(ApplyMethod(matlab.shift,LEFT*5),Write(mat,reverse=True),Write(Monte),)
        groupofmatlab=VGroup(mat,Monte)
        self.play(FadeOut(matlab),ApplyMethod(groupofmatlab.scale,0.55))
        self.play(ApplyMethod(groupofmatlab.shift,LEFT*5+UP*2))
       
        import numpy as np
        import random as ran
        offset = (-4, -1, 0)

        circle = Circle(radius=2, color=RED)
        circle.move_to(offset)

        square = Rectangle(width=4, height=4,color="BLACK")
        square.move_to(offset)


        self.play(Create(circle),Create(square))

        point_text, point_number = point_label = VGroup(
            Tex("All dot : ",color=BLACK),
            DecimalNumber(
                0,
                show_ellipsis=False,
                num_decimal_places=0,
                color=BLACK
            )
        )

        in_text, in_number = in_label = VGroup(
            Tex("Dot in a circle : ",color=BLACK),
            DecimalNumber(
                0,
                show_ellipsis=False,
                num_decimal_places=0,
                color=BLACK
            )
        )

        pi_text, pi_number = pi_label = VGroup(
            Tex("Pi : ",color="BLACK"),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=4,
                color=BLACK
            )
        )
        point_label.arrange(RIGHT)
        in_label.arrange(RIGHT)
        pi_label.arrange(RIGHT)

        point_label.move_to((2, -2, 0))
        in_label.move_to((2, 0, 0))
        pi_label.move_to((-4, 1.5, 0))

        self.add(pi_label)

        count_all = 0
        c = 0
        apx_pi = 0

        point_number.add_updater(lambda m: m.set_value(count_all))
        in_number.add_updater(lambda m: m.set_value(c))
        pi_number.add_updater(lambda m: m.set_value(apx_pi))
        line2 = Line(UP*2.5+LEFT*1.2,DOWN*3+LEFT*1.2,color="BLACK").set_opacity(0.3)
        self.play(Create(line2))       
        work_b=Tex("\\emph{My work:}",color="BLACK")
        work_b.move_to(RIGHT+UP*2)
        mission1a=Tex("\\emph{1.} Developed an appropriate physical model",color="BLACK").move_to(UP*0.5+RIGHT*2.5).scale(0.7)
        mission2a=Tex("\\emph{2. }Simulated the scattering and energy distribution ",color="BLACK").scale(0.7).move_to(DOWN*0.5+RIGHT*3)
        mission3a=Tex("of electrons in photoresist and substrate",color="BLACK").move_to(DOWN*1.5+RIGHT*2).scale(0.7)
        self.play(
            Write(work_b),
            Write(mission1a),
            Write(mission2a),
            Write(mission3a),
        )
        ran.seed(1)
        for i in range(1001):
            pos = (-6 + ran.random() * 4, -3 + ran.random() * 4, 0)
            if((pos[0] + 4) ** 2 + (pos[1]+1) ** 2 < 4):
                d = Dot(color=RED, radius = 0.04)
                c += 1
            else:
                d = Dot(color=GREEN, radius = 0.04)
            d.move_to(pos)

            self.play(Create(d, run_time=0.005))
            count_all = i
            apx_pi = c/(i+1) * 4
        self.play(
            Unwrite(Beam),
            Unwrite(groupofmatlab),
            Uncreate(circle),
            Uncreate(square),
            Unwrite(work_b),
            Unwrite(mission1a),
            Unwrite(mission2a),
            Unwrite(mission3a),
            Uncreate(line2),
            FadeOut(pi_label),
            Unwrite(R2),
        )
        self.clear()
        self.play(FadeOut(Content1,scale=1.5))

class S2(Scene):
    def construct(self):
        Honors = Text("Honors").scale(1.2)
        for letter in Honors:
            letter.set_color(random_bright_color())

        self.play(FadeIn(Honors,scale=1.5))
        self.play(ApplyMethod(Honors.shift,UP*3))
        jiangxuejin=Tex("\\emph{1. }奖学金",tex_template=TexTemplateLibrary.ctex,color="BLACK").move_to(LEFT*5+UP*1.5)
        self.play(Write(jiangxuejin))
        ho1=MarkupText(
            f'<span fgcolor="{ORANGE}">课程</span><span fgcolor="{BLACK}">奖</span>',
            color=BLACK,
            font_size=34
        ).move_to((-4,0.5,0))
        #ho2=MarkupText(
        #    f'<span fgcolor="{ORANGE}">课程</span><span fgcolor="{BLACK}">奖</span>',
        #    color=BLACK,
        #    font_size=34
        #)
        ho1_1=MarkupText(f'- 数学分析',color=BLACK,font_size=32).move_to((-2,0,0))
        ho1_2=MarkupText(f'- 线性代数',color="BALCK",font_size=32).move_to((1,0,0))
        self.play(
            FadeIn(ho1),
            FadeIn(ho1_1),

        )
