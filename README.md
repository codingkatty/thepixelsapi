# The Pixels API 🟥🟧🟨🟩🟦

![banner](https://i.imgur.com/OSPvgPe.png)

## What is this? 🟥
This is an r/place inspired api made for [raspapi ysws](https://raspapi.hackclub.com/). It's made with flask and it's used to display pixels in a 32x16 grid.

## How to use? 🟧
The API is hosted on Render, here: https://thepixelsapi.onrender.com <br>
You can refer the documentation at https://codingkatty.github.io/thepixelsapi/documentation
<br>

### GET requests 🟨
1. `https://thepixelsapi.onrender.com/image`<br>
This will return a PNG image of the current canvas.

2. `https://thepixelsapi.onrender.com/pixels`<br>
Returns all pixel data, add parameters (x, y or color) to filter.

3. `https://thepixelsapi.onrender.com/trending`<br>
Returns the most recurring color in all pixels along with the number of it.

### POST requests 🟩
1. `https://thepixelsapi.onrender.com/setpixel`<br>
Set a pixel to a color. Content type is application/json and x, y, color are required in the body.

## Why is it slow 🟦
It might be very very slow to load if the Render server goes inactive. It would take around 50 seconds for the server to start and after that it will remain fast.