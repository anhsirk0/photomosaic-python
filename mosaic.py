from PIL import Image
import math
import glob

class Mosaic:
    """
    Creates Photomosaic from images as tiles
    @param tile_width as int
    @param tile_height as int
    """
    def __init__(self, tile_width=50, tile_height=50):
        self.dir = './assets/tiles'
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_size = (self.tile_width, self.tile_height)
        self.tiles = []
        self.tiles_rgb = []

    def get_avg_rgb(self, im):
        """
        Return average rgb value of an image by looping
        over image's pixel and averaging overall rgb values
        @param im as PIL.Image
        """
        rgb_img = im.convert('RGB')
        width, height = im.size
        n = width * height
        avg_r = 0
        avg_g = 0
        avg_b = 0
        for i in range(width):
            for j in range(height):
                r, g, b = rgb_img.getpixel((i, j))
                avg_r += r/n
                avg_g += g/n
                avg_b += b/n
        return([avg_r, avg_g, avg_b])

    def distance(self, rgb1, rgb2):
        """
        Calculate distance between two rgb points
        as 3D coordinates
        @param rgb1, rgb2 as list of three elements
        """
        r1 = rgb1[0]
        r2 = rgb2[0]

        g1 = rgb1[1]
        g2 = rgb2[1]

        b1 = rgb1[2]
        b2 = rgb2[2]

        d = (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2
        return math.sqrt(d)

    def get_closest(self, rgb):
        """
        Returns the index of closest matching image from self.tiles
        @param rgb as list of three elements
        """
        m = math.inf
        for i in range(len(self.tiles_rgb)):
            d = self.distance(rgb, self.tiles_rgb[i])
            if m >= d:
                m = d
                index = i
        return index


    def create_tiles(self, dir):
        """
        Create tiles from given directory and store them in assets/tiles/
        @param dir as str
        """
        all_images = glob.glob(f"{dir}/*.*g")
        no_of_images = len(all_images)

        try:
            os.mkdir(self.dir)
        except:
            pass

        for i in range(no_of_images):
            img = all_images[i]
            im = Image.open(img)
            im = im.resize(self.tile_size)
            ext = img.split(".")[-1]
            im.save(f"{self.dir}/tile_{i}.{ext}")
            im_rgb = self.get_avg_rgb(im)
            self.tiles_rgb.append(im_rgb)

        print(no_of_images, "tiles created")

    def create_mosaic(self, im, out):
        """
        Create a mosaic of given image using tiles from assets/tiles
        @param im as PIL.Image
        """
        n = 5
        im.thumbnail((500, 500))
        width, height = im.size

        new_width = int(width * self.tile_width / n)
        new_height = int(height * self.tile_height / n)
        final = Image.new('RGB', (new_width, new_height))

        for w in range(0, width, n):
            for h in range(0, height, n):
                piece = im.crop((w, h, w + n, h + n))
                piece_rgb = self.get_avg_rgb(piece)
                index = self.get_closest(piece_rgb)
                tile_location = glob.glob(f"assets/tiles/tile_{index}.*")[0]
                tile = Image.open(tile_location)
                x = int(w * self.tile_width / n)
                y = int(h * self.tile_height / n)
                final.paste(tile, (x, y))

        final.save(out)
        print("Mosaic saved as output.png")

    def create(self, img_name, out, dir):
        """
        Main function, creates tiles and mosaic
        @param img_name as str
        @param dir as str
        """

        im = Image.open(img_name)
        self.create_tiles(dir)
        self.create_mosaic(im, out)

