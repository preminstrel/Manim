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
        title = Tex("\\textbf{?????????????????????}", tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(1.7)
        author = Tex("06219109 ?????????", tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).shift(DOWN)
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

        Content1 = Tex("??????\quad Study",tex_template=TexTemplateLibrary.ctex,color="BLACK")
        Content2 = Tex("??????\quad Research",tex_template=TexTemplateLibrary.ctex,color="BLACK")
        Content3 = Tex("??????\quad Honors",tex_template=TexTemplateLibrary.ctex,color="BLACK")
        Content4 = Tex("??????\quad Life",tex_template=TexTemplateLibrary.ctex,color="BLACK")
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
        Major = Tex("Major\qquad ?????????????????????????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.9).move_to(UP*0.8+RIGHT*1.8)
        Name = Tex("Name\qquad ?????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.9)
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
        self.wait(4)
        # END of Page 2

        self.play(
            FadeOut(title),
            FadeOut(Content4),
            FadeOut(Content2),
            FadeOut(Content3),
        )
        Study = Text("Study",gradient=(PINK, GREEN, ORANGE)).scale(1.2)
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
        maths=Tex("????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+UP*1.7)
        rectan1=Rectangle(color="BLUE")
        rectan1.surround(maths,buff=0.35)
        #group1 = VGroup(maths,rectan1)
        s1=Tex("99",color="BLACK").move_to(LEFT*2.5+UP*1.7)
        rec1=Circle(color="BLUE")
        rec1.surround(s1)

        linear_a=Tex("????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+UP*0.5)
        rectan2=Rectangle(color="BROWN")
        rectan2.surround(linear_a,buff=0.35)
        #group2=VGroup(linear_a,rectan2)
        s2=Tex("98",color="BLACK").move_to(LEFT*2.5+UP*0.5)
        rec2=Circle(color="BROWN")
        rec2.surround(s2)

        Phy=Tex("????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+DOWN*0.7)
        rectan3=Rectangle(color="GRAY")
        rectan3.surround(Phy,buff=0.35)
        #group3 = VGroup(Phy,rectan3)
        s3 = Tex("98",color="BLACK").move_to(LEFT*2.5+DOWN*0.7)
        rec3=Circle(color="GRAY")
        rec3.surround(s3)
        
        C=Tex("????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(LEFT*4+DOWN*1.9)
        rectan4=Rectangle(color="GOLD")
        rectan4.surround(C,buff=0.35)
        group3=VGroup(Phy,C)
        s4=Tex("97",color="BLACK").move_to(LEFT*2.5+DOWN*1.9)
        rec4=Circle(color="GOLD")
        rec4.surround(s4)
        
        maths1=Tex("????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(RIGHT*1.5+UP*1.7)
        rectan5=Rectangle(color="BLUE")
        rectan5.surround(maths1,buff=0.35)
        #group1 = VGroup(maths,rectan1)
        s5=Tex("99",color="BLACK").move_to(RIGHT*4+UP*1.7)
        rec5=Circle(color="BLUE")
        rec5.surround(s5)
  
        Signal=Tex("???????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(RIGHT*1.56+UP*0.5)
        rectan7=Rectangle(color="BROWN")
        rectan7.surround(Signal,buff=0.30)
        #group2=VGroup(linear_a,rectan2)
        s7=Tex("95",color="BLACK").move_to(RIGHT*4+UP*0.5)
        rec7=Circle(color="BROWN")
        rec7.surround(s7)       
        
        Complexf=Tex("????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(RIGHT*1.5+DOWN*1.9)
        rectan8=Rectangle(color="GOLD")
        rectan8.surround(Complexf,buff=0.35)
        #group4=VGroup(Phy,C)
        s8=Tex("98",color="BLACK").move_to(RIGHT*4+DOWN*1.9)
        rec8=Circle(color="GOLD")
        rec8.surround(s8)
        
        gtwl=Tex("????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(RIGHT*1.5+DOWN*0.7)
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

        Research = Text("Research",gradient=(RED, BLUE, GREEN)).scale(1.2)
        #for letter in Research:
        #    letter.set_color(random_bright_color())
        self.play(Transform(Content1,Research))
        self.play(
            #FadeOut(Content1),
            ApplyMethod(Content1.shift,UP*3),
            #Transform(Content1,Study_copy)  Mind the Difference!!
        )

        R2=Tex("???????????????????????????????????????????????????????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(DOWN*0.75)
        R1=Tex("??????????????????????????????ECG??????????????????????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7).move_to(UP*0.75)
        Teacher1=Tex("?????????????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.5).move_to(UP*0.15)
        Teacher2=Tex("????????????????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.5).move_to(DOWN*1.35)
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
        self.wait(13)
        self.play(Uncreate(RectanPre),Uncreate(RectanECG),FadeOut(CNN),Unwrite(predict),FadeOut(ECG))
        #self.wait(15) 
        work_ECG=Tex("\\emph{My work:}",color="BLACK")
        work_ECG.move_to(LEFT*4+UP*1.6)
        mission1=Tex("\\emph{1.} Data processing with normalization",color="BLACK").move_to(UP*0.5).scale(0.7)
        mission2=Tex("\\emph{2.} Developed a CNN model using Pytorch",color="BLACK").scale(0.7).move_to(DOWN*0.5)
        mission3=Tex("\\emph{3.} Designed an Adaptive Loss-aware Multi-bit Networks Quantization method",color="BLACK").move_to(DOWN*1.5).scale(0.7)
        self.play(
            Write(work_ECG),
            Write(mission1),
            Write(mission2),
            Write(mission3),
        )
        self.wait(13)
        self.play(
            Unwrite(work_ECG),
            Unwrite(mission1),
            Unwrite(mission2),
            Unwrite(mission3),
            Unwrite(R1),
        )

        Beam=Tex("???????????????????????????????????????????????????????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").scale(0.7)
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
        do = SVGMobject("document.svg").scale(3.5).move_to((-3,0,0))
        document1 = Tex("Published by IEEE",color="BLACK").move_to((3,1.5,0))
        document2 = Tex("EI Compendex, CPCI, SCOPUS",color = "BLACK").scale(0.9).move_to((3.5,0,0))
        document3 = Tex("First Author",color = "BLACK").move_to((3,-1.5,0))
        self.play(FadeIn(do),Write(document1),Write(document2),Write(document3))
        self.wait(8)
        self.play(FadeOut(do),Unwrite(document1),Unwrite(document2),Unwrite(document3)) 
        Honors = Text("Honors",gradient=(ORANGE, RED, BLUE)).scale(1.2)

        self.play(FadeIn(Honors,scale=1.5))
        self.play(ApplyMethod(Honors.shift,UP*3))
        jiangxuejin=Tex("\\emph{1. }?????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").move_to(LEFT*5+UP*1.5)
        self.play(Write(jiangxuejin))
        ho1=MarkupText(
            f'<span fgcolor="{ORANGE}">??????</span><span fgcolor="{BLACK}">???</span>',
            color=BLACK,
            font_size=34
        ).move_to((-4,0.5,0))
        #ho2=MarkupText(
        #    f'<span fgcolor="{ORANGE}">??????</span><span fgcolor="{BLACK}">???</span>',
        #    color=BLACK,
        #    font_size=34
        #)
        ho1_1=MarkupText(f'- ????????????',color=BLACK,font_size=32).move_to((-2,-0.5,0))
        ho1_2=MarkupText(f'- ????????????',color=BLACK,font_size=32).move_to((1,-0.5,0))
        ho1_3=MarkupText(f'- CET-4' ,color=BLACK,font_size=32).move_to((-2.2,-1.5,0))
        ho1_4=MarkupText(f'- ????????????',color=BLACK,font_size=32).move_to((1,-1.5,0))
        ho1_5=MarkupText(f'??????',color=BLACK,font_size=32).move_to((-2.5,-2.5,0))
        self.play(
            FadeIn(ho1),
            FadeIn(ho1_1),
            FadeIn(ho1_2),
            FadeIn(ho1_3),
            FadeIn(ho1_4),
            FadeIn(ho1_5),
        )
        self.wait(2)
        ho2=MarkupText(
            f'<span fgcolor="{BLUE}">??????</span><span fgcolor="{BLACK}">?????????</span>',
            color=BLACK,
            font_size=34
        ).move_to((-4,0.5,0))
        #ho2=MarkupText(
        #    f'<span fgcolor="{ORANGE}">??????</span><span fgcolor="{BLACK}">???</span>',
        #    color=BLACK,
        #    font_size=34
        #)
        ho2_1=MarkupText(f'- <span fgcolor="{LIGHT_BROWN}">686??????</span>?????????',color=BLACK,font_size=32).move_to((-2,-0.5,0))
        ho2_2=MarkupText(f'- <span fgcolor="{RED}">????????????</span>?????????',color=BLACK,font_size=32).move_to((-2,-1.5,0))
       
        ho2_3=ImageMobject("686.jpg").scale(0.2).move_to(RIGHT*2+DOWN)
        
        ho2_4=ImageMobject("zb.jpg").scale(0.2).move_to(RIGHT*5+DOWN)
        self.play(
            Transform(ho1,ho2),
            Transform(ho1_1,ho2_1),
            Transform(ho1_3,ho2_2),
            FadeOut(ho1_2,scale=1.3),
            FadeOut(ho1_4,scale=1.3),
            FadeOut(ho1_5),
            FadeIn(ho2_3,scale=0.3),
            FadeIn(ho2_4,scale=0.3)
        )
        self.wait(3)
        sanhaosheng=Tex("\\emph{2. }????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").move_to(LEFT*5+UP*1.5)
        ho3=MarkupText(
            f'<span fgcolor="{BLUE}">????????????</span><span fgcolor="{BLACK}">???????????????</span>',
            color=BLACK,
            font_size=34
        ).move_to((-4.2,0,0))
        ho4=MarkupText(
            f'<span fgcolor="{ORANGE}">????????????</span><span fgcolor="{BLACK}">??????????????????????????????</span>',
            color=BLACK,
            font_size=34
        ).move_to((-3,-1.8 ,0))
        #ho4_1=MarkupText(f'- <span fgcolor="{LIGHT_BROWN}">686??????</span>?????????',color=BLACK,font_size=32).move_to((-2,-0.5,0))
        #ho4_2=MarkupText(f'- <span fgcolor="{RED}">????????????</span>?????????',color=BLACK,font_size=32).move_to((-2,-1.5,0))
       
        ho4_1=ImageMobject("2.jpg").scale(0.2).move_to(RIGHT*3+UP*0.5).rotate(-PI/2)
        
        ho4_2=ImageMobject("1.jpg").scale(0.2).move_to(RIGHT*3+DOWN*2.2).rotate(-PI/2)
        self.play(
            FadeOut(ho1,sacle=0.5),
            Transform(jiangxuejin,sanhaosheng),
            Transform(ho1_1,ho3),
            Transform(ho1_3,ho4),
            Transform(ho2_3,ho4_1),
            Transform(ho2_4,ho4_2)
        )

        youxuesheng=Tex("\\emph{3. }???????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").move_to(LEFT*4.7+DOWN*3.2)

        self.play(Write(youxuesheng))
        self.wait(6) 
### START of LIFE
        Life = Text("Life",gradient=(RED, BLUE, GREEN)).scale(1.2)
        self.play(
            FadeOut(youxuesheng),
            FadeOut(ho1_1),
            FadeOut(ho1_3),
            FadeOut(ho2_3),
            FadeOut(ho2_4),
            Unwrite(jiangxuejin)
        )
        self.play(Transform(Honors,Life))
        self.play(ApplyMethod(Honors.shift,UP*3))
        uni=Tex("\\emph{1. }????????????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").move_to(LEFT*4+UP*2)
        
        uni_d=MarkupText(f'???????????????<span fgcolor="{BLUE}">???????????????</span>',color=BLACK,font_size=34).move_to((-3,0.5,0))
        ui_d2=MarkupText(f'???????????????<span fgcolor="{ORANGE}">??????????????????</span>',color=BLACK,font_size=34).move_to((-2.9,-1,0))
        ui_p1=ImageMobject("l.jpeg").move_to((3,1,0)).scale(0.5)
        ui_p2=ImageMobject("k.jpeg").move_to((3,-2.3,0)).scale(0.57)
        self.play(Write(uni),FadeIn(uni_d),FadeIn(ui_d2),FadeIn(ui_p1),FadeIn(ui_p2))
        self.wait(6)
        jingsai=Tex("\\emph{2. }??????",tex_template=TexTemplateLibrary.ctex,color="BLACK").move_to(LEFT*5.5+UP*2)
        Rob=MarkupText(f'- <span fgcolor="{GRAY}">Rob</span>Cup',color=BLACK,font_size=34).move_to((-4,1,0))
        mathcomp = MarkupText(f'- <span fgcolor="{BLUE}">??????</span>??????',color=BLACK,font_size=34).move_to((-4,0.1,0))
        veh= MarkupText(f'- <span fgcolor="{ORANGE}">?????????</span>??????',color=BLACK,font_size=34).move_to((-4,-1.7,0))
        code= MarkupText(f'- <span fgcolor="{LIGHT_BROWN}">??????</span>??????',color=BLACK,font_size=34).move_to((-4,-0.8,0))
        dots=Tex("$\\cdots \\cdots$",color="BLACK").move_to((-4,-2.6 ,0))
        com_p1=ImageMobject("9.jpg").move_to((3,1,0)).scale(0.2).rotate(-PI/2)
        com_p2=ImageMobject("6.jpg").move_to((3,-2,0)).scale(0.2).rotate(-PI/2)
        self.play(
            Transform(uni,jingsai),
            FadeOut(uni_d,scale=0.3),
            FadeIn(Rob,scale=1.3),
            FadeOut(ui_d2,scale=0.3),
            FadeIn(mathcomp,scale=1.3),
            FadeIn(veh,scale=1.3),
            FadeIn(code,scale=1.3),
            Write(dots),
            FadeOut(ui_p1),
            FadeOut(ui_p2),
            FadeIn(com_p1,scale=1.5),
            FadeIn(com_p2,scale=1.5)
        )
        self.wait(1)
        shehui=Tex("\\emph{3. }????????????",tex_template=TexTemplateLibrary.ctex,color="BLACK").move_to(LEFT*4.5+UP*2)
        sp=ImageMobject("s.jpg").move_to((3,-0.7,0)).scale(1.2)
        sd1=MarkupText(f'- <span fgcolor="{LIGHT_BROWN}">????????????</span>???',color=BLACK,font_size=34).move_to((-4,0,0))
        sd2=MarkupText(f'- <span fgcolor="{RED}">???????????????</span>??????',color=BLACK,font_size=34).move_to((-4,-1,0))
        sd3=MarkupText(f'- <span fgcolor="{GREEN}">??????</span>?????????',color=BLACK,font_size=34).move_to((-4,-2,0))
        #self.wait(3)

        self.play(
            Transform(uni,shehui),
            FadeIn(sp),
            FadeOut(com_p1,scale=1.5),
            FadeOut(com_p2,scale=1.5),            
            FadeOut(Rob,scale=1.3),
            #FadeOut(ui_d2,scale=0.3),
            FadeOut(mathcomp,scale=1.3),
            FadeOut(veh,scale=1.3),
            FadeOut(code,scale=1.3),
            Unwrite(dots),
            FadeIn(sd1),
            FadeIn(sd2),
            FadeIn(sd3),
        )
        self.wait(2)
        self.play(
            FadeOut(sd1),
            FadeOut(sd2),
            FadeOut(sd3),
            FadeOut(sp),
            Unwrite(uni),
        )
        #self.wait(3)
        fin= Text("Fin.", slant=ITALIC,color=BLACK).scale(1.2)
        self.play(Transform(Honors,fin))
        Thanks=Tex("Thank you",color=BLACK).scale(2.5)
        self.play(ApplyMethod(Honors.shift,UP*3),Write(Thanks))

        #contact = Tex("Contact me").scale(2)
        #contact.move_to(UP*3)
        github = Tex("https://github.com/preminstrel",color=BLACK).scale(0.5)
        github.move_to((-3,-3,0))
        mail = Tex("preminstrel@gmail.com",color=BLACK).scale(0.5)
        mail.move_to((3,-3,0))
        github_png = ImageMobject("Github.png").scale(0.05)
        github_png.move_to((-3,-3,0))
        mail_svg = SVGMobject("Gmail.svg").scale(0.25)
        mail_svg.move_to((3,-3,0))
        
        self.play(Create(mail_svg),FadeIn(github_png))
        self.play(mail_svg.animate.shift(LEFT*1.75),github_png.animate.shift(LEFT*1.75))
        github.next_to(github_png, RIGHT,buff = 0.5)
        mail.next_to(mail_svg,RIGHT,buff = 0.5)
        self.play(Write(mail),Write(github))
        self.wait(13)


