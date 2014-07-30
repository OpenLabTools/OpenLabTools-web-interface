class Microscope():
    def __init__(self):
        pass

class toggle():
    def __init__(self, state):
        self._state = state;
        pass

    def on(self):
        pass

    def off(self):
        pass
        
    def toggle(self):
        pass

    def state(self): return self.state()
    
    
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import numpy as np
    import time
    im_file_name = "/home/lz307/Downloads/off-and-on-bulb-158099_238x238.jpg"
    plt.ion()
    plt.show()
    img=mpimg.imread(im_file_name)
    left_half = img[:, 1:img.shape[1]/2, :];
    right_half = img[:, img.shape[1]/2-4:img.shape[1]-5, :];
    right_half = np.fliplr(right_half)
    
    while(1):
        imgplot = plt.imshow(left_half)
        plt.draw()
        time.sleep(1)
        imgplot = plt.imshow(right_half)
        plt.draw()
        time.sleep(1)
