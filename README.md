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


## Usage

to do.

## Built With

* Pillow Image Library - Used to open, modify, and save images.
* ThreadPool - Used to divide image among worker threads to speed up image processing.
* tkinter - Used to open native file dialog to select image.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
