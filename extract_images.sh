#!/bin/bash


# based on https://gist.github.com/bendavis78/ed22a974c2b4534305eabb2522956359
usage() {
    echo "Usage: $(basename $0) fish_species.pdf dest_dir";
}

[[ -z "$1" ]] && usage && exit 1;
[[ -z "$2" ]] && usage && exit 1;

TMPDIR="$(mktemp -d)";
DIR=$2;

mkdir "$TMPDIR/extracted";
# Extract the images into tmpdir
pdfimages -all "$1" "$TMPDIR/extracted/image" || exit 1;

# Rename images based on object id and whether or not they are a mask
pdfimages -list "$1" | tail -n +3 | while read -r row; do
    num=$(echo "$row" | awk '{print $2}');
    imgtype=$(echo "$row" | awk '{print $3}');
    imgenc=$(echo "$row" | awk '{print $9}');
    objectid=$(echo "$row" | awk '{print $11}');
    
    # Determine source extension based on the encoding from the PDF
    if [[ "$imgenc" == "jpeg" ]]; then
        src_ext="jpg"
    else
        src_ext="png"
    fi

    # The source filename
    src=$(printf "$TMPDIR/extracted/image-%03d.$src_ext" $num);

    # Always use PNG for the output
    ext="png";

    if [[ "$imgtype" == "smask" ]]; then
        dest=$(printf "$TMPDIR/image-%03d-mask.$ext" $objectid);
    else
        dest=$(printf "$TMPDIR/image-%03d.$ext" $objectid);
    fi
    echo "$src -> $dest";
    mv "$src" "$dest" || exit 1;
done

# Merge the images that have a mask
pdfimages -list "$1" | tail -n +3 | while read -r row; do
    imgtype=$(echo "$row" | awk '{print $3}');
    objectid=$(echo "$row" | awk '{print $11}');
    if [[ "$imgtype" == "smask" ]]; then
        img=$(printf "$TMPDIR/image-%03d.png" $objectid);
        mask=$(printf "$TMPDIR/image-%03d-mask.png" $objectid);
        echo "convert $img $mask";
        # Ensure the output is always PNG with transparency
        convert "$img" "$mask" -alpha off -compose copy-opacity -composite "$img" || exit 1;
    fi
done

rm "$TMPDIR"/image-*-mask.png*;

mv "$TMPDIR"/* "$DIR/";

