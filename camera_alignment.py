"""
Helper module for checking camera alignment. Serves for a very specific setup. In the setup there must be two markers
which need to be aligned horizontally with the camera. Also the two markers should be at a specific distance to match
the x coordinates within the image. The specific coordinates are calculated using X and Y coordinate coefficients.
Function returns two different outputs. First is a tuple of length 3 containing bools. These assertions indicate
if horizontal alignemnt, left marker alignemnt and right marker alignment are correct or not. Second output is the image
data showing the given frame and alignment information. It is practical to use this image matrix wihin a video input.

Usage:
    import camera_alignment as ca

    # Read the frame and give frame to the get_alignment_info function.
    assertions, image_data = ca.get_alignment_info(frame)
    # Do logic using assertions information.
    # Display the image_data if desired.

"""

import logging
from pathlib import Path

import cv2
import numpy as np


MARKER_LEFT, MARKER_RIGHT = 'L', 'R'


MARKER_LEFT_PATH = str(Path(__file__).parent / "resources/marker_left.png")
MARKER_RIGHT_PATH = str(Path(__file__).parent / "resources/marker_right.png")

VERTICAL_ALIGNMENT_TOLERANCE = 5  # px
MARKER_INDIVIDUAL_TOLERANCE =  5  # px

Y_COORDINATE_COEFFICIENT = 210 / 1000
X_COORDINATE_COEFFICIENT = 370 / 1000


def _get_marker_coords(source_matrix: np.ndarray, marker: str=MARKER_LEFT) -> tuple:

    """
    Returns the desired marker (left or right) coordinates from the given image if it was found,
    otherwise returns an empty tuple.
    """

    # Read the template.
    template_image = MARKER_LEFT_PATH if marker == MARKER_LEFT else MARKER_RIGHT_PATH
    template_matrix = cv2.imread(template_image, cv2.IMREAD_GRAYSCALE)
    # TODO Do assertions here.
    w, h = template_matrix.shape

    # Apply template matching.
    # One of the following methods could also be used.
    # 'cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED'
    result = cv2.matchTemplate(source_matrix, template_matrix, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    return (top_left, bottom_right)

def _get_expected_coordinates(source_matrix: np.ndarray):

    screen_width, screen_height = source_matrix.shape[::-1]
    expected_y_coordinate = int(screen_height * Y_COORDINATE_COEFFICIENT)
    expected_left_x_coordinate = int(screen_width * X_COORDINATE_COEFFICIENT)
    expected_right_x_coordinate = screen_width - expected_left_x_coordinate

    return expected_y_coordinate, expected_left_x_coordinate, expected_right_x_coordinate

def _get_asssertions_info(left_marker_coordinates:tuple, right_marker_coordinates: tuple, expected_coords: tuple) -> list:

    """
    Checks if camera is correctly aligned.
    Returns a dictionary containing three alignment assertion results, horizontal line alignment, left marker vertical
    alignment, right marker vertical alignemt, respectively.
    """

    assertions_info = {"horizontal": True, "left_vertical": True, "right_vertical": True}
    expected_y_coordinate, expected_left_x_coordinate, expected_right_x_coordinate = expected_coords

    marker_left_center_y = int((left_marker_coordinates[0][1] + left_marker_coordinates[1][1]) / 2)
    marker_left_center_x = int((left_marker_coordinates[0][0] + left_marker_coordinates[1][0]) / 2)

    marker_right_center_y = int((right_marker_coordinates[0][1] + right_marker_coordinates[1][1]) / 2)
    marker_right_center_x = int((right_marker_coordinates[0][0] + right_marker_coordinates[1][0]) / 2)

    calculated_y_coordinate = int((marker_left_center_y + marker_right_center_y) / 2)
    if abs(calculated_y_coordinate - expected_y_coordinate) > VERTICAL_ALIGNMENT_TOLERANCE:
        print("Image is not aligned, expected y coordinate not satisfied...")
        print((
            f"Calculated y coordinate: {calculated_y_coordinate}\n"
            f"Expected y coordinate: {expected_y_coordinate}\n"
            f"Tolerance: {VERTICAL_ALIGNMENT_TOLERANCE}"))
        assertions_info["horizontal"] = False

    if abs(marker_left_center_x - expected_left_x_coordinate) > MARKER_INDIVIDUAL_TOLERANCE:
        print("Image is not aligned, marker left x coordinate not satisfied...")
        print((
            f"Calculated left marker x coordinate: {marker_left_center_x}\n"
            f"Expected left marker x coordinate: {expected_left_x_coordinate}\n"
            f"Tolerance:{MARKER_INDIVIDUAL_TOLERANCE}"
            ))
        assertions_info["left_vertical"] = False

    if abs(marker_right_center_x - expected_right_x_coordinate) > MARKER_INDIVIDUAL_TOLERANCE:
        print("Image is not aligned, marker right x coordinate not satisfied...")
        print((
            f"Calculated right marker x coordinate: {marker_right_center_x}\n"
            f"Expected right marker x coordinate: {expected_right_x_coordinate}\n"
            f"Tolerance:{MARKER_INDIVIDUAL_TOLERANCE}"
            ))
        assertions_info["right_vertical"] = False

    return assertions_info

def _draw_custom_grid(source_matrix:np.ndarray, expected_coords:tuple, assertions_info: dict, thickness:int=2):

    def get_color(assertion):
        return [0, 255, 0] if assertion else [0, 0, 255]

    # Draw
    color_h = get_color(assertions_info["horizontal"])
    color_vl = get_color(assertions_info["left_vertical"])
    color_vr = get_color(assertions_info["right_vertical"])

    start = 0
    m_shape = source_matrix.shape
    screen_height, screen_width = m_shape[:-1] if len(m_shape) > 2 else m_shape
    horizontal_grid_line, vertical_grid_line_left, vertical_grid_line_right = expected_coords

    cv2.line(source_matrix, (start, horizontal_grid_line), (screen_width, horizontal_grid_line), color_h, thickness)
    cv2.line(source_matrix , (vertical_grid_line_left, start), (vertical_grid_line_left, screen_height), color_vl, thickness )
    cv2.line(source_matrix , (vertical_grid_line_right, start), (vertical_grid_line_right, screen_height), color_vr, thickness)

def _draw_marker_rectangles(source_matrix: np.ndarray, marker_coordinates:tuple, thickness:int=2):

    top_left_l, bot_right_l, top_left_r, bot_right_r = marker_coordinates

    cv2.rectangle(source_matrix, top_left_l, bot_right_l, [0, 255, 0], thickness)
    cv2.rectangle(source_matrix, top_left_r, bot_right_r, [255, 0, 0], thickness)

def get_alignment_info(source_matrix: np.ndarray):

    showcase_matrix = source_matrix.copy()
    # Read the source image.
    if len(source_matrix.shape) > 2:
        source_matrix = source_matrix[:, :, 0]

    # TODO Do assertions here.
    left_marker_coordinates = _get_marker_coords(source_matrix, MARKER_LEFT)
    right_marker_coordinates = _get_marker_coords(source_matrix, MARKER_RIGHT)

    expected_coords = _get_expected_coordinates(source_matrix)
    assertions_info = _get_asssertions_info(left_marker_coordinates, right_marker_coordinates, expected_coords)

    _draw_marker_rectangles(showcase_matrix, [*left_marker_coordinates, *right_marker_coordinates])
    _draw_custom_grid(showcase_matrix, expected_coords, assertions_info)

    return assertions_info, showcase_matrix

