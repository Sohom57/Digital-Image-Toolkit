import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processing import operations

class TestImageProcessing(unittest.TestCase):
    """Test suite for image processing operations."""

    def setUp(self):
        """Set up common test data before each test method."""
        # A simple 3x3 grayscale image (2D array)
        self.gray_image = np.array([
            [50, 100, 150],
            [120, 128, 140],
            [200, 210, 220]
        ], dtype=np.uint8)

        # A simple 2x2 color image (3D array)
        self.color_image = np.array([
            [[255, 0, 0], [0, 255, 0]],  # Red, Green
            [[0, 0, 255], [10, 20, 30]]   # Blue, Dark Gray
        ], dtype=np.uint8)

    def test_convert_to_grayscale(self):
        """Test the grayscale conversion logic."""
        result = operations.convert_to_grayscale(self.color_image)
        self.assertEqual(result.ndim, 2)
        self.assertEqual(result.shape, (2, 2))
        self.assertEqual(result.dtype, np.uint8)
        self.assertAlmostEqual(result[0, 0], 76, delta=1)

    def test_negative_image(self):
        """Test the image negation."""
        result = operations.negative_image(self.gray_image)
        expected = 255 - self.gray_image
        np.testing.assert_array_equal(result, expected)
        self.assertEqual(result[0, 0], 205)

    def test_apply_thresholding(self):
        """Test binary thresholding."""
        threshold = 128
        result = operations.apply_thresholding(self.gray_image, threshold)
        expected = np.array([
            [0, 0, 255],
            [0, 0, 255],
            [255, 255, 255]
        ], dtype=np.uint8)
        np.testing.assert_array_equal(result, expected)

    # --- START OF CHANGES ---
    def test_laplacian_edge(self):
        """Test the Laplacian edge detection."""
        # Use a 5x5 image with a 1-pixel zero-border to get a clean result.
        edge_image = np.array([
            [0,   0,   0,   0, 0],
            [0,   0,   0,   0, 0],
            [0, 255, 255, 255, 0],
            [0,   0,   0,   0, 0],
            [0,   0,   0,   0, 0]
        ], dtype=np.uint8)

        result = operations.laplacian_edge(edge_image)
        
        self.assertEqual(result.shape, edge_image.shape)
        self.assertEqual(result.dtype, np.uint8)
        
        # Now, the corner pixel's neighborhood is all zeros, so the result MUST be 0.
        self.assertEqual(result[0, 0], 0)
        
        # The center of the edge should be bright (a high value), indicating an edge was found.
        # We check the pixel at [2, 2] which is the center of our 5x5 image.
        self.assertGreater(result[2, 2], 200) # Check for a strong edge detection response
    # --- END OF CHANGES ---

    def test_adjust_contrast(self):
        """Test contrast adjustment."""
        alpha_increase = 1.5
        result_inc = operations.adjust_contrast(self.gray_image, alpha_increase)
        self.assertEqual(result_inc[0, 0], 11)
        self.assertEqual(result_inc[2, 0], 236)

        alpha_decrease = 0.5
        result_dec = operations.adjust_contrast(self.gray_image, alpha_decrease)
        self.assertEqual(result_dec[0, 0], 89)

if __name__ == '__main__':
    unittest.main()