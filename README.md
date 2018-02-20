# Edge Detection

A program which finds and highlights the edges in an image using differences in colour values.  

The function which processes the images, `find_edges` accepts a variety of modes listed below.

### Modes Table
| Original                                          | Gradient Black (grad_black)                 |
|:-------------------------------------------------:|:----------------------------------------------:|
|![Original image](https://i.imgur.com/S5ACk9W.jpg) | ![grad_black](https://i.imgur.com/rgg0wKL.jpg) |
| Original                                          | Gradient White (on_white)                   |
|![Original image](https://i.imgur.com/S5ACk9W.jpg) | ![on_white](https://i.imgur.com/OEqrsDZ.jpg)   |
| Original                                          | Gradient Overlayed on Original (overlay)       |
|![Original image](https://i.imgur.com/S5ACk9W.jpg) | ![overlay](https://i.imgur.com/6EtNgqd.jpg)    |


## How it Works
Example using grad_black:
1. Find image using tkinter dialog, open using Pillow (PIL).
2. Create blank image (black background) with same width and height as original image.
3. Split bounds of image into quarters, create 4 worker threads which asyncronously perform `compare_pixels` function on each quarter; Creates 4 image objects (one per quarter).
4. `compare_pixels` function sums RGB values of a pixel and subtracts the sum of the next pixel's RGB values (to the right). If the `difference` is greater than the `threshold` (specified by user), colour the corresponding pixel on the quarter image. The RGB values of the corresponding pixel is (`difference`, `difference`, `difference`).
5. `compare_pixels` repeats the same method, comparing pixels vertically (pixel vs. pixel below).
6. Each quarter image is pasted onto the output image. The output image is then saved (with optional `name` specified by user).

## Built With

* Pillow Image Library - Used to open, modify, and save images.
* ThreadPool - Used to divide image among worker threads to speed up image processing.
* tkinter - Used to open native file dialog to select image.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
