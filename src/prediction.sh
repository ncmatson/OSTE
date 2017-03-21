python predict.py \
--model $PWD/MnihCNN_multi.py \
--param $PWD/epoch-400.model \
--test_sat_dir $PWD/inputs \
--channels 3 \
--offset 8 \
--gpu 0 &

