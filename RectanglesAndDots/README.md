# The Problem

![img.png](img.png)

Suppose I have a finite evenly spaced (on both axes) grid of points on a plane (blue) and there are also "forbidden points" (green) that can be placed anywhere within this grid.

I want to draw axis-aligned rectangles around the blue points but not the green forbidden points.

How do I find the minimum number of rectangles it would take to enclose all the blue points?

# Possible Approaches
* Brute force: Put rectangles around each point, and stochastically pick pairs of rectangles to merge.

# Results
## First attempt at brute force
Install dependencies with `pip3 install -r requirements.txt`
Run `python3 demo.py`
