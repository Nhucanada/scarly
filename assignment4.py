import skimage.io as io
import numpy as np
import hashlib
import doctest

class ImageAnalysis:
    def __init__(self,image):
        """Attributes: imageName, shape, hash value"""
        self.imageName = image
        self.image = io.imread(image).astype(np.uint8)
        self.hash = self.find_hash(self.image)
        self.hiddenImage = None
        
    def find_hash(self,image):
        """Find hash value of image"""
        array = image.tobytes()
        return hashlib.sha256(array).hexdigest()
    
    def show(self):
        """Display image on screen"""
        io.imshow(self.image)
        io.show()
        
    def __str__(self):
        """Returns specific message when printing
        obj type ImageAnalysis
        >>> i = ImageAnalysis("mountain.png")
        >>> print(i)
        Analyzing mountain.png of size 9144576 and hash 8c06003d2a866e67614708b8cdc0855d9977d287135465dcb3a8c108f4c52a4d"""
        message = "Analyzing " + self.imageName + " of size " + \
                  str(self.image.size) + " and hash " + self.hash
        return message
     
    def retrieveHidden(self):
        """Extract hidden image from image and save info
        >>> i = ImageAnalysis("mountain.png")
        >>> i.retrieveHidden()
        '1022e57ccb69e79c6abbe7e529230a9ad691baa923607dde667582b7266ea5de'
        """
        # Define hidden image attributes
        hide_shape = 131, 100, 3
        
        # create array of zeros of same shape as hidden image
        self.hiddenImage = np.zeros((hide_shape), dtype = np.uint8)
        
        # Extract hidden image, in every 11 pixels (column major)
        for i in range(hide_shape[0]):
            for j in range(hide_shape[1]):
                image_row = i * 11
                image_col = j * 11
                self.hiddenImage[i,j] = self.image[image_row, image_col]
        
        io.imsave("hidden.jpg", self.hiddenImage)
        return self.find_hash(self.hiddenImage)
    
    def show_hidden(self):
        """Display hidden image if retriveHidden is run first
            raise error otherwise
        >>> i = ImageAnalysis("mountain.png")
        >>> i.show_hidden()
        Traceback (most recent call last):
        ...
        ValueError: Hidden image has not yet been recovered
        """
        if self.hiddenImage is None: #self.hiddenImage is not defined
            raise ValueError("Hidden image has not yet been recovered")
        
        io.imshow(self.hiddenImage)
        io.show()
    
    def fix(self):
    """Fix the image by sampling colours from surrounding 4 pixels
    >>> i = ImageAnalysis("mountain.png")
    """
    fixed = self.image.copy()
    hide_shape = 131, 100, 3

    for i in range(hide_shape[0]):
        for j in range(hide_shape[1]):
            row, col = i * 11, j * 11
            nearby = []

            if row > 0:  # Pixel Above
                nearby.append(fixed[row - 1, col])
            if row < fixed.shape[0] - 1:  # Pixel Below
                nearby.append(fixed[row + 1, col])
            if col > 0:  # Pixel to Left
                nearby.append(fixed[row, col - 1])
            if col < fixed.shape[1] - 1:  # Pixel to Right
                nearby.append(fixed[row, col + 1])

            if nearby:
                patch = np.mean(nearby, axis=0).astype(np.uint8)
                fixed[row, col] = patch

    self.fixed = fixed
    io.imsave("mountain_fixed.jpg", self.fixed)

    # Return hash of the fixed image
    self.hash = self.find_hash(self.fixed)
    return self.hash
    
    def __eq__(self,other):
        """compares two image obj based on hash value
        >>> original = ImageAnalysis("mountain.png")
        >>> fixed = ImageAnalysis("mountain_fixed.jpg")
        >>> print(original == fixed)
        False
        """
        return self.hash == other.hash

    def averageRGB(self):
        """finds average of RGB tuple and writes data into csv
        >>> i = ImageAnalysis("mountain.png")
        >>> i.retrieveHidden()
        """
        
        avg_value = []
        for row in self.fixed:
            avg_row=[]
            for col in row:
                avg_row.append(np.mean(col).astype(np.uint8))
            avg_value.append(avg_row)
            
        with open('RGB.csv', 'w') as fobj:
            for row in avg_value:
                for col in row:
                    fobj.write(str(col)+",")
                fobj.write("\n")
                
        self.avg = np.array(avg_value)
        return self.find_hash(self.avg)
    
    def load_rgb_from_file(self, filename):
        
        with open(filename, 'r') as fobj:
            info = fobj.readlines()
        values = []
        for row in info:
            for col in info:
                values.append(int(col))
        array = np.array(values, dtype = np.uint8)
        array = array.reshape(
        
        io.imsave("grayscale.jpg", array)
        return self.find_hash(array)
        
    
i = ImageAnalysis("mountain.png")
i.retrieveHidden()
i.fix()
i.averageRGB()
i.load_rgb_from_file("RGB.csv")

        
    
 
 
 
 
 
 
original = ImageAnalysis("mountain.png")
fixed = ImageAnalysis("mountain_fixed.jpg")
print(original == fixed) # should return false


doctest.testmod()
            


        
        
