# Manim

@ author Hanshi Sun

## 1 Video rendering

### 1.1 Command line flags

``` bash
$ manim scene.py test -s -pql
```

- `-p` means preview/play, which can display the rendered video.
- `-ql` means low quality (480P15)
- `-qm` means medium quality (720P30)
- `-qh` means high quality (1080P60)  **DEFAULT**
- `-qp` (1440P60)
- `-qk` (2160P60)
- `-s` means saving the last frame 

## 2 Mobjects

Mobjects are the basic building block for all manim animations. For an instance,  `Circle`, `Arrow` and `Rectangle` are mojects. Moreover, `Axes`,`FucntionGraph` or `BarChart` are mojects, too.

### 2.1 Position-related Methods

`add()` and `remove()` are basic methods.

`Create()` and `FadeOut()` are advanced methods which have anime effect.

#### 2.1.1 `shift()`

`shift()` method is designed to adjust the position of the mobjects. By default, mobjects are placed at *the center of coordinates*, or *origin*, when they are first created. The codes below express that the circle is shifted 2 units UP. 

``` python
circle.shift(UP * 2)
square = Square().shift(LEFT)
```

#### 2.1.2 `move_to()` and `next_to()`

`move_to()` method uses *absolute units* (measured relative to the `ORIGIN`), while `next_to` uses *relative units* (measured from the mobject passed as the first argument). The difference with `move_to` is that `next_to` represents the distance of the boundary, not the center distance.

```python
        # place the circle two units left from the origin
        circle.move_to(LEFT * 2)
        # place the square to the left of the circle
        square.next_to(circle, LEFT)
        # align the left border of the triangle to the left border of the circle
        triangle.align_to(circle, LEFT)
```

#### 2.1.3 Mobject on-screen order

``` python
self.add(triangle, square, circle)
self.add(circle, square, triangle)
```

The former creates triangle, square and circle in order while the latter creates circle, square and triangle in order.

#### 2.1.4 `rotate()`

```python
square.rotate(PI/4)
```

### 2.2 Styling mobjects

#### 2.2.1 `set_stroke` and `set_fill`

```python
        circle.set_stroke(color=GREEN, width=20)
        square.set_fill(YELLOW, opacity=1.0)
```

he former changes the visual style of the mobject’s *border* while the latter changes the style of the *interior*. 

#### 2.2.2 `scale()`

```python
dot1 = Dot()
dot1.scale(3)
```



### 2.3 Animation

At the heart of manim is animation. Generally, you can add an animation to your scene by calling the `play()` method.

#### 2.3.1 `FadeIn()` and `FadeOut()`

#### 2.3.2 `Rotate()`

```python
self.play(Rotate(square, PI/4))
```

#### 2.3.3 `ApplyMethod()`

```python
# animate the change of color
self.play(ApplyMethod(square.set_fill, WHITE))
# animate the change of position
self.play(ApplyMethod(square.shift, UP))
```

For example, `ApplyMethod(square.shift, UP)` executes `square.shift(UP)`, but animates it instead of applying it immediately.

#### 2.3.4 `run_time`

```python
self.play(ApplyMethod(square.shift, UP), run_time=3)
```

#### 2.3.5 `GrowFromCenter()`

```python
self.play(GrowFromCenter(circle))
```

#### 2.3.6 `Transform()`

```python
self.play(Transform(dot, dot2))
```

#### 2.3.7 `MoveAlongPath()`

```python
self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
```

#### 2.3.8 `rate_func`

3 values：

 `there_and_back` just there and back

`linear ` change as a linear speed

`smooth` The speed of change will start from 0 and increase, decreasing while it will get to the goal.

#### 2.3.9 `Rotating()`

```python
self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
```

#### 2.3.10 `Transform() ` and `ReplacementTransform()`

- Same: Same effect
- Difference: `Transform()` shows object1 while `ReplacementTransform()` shows object2.

### 3 Parts

circle:	`Circle(radius=1, color=BLUE)`

dots: 	`Dot([-2, -3, 0])`			

lines:	`Line(dot.get_center(),dot2.get_center()).set_color(ORANGE)`

brace:

```python
b1 = Brace(line,direction = line.copy().rotate(PI/2).get_unit_vector())
b1text = b1.get_text("Hello")
```

arrow:	`Arrow(ORIGIN, [2, 2, 0], buff=0)`

numberplane:	`NumberPlane()`

framebox:	`SurroundingRectangle(text[1], buff = .1)`

MathTex

> The format of formulas in Latex, we can use Latex syntax inside it.

#### syntax

```python
text = MathTex("\\left\\{ \\begin{aligned} &\\mu a^2+b^2=c^2 \\\ &a = 0 \\end{aligned}\\right.") 
```

```python
text = MathTex( r"\left\{ \begin{aligned} &\mu a^2+b^2=c^2 \\ &a = 0 \end{aligned}\right.")
```

> Obviously, "r" can be used to fix the redundant \ \.

### Tex

> The format of  words in Latex, which I don't know how to realize the Chinese.

### Text

> Just text, we can easily format fonts.

