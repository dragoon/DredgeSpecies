## Dredge Fish Species Notebook
<p align="middle">
<img width="500" height="227" src="readme_images/dredge_promo.png"/>
<img width="155" height="227" src="readme_images/notebook.png"/>
</p>

### Description
The process to create a physical version of the digital Fish Species Notebook from [Dredge](https://www.dredge.game/)

### Image Extraction
![Fish Notebook](readme_images/fish_notebook_screenshot.png)
The Notebook is a single PDF file, so we will use PDF image extractor to get specific fish images out of it:
```shell
./extract_images.sh fish.pdf dredge
```
The script uses ``pdfimages`` tools and ``ImageMagick`` to apply transparent mask back to images.
As a result, you will get one folder full of different images.
You will notice that fish images
Next, create the following directory structure:
```
📂 assets
├── 📂 aberration_bg
│   ├── horizontal_rect_abb.png
│   ├── square_abb.png
│   └── vertical_rect_abb.png
├── 📂 photos_aberrations
│   ├── image-xxx.png
│   └── ...
├── 📂 normal_bg
│   ├── horizontal_rect_normal.png
│   ├── square_normal.png
│   └── vertical_rect_normal.png
├── 📂 photos_normal
│   ├── image-xxx.png
│   └── ...
```
I have already added background directories to this repo:

<p align="middle">
<img width="320" height="320" src="assets/aberration_bg/square_abb.png"/>
<img width="320" height="320" src="assets/normal_bg/square_normal.png"/>
</p>

The fish photos are not in this repo for potential copyright reasons.
Just added a "basic and plentiful" cod as an example:
<p align="middle">
<img width="320" height="320" src="assets/normal/image-178.png"/>
<img width="320" height="320" src="assets/aberrations/image-176.png"/>
</p>
So you need to manually move extracted fish images to their respective folders.

### Background Matching
Next, I prepared a python script that will accept background and raw image photo directories, and match the fish with background using the closest aspect ratio: 

```shell
python3 dredge_bg_matcher.py assets/normal_bg assets/normal normal_fish_with_bg
python3 dredge_bg_matcher.py assets/aberration_bg assets/aberrations abb_fish_with_bg
```
The script is not perfect, and I have added a custom background matching for some images based on their extracted order sequence,
so you might have to tweak it a bit if you get different results.

#### Fish Shadow
One thing I noticed is that the extracted images do not have shadow as in the PDF, so I added a method to generate a shadow to this script as well.
I think it matches the original one pretty well:
<p align="middle">
<img width="300" height="168" alt="original shadow" src="readme_images/orig_shadow.png"/>
<img width="284" height="168" alt="my shadow" src="readme_images/my_shadow.png"/>
</p>
<p align="middle">Left - original, Right - My shadow</p>


#### Final Results
After that, you should see the matched and combines photos in the output directories:
<p align="middle">
<img width="320" height="320" src="assets/normal_fish_with_bg/image-178.png"/>
<img width="320" height="320" src="assets/abb_fish_with_bg/image-176.png"/>
</p>

### Photo Printing
I have used my local photo printing shops (in Switzerland: Migros or ALDI Photos) with the following specs:
* Square photos: 9cm for most, 10 cm for Grouper and Gnashing Perch
* Rectangle: 9x13cm
* Rare fish Close-ups: 10x15cm

First Results:

![Fish Sheet First Results](readme_images/fish_sheet_draft.jpg)

Total budget: XX$

### Notebook
This is the most difficult part. I had imagined the following specifications:
* Hardcover
* Brown/Yellow/Orange cover
* 40 pages
* Liner or Blank
* Yellowish paper

This turned out to be extremely difficult. For trying things out, I have ordered [this one from Amazon](https://www.amazon.de/-/en/gp/product/B09FF7J2B3/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1) (in package of 3):
<p align="middle">
    <img src="readme_images/amazon_40sheet1.jpg" width="300">
    <img src="readme_images/amazon_40sheet.jpg" width="300">
</p>

The cover is black and soft, but other parameters match well.

Otherwise I am considering a [Personalised A4 Notebook from Etsy](https://www.etsy.com/listing/1158061119/personalised-a4-notebook-printed-with?ref=cart):
<p align="middle">
    <img src="readme_images/etsy1.avif" width="300">
    <img src="readme_images/etsy2.avif" width="300">
</p>