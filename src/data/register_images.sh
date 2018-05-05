#!/usr/bin/env bash

images_dir=/Users/mm40108/projects/datadays17/olfactory_protein_viz/images/Robo2_TEST

elastix=/Users/mm40108/Desktop/progfiles/elastix_macosx64_v4.8/bin/elastix
params=./Parameters_BSpline.txt

fixed=$images_dir/Robo2_1a.jpg

$elastix -f $fixed -m $images_dir/Robo2_2a.jpg -out $images_dir/out -p $params
$elastix -f ... -m ... -out $images_dir/out -p $params -t0 out1/TransformParameters.0.txt
$elastix -f ... -m ... -out out3 -p param3.txt -t0 out2/TransformParameters.0.txt



$elastix -f $fixed -m $images_dir/Robo2_2a.jpg -m $images_dir/Robo2_3.jpg -out $images_dir/out -p $params -p $params