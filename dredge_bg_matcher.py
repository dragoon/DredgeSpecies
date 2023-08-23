import sys
from PIL import Image, ImageFilter, ImageColor
import os


def add_shadow(input_image, offset=(8, 8), shadow_color="#111111AA"):
    """Add a shadow to an image with a transparent background."""

    # Ensure the image has an alpha layer
    img_with_alpha = input_image.convert('RGBA')

    # Create a blank transparent image with the size of the input image + offset
    total_width = input_image.width + abs(offset[0] * 2)  # Extra space for the shadow
    total_height = input_image.height + abs(offset[1] * 2)
    new_image = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))  # Transparent

    # Position the original image on the new image
    img_position = (abs(offset[0]) if offset[0] > 0 else 0, abs(offset[1]) if offset[1] > 0 else 0)

    # Create a shadow mask using the alpha channel of the image
    alpha = img_with_alpha.split()[3]
    blurred_shadow = alpha.filter(ImageFilter.GaussianBlur(radius=0))
    # Convert shadow_color from string to tuple
    r, g, b = ImageColor.getcolor(shadow_color, "RGB")
    shadow_color_rgba = (r, g, b, 0)  # Append 0 alpha

    shadow_layer = Image.new('RGBA', new_image.size, shadow_color_rgba)  # Use the RGBA tuple
    shadow_position = (img_position[0] + offset[0], img_position[1] + offset[1])
    shadow_layer.paste(shadow_color, shadow_position, blurred_shadow)  # Paste using alpha of blurred shadow as mask

    # Paste original image on top of shadow
    shadow_layer.paste(img_with_alpha, img_position, img_with_alpha)

    return shadow_layer


def best_matching_background(bg_images, fg):
    """Find the best-matching background image based on aspect ratio."""
    fg_ratio = fg.width / fg.height
    best_bg = None
    min_diff = float('inf')

    img_num = os.path.basename(fg.filename).split('-')[1].split('.')[0]
    # overrides for wrong matches
    if img_num in ("439", "1110", "1112"):
        fg_ratio = 1

    for bg in bg_images:
        bg_ratio = bg.width / bg.height
        diff = abs(fg_ratio - bg_ratio)

        if diff < min_diff:
            min_diff = diff
            best_bg = bg

    return best_bg


def overlay_centered(bg, fg):
    # Calculate the ratio to fit the foreground width to (bg.width - 90)
    target_width = bg.width - 90

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

    fg_with_shadow = add_shadow(fg)  # Add shadow to the resized foreground

    x = (bg.width - fg_with_shadow.width) // 2
    y = (bg.height - fg_with_shadow.height) // 2

    merged = bg.copy()
    merged.paste(fg_with_shadow, (x, y), fg_with_shadow)
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
