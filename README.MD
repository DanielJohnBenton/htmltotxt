# Convert static HTML files to plain text

`*.html` and `*.htm` files are converted to `.txt`, (hopefully) keeping only the visible text.

Converts recursively and preserves paths, so if you use:

```
> py htmltotxt.py convert
Converting files...
[||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||] 7
Done.
```

`convert/` (input) tree:

```
+---convert
|   |   index.html
|   |   robots.txt
|   |   style.css
|   |   z.png
|   |
|   +---admin
|   |       LOGIN.HTM
|   |       PANEL.HTM
|   |
|   +---downloads
|   |       pwned_message.txt
|   |       virus.exe
|   |
|   +---shop
|           background.jpeg
|           checkout.html
|           item1.html
|           item2.html
|           shopping_cart.htm
```

`htmltotxt_converted/` (output) tree:

```
+---htmltotxt_converted
    |   index.html.txt
    |
    +---admin
    |       LOGIN.HTM.txt
    |       PANEL.HTM.txt
    |
    +---downloads
    +---shop
            checkout.html.txt
            item1.html.txt
            item2.html.txt
            shopping_cart.htm.txt
```

## Technology used

* Python 3
* Built-in modules: math, sys, os, shutil
* Third-party libraries: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [FTFY](https://github.com/LuminosoInsight/python-ftfy)