"""
Plugin utilites for the pictool.

This module contains all of the commands supported by the application script pictool.py.
To be a valid command, a function must (1) have a first parameter 'image' for the
image buffer, (2) assign default values to parameters after the first, and (3)
return True if it modifies the image and False if not.  You can use these rules to
make your own plugin utilities.

Only three four functions -- mono, flip, transpose, and rotate -- are required for this
project.  All others are optional, though the folder 'solutions' does contain examples
for each of them.

IMPORTANT: It is highly recommended that these functions enforce the preconditions for 
any parameter after images.  Otherwise, command line typos may be hard to debug.

Author: Gabriel Wooten
Date: November 28, 2023
"""


# Function useful for debugging
def display(image):
    """
    Returns False after pretty printing the image pixels, one pixel per line.
    
    All plug-in functions must return True or False.  This function returns False 
    because it displays information about the image, but does not modify it.
    
    You can use this function to look at the pixels of a file and see whether the 
    pixel values are what you expect them to be.  This is helpful to analyze a file
    after you have processed it.
    
    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    height = len(image)
    width  = len(image[0])
    
    # Find the maximum string size for padding
    maxsize = 0
    for row in image:
        for pixel in row:
            text = repr(pixel)
            if len(text) > maxsize:
                maxsize = len(text)
    
    # Pretty print the pixels
    print()
    for pos1 in range(height):
        row = image[pos1]
        for pos2 in range(width):
            pixel = row[pos2]
            
            middle = repr(pixel)
            padding = maxsize-len(middle)
            
            prefix = '      '
            if pos1 == 0 and pos2 == 0:
                prefix = '[  [  '
            elif pos2 == 0:
                prefix = '   [  '
            
            suffix = ','
            if pos1 == height-1 and pos2 == width-1:
                suffix = (' '*padding)+' ]  ]'
            elif pos2 == width-1:
                suffix = (' '*padding)+' ],'
            
            print(prefix+middle+suffix)
    
    # This function does not modify the image
    return


# Example function illustrating image manipulation
def dered(image):
    """
    Returns True after removing all red values from the given image.
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. This function sets the red value to 0 for every 
    pixel in the image.
    
    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    # Get the image size
    height = len(image)
    width  = len(image[0])
    
    for row in range(height):
        for col in range(width):
            pixel = image[row][col]
            pixel.red = 0
    
    # This function DOES modify the image
    return True


# IMPLEMENT THESE FOUR FUNCTIONS
def mono(image, sepia=False):
    """
    Returns True after converting the image to monochrome.
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It converts the image to either greyscale or
    sepia tone, depending on the parameter sepia.
    
    If sepia is False, then this function uses greyscale.  For each pixel, it computes
    the overall brightness, defined as 
        
        0.3 * red + 0.6 * green + 0.1 * blue.
    
    It then sets all three color components of the pixel to that value. The alpha value 
    should remain untouched.
    
    If sepia is True, it makes the same computations as before but sets green to
    0.6 * brightness and blue to 0.4 * brightness.
    
    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    
    Parameter sepia: Whether to use sepia tone instead of greyscale
    Precondition: sepia is a bool
    """
    # We recommend enforcing the precondition for sepia
    # Change this to return True when the function is implemented
    # Validate the precondition for sepia
    assert isinstance(sepia, bool), "sepia must be a boolean"
    
    for row in image:
        for pixel in row:
            brightness = int(0.3 * pixel.red + 0.6 * pixel.green + 0.1 * pixel.blue)
            
            pixel.red = pixel.green = pixel.blue = min(brightness, 255)

            if sepia:
                pixel.green = min(int(0.6 * brightness), 255)
                pixel.blue = min(int(0.4 * brightness), 255)
            
            
    return True


def flip(image,vertical=False):
    """
    Returns True after reflecting the image horizontally or vertically.
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. By default it reflects the image horizonally,
    or vertically if vertical is True.
    
    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    
    Parameter vertical: Whether to reflect the image vertically
    Precondition: vertical is a bool
    """
    # We recommend enforcing the precondition for vertical
    height = len(image)
    width = len(image[0])

    # Create a copy of the original image
    original_image = [row[:] for row in image]

    if vertical:
        # Reflect the image vertically
        for row in range(height):
            for col in range(width):
                image[row][col] = original_image[height - 1 - row][col]
    else:
        # Reflect the image horizontally
        for row in range(height):
            for col in range(width):
                image[row][col] = original_image[row][width - 1 - col]

    
    # Change this to return True when the function is implemented
    return True


def transpose(image):
    """
    Returns True after transposing the image
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It transposes the image, swaping colums and rows.
    
    Transposing is tricky because you cannot just change the pixel values; you have
    to change the size of the image table.  A 10x20 image becomes a 20x10 image.
    
    The easiest way to transpose is to make a transposed copy with the pixels from
    the original image.  Then remove all the rows in the image and replace it with
    the rows from the transposed copy.
    
    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    # Get the dimensions of the original image
    original_height = len(image)
    original_width = len(image[0])

    # Create a transposed copy of the original image
    transposed_image = [[image[row][col] for row in range(original_height)] for col in range(original_width)]

    # Update the dimensions of the image
    image.clear()
    for row in range(original_width):
        image.append([transposed_image[row][col] for col in range(original_height)])

    # Change this to return True when the function is implemented
    return True


def rotate(image,right=False):
    """
    Returns True after rotating the image left of right by 90 degrees.
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. By default it rotates the image left, or right
    if parameter right is True.
    
    To rotate left, transpose and then flip vertically.  To rotate right, flip
    vertically first and then transpose.
    
    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    
    Parameter right: Whether to rotate the image right
    Precondition: right is a bool
    """
    # Get the dimensions of the original image
    original_height = len(image)
    original_width = len(image[0])

    if right:
        # Rotate right: flip vertically first and then transpose
        flip(image, vertical=True)
        transpose(image)
    else:
        # Rotate left: transpose and then flip vertically
        transpose(image)
        flip(image, vertical=True)

    return True


# ADVANCED OPTIONAL FUNCTIONS
def vignette(image):
    """
    Returns True after vignetting (corner darkening) the current image.
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It simulates vignetting, which is a characteristic 
    of antique lenses. This plus sepia tone helps give a photo an antique feel.
    
    To compute the vignette, you must compute the distance of each pixel from the
    center.  For any two pixels at position (r0,c0) and (r1,c1), the distance between
    the two is
        
        dist( (r0,c0), (r1,c1)) = sqrt( (r0-r1)*(r0-r1)+(c0-c1)*(c0-c1) )
    
    The vignette factor for a pixel at row r, col r is
        
        1 - (d / H)^2
    
    where d is the distance from the pixel to the center of the image and H (for the
    half diagonal) is the distance from the center of the image to a corner. To 
    vignette an image, multiply each NON-ALPHA color value by its vignette factor.
    The alpha value should be left untouched.
    
    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    import math
    # Get the dimensions of the image
    height = len(image)
    width = len(image[0])

    # Find the center of the image
    center_row = height // 2
    center_col = width // 2

    # Find the half diagonal distance
    half_diagonal = math.sqrt(center_row ** 2 + center_col ** 2)

    # Apply vignette effect
    for row in range(height):
        for col in range(width):
            # Calculate distance from the center
            distance = math.sqrt((row - center_row) ** 2 + (col - center_col) ** 2)

            # Calculate vignette factor
            vignette_factor = 1 - (distance / half_diagonal) ** 2

            # Apply vignette factor to non-alpha color values
            pixel = image[row][col]
            if pixel.alpha < 255:  # Check if there is any transparency
                pixel.red = int(pixel.red * vignette_factor)
                pixel.green = int(pixel.green * vignette_factor)
                pixel.blue = int(pixel.blue * vignette_factor)

    return True

def blur(image,radius=5):
    """
    Returns True after bluring the image.
    
    To blur an image you loop over all pixels.  For each pixel, you average all colors
    (all 4 values including alpha) in a box centered at the pixel with the given radius.
    For example, suppose you are blurring the pixel at position (4,7) with a radius 2
    blur.  Then you will average the pixels at positions (2,5), (2,6), (2,7), (2,8), 
    (2,9), (3,5), (3,6), (3,7), (3,8), (3,9), (4,5), (4,6), (4,7), (4,8), (4,9), (5,5),
    (5,6), (5,7), (5,8), (5,9), (6,5), (6,6), (6,7), (6,8), and (6,9).  You then assign
    that average value to the pixel.
    
    If the box goes outside of the image bounds, go to the edge of the image.  So if you
    are blurring the pixel at position (0,1) with a radius 2, you average the pixels
    at positions (0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (1,3), (2,0), (2,1), 
    (2,2), and (2,3).
    
    This calculation MUST be done in a COPY.  Otherwise, you are using the blurred 
    value in future pixel computations (e.g. when you try to blur the pixel to the 
    right of it).  All averages must be computed from the original image.  Use the 
    steps from transpose() to modify the image.
    
    WARNING: This function is very slow (Adobe's programs use much more complicated
    algorithms and are not written in Python).  Blurring 'Walker.png' with a radius 
    of 30 can take up to 10 minutes.
    
    Parameter image: The image to blur
    Precondition: image is a 2d table of RGB objects
    
    Parameter radius: The blur radius
    Precondition: radius is an int > 0
    """
    # We recommend enforcing the precondition for radius
    # Get the dimensions of the image
    import introcs
    height = len(image)
    width = len(image[0])

    # Create a copy of the original image
    blurred_image = [[introcs.RGB(0, 0, 0, 0) for _ in range(width)] for _ in range(height)]

    # Loop over each pixel in the original image
    for row in range(height):
        for col in range(width):
            # Variables to calculate the average color values
            total_red = 0
            total_green = 0
            total_blue = 0
            total_alpha = 0
            count = 0

            # Loop over the surrounding pixels within the specified radius
            for i in range(-radius, radius + 1):
                for j in range(-radius, radius + 1):
                    # Calculate the coordinates of the surrounding pixel
                    new_row = max(0, min(row + i, height - 1))
                    new_col = max(0, min(col + j, width - 1))

                    # Get the color values of the surrounding pixel
                    pixel = image[new_row][new_col]
                    total_red += pixel.red
                    total_green += pixel.green
                    total_blue += pixel.blue
                    total_alpha += pixel.alpha
                    count += 1

            # Calculate the average color values
            average_red = total_red // count
            average_green = total_green // count
            average_blue = total_blue // count
            average_alpha = total_alpha // count

            # Assign the average color values to the corresponding pixel in the copy
            blurred_image[row][col] = introcs.RGB(average_red, average_green, average_blue, average_alpha)

    # Update the original image with the blurred copy
    for row in range(height):
        for col in range(width):
            image[row][col] = blurred_image[row][col]

    return True



def pixellate(image,step=10):
    """
    Returns True after pixellating the image.
    
    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It pixellates the image to give it a blocky feel. 
    
    To pixellate an image, start with the top left corner (e.g. the first row and column).  
    Average the colors (all 4 values including alpha) of the step x step block to the
    right and down from this corner.  For example, if step is 3, you will average the
    colors at positions (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), and (2,2).
    After computing the averages, assign each color's (and the alpha's) average value
    to ALL the pixels in the block.
    
    If there are less than step rows or step columns, go to the edge of the image.  So
    on a image with 2 rows and 4 columns, a step 3 pixellate would process the colors
    at positions  (0,0), (0,1), (0,2), (1,0), (1,1), and (1,2).
    
    When you are done, skip over step columns to get the the next corner pixel, and 
    repeat  this process again.  Because the blocks do not overlap, it is not necessary 
    to create a copy (like blur). You can reassign the pixels before moving to the next 
    block. For example, suppose step is 3. Then the next block is at position (0,3) and 
    includes the pixels at (0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), 
    and (2,5).  
    
    Continue the process looping over rows and columns to get a pixellated image.
    
    Parameter image: The image to pixelate
    Precondition: image is a 2d table of RGB objects
    
    Parameter step: The number of pixels in a pixellated block
    Precondition: step is an int > 0
    """
    # We recommend enforcing the precondition for step
    # Get the dimensions of the image
    height = len(image)
    width = len(image[0])
    
    for row in range(0, height, step):
        for col in range(0, width, step):
            # Compute the average color values for the block
            avg_red = 0
            avg_green = 0
            avg_blue = 0
            avg_alpha = 0
            count = 0
            
            for i in range(min(step, height - row)):
                for j in range(min(step, width - col)):
                    pixel = image[row + i][col + j]
                    avg_red += pixel.red
                    avg_green += pixel.green
                    avg_blue += pixel.blue
                    avg_alpha += pixel.alpha
                    count += 1
            
            # Calculate the average values
            avg_red //= count
            avg_green //= count
            avg_blue //= count
            avg_alpha //= count
            
            # Update all pixels in the block with the average values
            for i in range(min(step, height - row)):
                for j in range(min(step, width - col)):
                    pixel = image[row + i][col + j]
                    pixel.red = avg_red
                    pixel.green = avg_green
                    pixel.blue = avg_blue
                    pixel.alpha = avg_alpha
    
    return True
