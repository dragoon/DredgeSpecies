import sys
from PIL import Image
import os


def best_matching_background(bg_images, fg):
    """Find the best-matching background image based on aspect ratio."""
    fg_ratio = fg.width / fg.height
    best_bg = None
    min_diff = float('inf')

    for bg in bg_images:
        bg_ratio = bg.width / bg.height
        diff = abs(fg_ratio - bg_ratio)

        if diff < min_diff:
            min_diff = diff
            best_bg = bg

    return best_bg


def overlay_centered(bg, fg):
    # Calculate the ratio to fit the foreground width to (bg.width - 40)
    target_width = bg.width - 80
    # Only scale down if the foreground image's width is larger than target_width.
    if fg.width > target_width:
        width_ratio = target_width / fg.width
        new_size = (int(fg.width * width_ratio), int(fg.height * width_ratio))

        # Ensure the new height doesn't exceed the background height.
        # If it does, adjust the ratio accordingly and recalculate.
        if new_size[1] > bg.height:
            height_ratio = bg.height / fg.height
            new_size = (int(fg.width * height_ratio), int(fg.height * height_ratio))

        fg = fg.resize(new_size, Image.LANCZOS)

    x = (bg.width - fg.width) // 2
    y = (bg.height - fg.height) // 2

    merged = bg.copy()
    merged.paste(fg, (x, y), fg)
    return merged


def main(backgrounds_folder, foregrounds_folder, output_folder):
    # Load all background images
    bg_images = [Image.open(os.path.join(backgrounds_folder, bg)) for bg in os.listdir(backgrounds_folder) if
                 bg.endswith(('jpg', 'png', 'jpeg'))]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for fg_name in os.listdir(foregrounds_folder):
        fg_path = os.path.join(foregrounds_folder, fg_name)

        try:
            fg_image = Image.open(fg_path)
        except:
            continue  # Not an image, skip

        best_bg = best_matching_background(bg_images, fg_image)
        result = overlay_centered(best_bg.copy(), fg_image)
        result.save(os.path.join(output_folder, fg_name))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script_name.py <backgrounds_folder> <fish_images_folder> <output_folder>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
