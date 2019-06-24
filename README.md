MIMIC-III Time Series Models
=========================

## Motivation

Exploring models that best suitable for time series tasks in clinical senarios.


## Data preparation

We do not provide the MIMIC-III data itself. You must acquire the data yourself from https://mimic.physionet.org/. Specifically, download the CSVs. Otherwise, generally we make liberal use of the following packages:

- numpy
- pandas

To extract time series data from MIMIC-III, you need to refer  https://github.com/YerevaNN/mimic3-benchmarks. **Please be sure also to cite the original [MIMIC-III Benchmarks paper](https://arxiv.org/abs/1703.07771) and the original [MIMIC-III paper](http://www.nature.com/articles/sdata201635).**


## Requirments

If you are using Python with a Terminal, you can set python environment by typing this under mimic3-time-series folder
```
export PYTHONPATH=. 
```
If you are running with Jupyter Notebook, you can set python environment by typing this under mimic3-time-series folder
```
PYTHONPATH=. jupyter notebook --ip 0.0.0.0 --port 8003
```

### In-hospital mortality prediction#

#####LSTM
Train
```
python in_hospital_mortality/main.py --network models/lstm.py --dim 16 --timestep 1.0 --depth 2 --dropout 0.3 --mode train --batch_size 8 --output_dir in_hospital_mortality/
 
```

Test
```
python in_hospital_mortality/main.py --network models/lstm.py --dim 16 --timestep 1.0 --depth 2 --dropout 0.3 --mode test --batch_size 8 --load_state in_hospital_mortality/keras_states/k_lstm.n16.d0.3.dep2.bs8.ts1.0.epoch27.test0.27868239298546116.state
```

##### XGBoost
Train & Test
```
python in_hospital_mortality/xgboost/main.py  --output_dir in_hospital_mortality/xgboost/
```

##### Logistic Regression
Train & Test
```
python in_hospital_mortality/lr/main.py --l2 --C 0.001 --output_dir in_hospital_mortality/lr/
```


### Decompensation prediction


```
python decompensation/main.py --network models/lstm.py --dim 16 --timestep 1.0 --depth 2 --dropout 0.3 --mode train --batch_size 8 --output_dir decompensation
```


### Length of stay prediction
```
python length_of_stay/main.py --network models/lstm.py --dim 16 --timestep 1.0 --depth 2 --dropout 0.3 --mode train --batch_size 8 --output_dir length_of_stay
```
### Phenotype classification
```
python phenotyping/main.py --network models/lstm.py --dim 256 --timestep 1.0 --depth 1 --dropout 0.3 --mode train --batch_size 8 --output_dir phenotyping/
```

### MultiTask
```
python multitask/main.py --network models/multitask_lstm.py --dim 512  --timestep 1.0  --dropout 0.3 --mode train --batch_size 16  --ihm_C 0.2 --decomp_C 1.0 --los_C 1.5 --pheno_C 1.0   --output_dir multitask/
```

### Questions

Please feel free to reach me (Yanke Hu, yhu@humana.com) or Raj (Raj Subramanian, rsubramanian5@humana.com) for any questions or just open a github issue.