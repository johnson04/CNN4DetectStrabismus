"""unit testing preprocess module"""
import os
import sys
import unittest

pkg_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../'
)
sys.path.insert(0, pkg_dir)

# pylint: disable=import-error,wrong-import-position
from detector import (
    DEFAULT_HEIGHT,
    DEFAULT_WIDTH
)

from detector.preprocess import (
    Vertex,
    Region,
    Image
)


class TestSuitePreprocessing(unittest.TestCase):
    """
    Purpose: testing preprocessing code
    Data Structures to be tested:
        * Vertex
        * Region
        * Image
    Features to be tested:
        * Load Image
        * Crop Image
    """

    def setUp(self):
        self.src_image = [
            {'file_name': 'test-data/healthy_014.jpg',
             'shape':(640, 428, 3)},
            {'file_name': 'test-data/eso_008.jpg',
             'shape': (467, 600, 3)}
        ]

    def test_vertex(self):
        '''testing Vertex data structure'''
        vtx = Vertex()
        self.assertEqual(vtx.x, 0)
        self.assertEqual(vtx.y, 0)
        vtx = Vertex(-1000, 235)
        self.assertEqual(vtx.x, -1000)
        self.assertEqual(vtx.y, 235)
        self.assertEqual(str(vtx), '(-1000, 235)')
        try:
            vtx.x =  200
            vtx.y = -134
        except Exception as err: # pylint: disable=broad-except
            self.failureException(err)
        self.assertEqual(vtx.x,  200)
        self.assertEqual(vtx.y, -134)
        self.assertEqual(str(vtx), '(200, -134)')

    def test_region_def(self):
        '''testing Region data structure'''
        rgn = Region()
        self.assertEqual(str(rgn), '(0, 0, 0, 0)')
        self.assertEqual(rgn.height, 0)
        self.assertEqual(rgn.width, 0)
        self.assertTrue(rgn.is_empty())
        # left < 0
        try:
            rgn.set_region(Vertex(-1, 2), Vertex(3, 4))
        except ValueError as err:
            print(str(err))
        else:
            self.fail('ValueError is expected!')
        # top < 0
        try:
            rgn.set_region(Vertex(1, -2), Vertex(3, 4))
        except ValueError as err:
            print(str(err))
        else:
            self.fail('ValueError is expected!')
        # right < 0
        try:
            rgn.set_region(Vertex(1, 2), Vertex(-3, 4))
        except ValueError as err:
            print(str(err))
        else:
            self.fail('ValueError is expected!')
        # bottom < 0
        try:
            rgn.set_region(Vertex(1, 2), Vertex(3, -4))
        except ValueError as err:
            print(str(err))
        else:
            self.fail('ValueError is expected!')
        # top > bottom : top is below bottom
        try:
            rgn.set_region(Vertex(1, 4), Vertex(3, 2))
        except ValueError as err:
            print(str(err))
        else:
            self.fail('ValueError is expected!')
        # left > right
        try:
            rgn.set_region(Vertex(3, 4), Vertex(1, 2))
        except ValueError as err:
            print(str(err))
        else:
            self.fail('ValueError is expected!')

    def test_region_op(self):
        '''testing Region operations'''
        try:
            rgn1 = Region(Vertex(1, 10), Vertex(18, 20))
            rgn2 = Region(Vertex(2, 16), Vertex(15, 18))
            rgn3 = Region(Vertex(3, 12), Vertex(19, 17))
        except ValueError:
            self.fail('Region initialization error!')
        self.assertEqual(rgn1.height, 10)
        self.assertEqual(rgn3.width, 16)
        self.assertTrue(rgn1.contains(rgn2))
        self.assertFalse(rgn1.contains(rgn3))
        self.assertFalse(rgn2.contains(rgn3))

        rgn2.union(rgn3)
        self.assertTrue(rgn2.contains(rgn3))
        self.assertEqual(str(rgn2), '(2, 12, 19, 18)')
        rgn1.intersect(rgn3)
        self.assertTrue(rgn3.contains(rgn1))

        try:
            rgn3.shift_vert(-3)
        except ValueError:
            self.fail('shift_vert() error!')
        self.assertEqual(str(rgn3), '(3, 9, 19, 14)')
        self.assertFalse(rgn2.contains(rgn3))
        try:
            rgn3.shift_vert(-10)
        except ValueError:
            print('ValueError is expected')
        else:
            self.fail('ValueError is expected!')

        try:
            rgn3.shift_vert(4)
        except ValueError:
            self.fail('shift_vert() error!')
        self.assertEqual(str(rgn3), '(3, 13, 19, 18)')
        self.assertTrue(rgn2.contains(rgn3))
        try:
            rgn3.shift_hori(1)
        except ValueError:
            self.fail('shift_hori() error!')
        self.assertEqual(str(rgn3), '(4, 13, 20, 18)')
        self.assertFalse(rgn2.contains(rgn3))

        try:
            rgn3.shift_hori(-5)
        except ValueError:
            print('ValueError is expected')
        else:
            self.fail('ValueError is expected!')
        self.assertEqual(str(rgn3), '(4, 13, 20, 18)')

    def test_image_def(self):
        '''testing Image data structure'''
        # testing empty Image
        try:
            img = Image()
        except Exception: # pylint: disable=broad-except
            self.fail('an error occurred when creating empty Image!')
        self.assertTrue(img.type is None, True)
        self.assertEqual(img.height, 0)
        self.assertEqual(img.width, 0)

        # exporting empty image causes TypeError
        try:
            img.to_rgb()
        except TypeError:
            print('TypeError is expected!')
        else:
            self.fail('TypeError is expected!')
        try:
            img.to_bgr()
        except TypeError:
            print('TypeError is expected!')
        else:
            self.fail('TypeError is expected!')
        try:
            img.to_gray()
        except TypeError:
            print('TypeError is expected!')
        else:
            self.fail('TypeError is expected!')

        # testing Image loaded from a file
        file_name = self.src_image[0]['file_name']
        img_shape = self.src_image[0]['shape']
        try:
            img = Image(file_name)
        except Exception: # pylint: disable=broad-except
            self.fail(f'loading image from {file_name} failed!')
        self.assertEqual(img_shape[:2], (img.height, img.width))

        # exporting loaded image should work
        try:
            new_img = img.to_rgb()
        except TypeError:
            self.fail('TypeError: img.to_rgb()!')
        self.assertEqual(new_img.shape[:2], (img.height, img.width))

        try:
            new_img = img.to_bgr()
        except TypeError:
            self.fail('TypeError: img.to_bgr()!')
        self.assertEqual(new_img.shape[:2], (img.height, img.width))

        try:
            img.to_gray()
        except TypeError:
            self.fail('TypeError: img.to_gray()!')
        self.assertEqual(new_img.shape[:2], (img.height, img.width))

    def test_image_op(self):
        '''testing Image operations'''
        file_name = self.src_image[0]['file_name']
        img_shape = self.src_image[0]['shape']
        try:
            img = Image(file_name)
        except Exception: # pylint: disable=broad-except
            self.fail(f'loading image from {file_name} failed!')
        self.assertEqual(img.height, img_shape[0])
        self.assertEqual(img.width,  img_shape[1])
        try:
            img.resize(width=0, height=100)
        except ValueError:
            print('ValueError is expected!')
        else:
            self.fail('ValueError is expected!')
        try:
            img.resize(width=400, height=0)
        except ValueError:
            print('ValueError is expected!')
        else:
            self.fail('ValueError is expected!')

        try:
            new_type, new_img = img.resize()
        except ValueError:
            self.fail('ValueError occured when resizing image with default arguments!')
        self.assertEqual(new_type, 'BGR')
        self.assertEqual(new_img.shape[0], DEFAULT_HEIGHT)
        self.assertEqual(new_img.shape[1], DEFAULT_WIDTH)

if __name__ == '__main__':
    unittest.main()