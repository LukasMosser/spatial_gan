import os
import numpy as np
from PIL import Image
from PIL.Image import FLIP_LEFT_RIGHT


def image_to_tensor(img):
    '''
    convert image to Theano/Lasagne 3-tensor format;
    changes channel dimension to be in the first position and rescales from [0,255] to [-1,1]
    '''
    print "lel"
    print img.shape
    tensor = np.array(img).transpose( (2,0,1) )
    tensor = tensor / 128. - 1.
    return tensor


def tensor_to_image(tensor):
    '''
    convert 3-tensor to image;
    changes channel to be last and rescales from [-1, 1] to [0, 255]
    '''
    img = np.array(tensor).transpose( (1,2,0) )
    img = (img + 1.) * 128.
    return np.uint8(img)
    

def get_texture_iter(folder, npx=128, batch_size=64, \
                     filter=None, mirror=True):
    '''
    @param folder       iterate of pictures from this folder
    @param npx          size of patches to extract
    @param n_batches    number of batches to yield - if None, it yields forever
    @param mirror       if True the images get augmented by left-right mirroring
    @return a batch of image patches fo size npx x npx, with values in [0,1]
    '''
    HW    = npx
    imTex = []
    files = os.listdir(folder)
    for f in files:
        name = folder + f
        #try:
        print "lel"
        img = Image.open(name)
        img = np.array(img)
        gray = np.mean(img, -1)
        img = gray
        img = np.array(img)[ :, : , np.newaxis]
        
        print img.shape
        #print np.array(img).shape
        imTex += [image_to_tensor(img)]
        if mirror:
            img = img.transpose(FLIP_LEFT_RIGHT)
            imTex += [image_to_tensor(img)]
        #except:
        print "Image ", name, " failed to load!"
    print imTex
    while True:
        data=np.zeros((batch_size,1,npx,npx))                   # NOTE: assumes 3 channels!
        for i in range(batch_size):
            ir = np.random.randint(low=0, high=len(imTex))
            imgBig = imTex[ir]
            if HW < imgBig.shape[1] and HW < imgBig.shape[2]:   # sample patches
                h = np.random.randint(imgBig.shape[1] - HW)
                w = np.random.randint(imgBig.shape[2] - HW)
                img = imgBig[:, h:h + HW, w:w + HW]
            else:                                               # whole input texture
                img = imgBig
            data[i] = img

        yield data


def save_tensor(tensor, filename):
    '''
    save a 3-tensor (channel, x, y) to image file
    '''
    print tensor.shape
    img = tensor_to_image(tensor)
    print img.shape
    img = Image.fromarray(img[:, :, 0])
    img.save(filename)


if __name__=="__main__":
    print "nothing here."
