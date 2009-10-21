#!/bin/sh
sed \
	-e 's/source="norm"/source="DUSG_norm"/g' \
	-e 's/source="split"/source="DUSG_split"/g' \
	-e 's/source="mlp"/source="DUSG_mlp"/g' \
	-e 's/source="mlp1"/source="DUSG_mlp1"/g' \
	-e 's/source="post"/source="DUSG_post"/g' \
	-i train_*_B_DUSG_{preLkh1,preLkh2,post,comb}.xml
sed \
	-e 's/source="norm"/source="C_norm"/g' \
	-e 's/source="split"/source="C_split"/g' \
	-e 's/source="mlp"/source="C_mlp"/g' \
	-e 's/source="mlp1"/source="C_mlp1"/g' \
	-e 's/source="post"/source="C_post"/g' \
	-i train_*_B_C_{preLkh1,preLkh2,post,comb}.xml
