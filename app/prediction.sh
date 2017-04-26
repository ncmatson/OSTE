for i in $PWD/app/static/img/*.png; do convert -flatten "$i" "${i%.*}.tiff" ; done

python $PWD/app/predict.py \
--model $PWD/app/MnihCNN_multi.py \
--param $PWD/app/epoch-400.model \
--test_sat_dir $PWD/app/static/img \
--channels 3 \
--offset 8 \
--gpu 0 


