# Data and Code for IJCAI'21 paper - SafeDrug

### Folder Specification
- data/
    - **get_SMILES.py**: which is a crawler, given the drug ATC-4 level code (four digit, e.g., 'A01A'), our crawler returns (a set of) SMILES strings of that ATC-4 class (crawled from drugbank). This file needs atc2rxnorm.pkl (which maps ATC-4 code to rxnorm code and then query to drugbank), generated from ndc2rxnorm_mapping.txt and ndc2atc_level4.csv.
    - **ddi_mask_H.py**: This file will output the bipartite structure of drug molecules and the fragments/substructures.
    - **processing.py**: our data preprocessing file.
      - Input (extracted from external resources)
          - PRESCRIPTIONS.csv: the prescription file from MIMIC-III raw dataset
          - DIAGNOSES_ICD.csv: the diagnosis file from MIMIC-III raw dataset
          - PROCEDURES_ICD.csv: the procedure file from MIMIC-III raw dataset
          - idx2SMILES.pkl: drug ID (we use ATC-4 level code to represent drug ID) to drug SMILES string dict (This file is created by **get_SMILES.py**, due to the change of drug bank web structure, it may need updates)
          - ndc2atc_level4.csv: this is a NDC-RXCUI-ATC5 file, which gives the mapping information
          - drug-atc.csv: this is a CID-ATC file, which gives the mapping from CID code to detailed ATC code (we should truncate later)
          - ndc2rxnorm_mapping.txt: rxnorm to RXCUI file
          - drug-DDI.csv: this a large file, could be downloaded from https://drive.google.com/file/d/1mnPc0O0ztz0fkv3HF-dpmBb8PLWsEoDz/view?usp=sharing
      - Output
          - data_final.pkl: intermediate result
          - ddi_A_final.pkl: ddi matrix
          - ddi_matrix_H.pkl: H mask structure (This file is created by **ddi_mask_H.py**)
          - ehr_adj_final.pkl: used in GAMENet baseline (if two drugs appear in one set, then they are connected)
          - (important) records_final.pkl: 100 patient visit-level record samples. Under MIMIC Dataset policy, we are not allowed to distribute the datasets. Practioners could go to https://physionet.org/content/mimiciii/1.4/ and requrest the access to MIMIC-III dataset and then run our processing script to get the complete preprocessed dataset file.
          - voc_final.pkl: diag/prod/med index to code dictionary
    - follow this figure and figure out the data preprocessing flow

    <table> <tr> <td> <a><img src="illustration.png"></a> </td></tr> </table>
- src/
    - SafeDrug.py: our model
    - Epoch_49_TARGET_0.06_JA_0.5183_DDI_0.05854.model: the model we trained on the training set
    - baselines:
        - GAMENet.py
        - DMNC.py: there are some bg issues for the latest dnc package, please refer to the original DMNC repo https://github.com/thaihungle/DMNC
        - Leap.py
        - Retain.py
        - ECC.py
        - LR.py
    - setting file
        - model.py
        - util.py
        - layer.py



### Step 1: Data Processing

- Go to https://physionet.org/content/mimiciii/1.4/ to download the MIMIC-III dataset (You may need to get the certificate)

  ```python
  cd ./data
  wget -r -N -c -np --user [account] --ask-password https://physionet.org/files/mimiciii/1.4/
  ```

- go into the folder and unzip three main files

  ```python
  cd ./physionet.org/files/mimiciii/1.4
  gzip -d PROCEDURES_ICD.csv.gz # procedure information
  gzip -d PRESCRIPTIONS.csv.gz  # prescription information
  gzip -d DIAGNOSES_ICD.csv.gz  # diagnosis information
  ```

- download the DDI file and move it to the data folder
  download https://drive.google.com/file/d/1mnPc0O0ztz0fkv3HF-dpmBb8PLWsEoDz/view?usp=sharing
  ```python
  mv drug-DDI.csv ./data
  ```

- processing the data to get a complete records_final.pkl

  ```python
  cd ./data
  vim processing.py
  
  # line 294~296
  # med_file = './physionet.org/files/mimiciii/1.4/PRESCRIPTIONS.csv'
  # diag_file = './physionet.org/files/mimiciii/1.4/DIAGNOSES_ICD.csv'
  # procedure_file = './physionet.org/files/mimiciii/1.4/PROCEDURES_ICD.csv'
  
  python processing.py
  ```

- run ddi_mask_H.py to get the ddi_mask_H.pkl

  ```python
  python ddi_mask_H.py
  ```



### Step 2: Package Dependency

- first, install the rdkit conda environment
```python
conda create -c conda-forge -n SafeDrug  rdkit
conda activate SafeDrug
```

- then, in SafeDrug environment, install the following package
```python
pip install scikit-learn, dill, dnc
```
Note that torch setup may vary according to GPU hardware. Generally, run the following
```python
pip install torch
```
If you are using RTX 3090, then plase use the following, which is the right way to make torch work.
```python
python3 -m pip install --user torch==1.8.0+cu111 torchvision==0.9.0+cu111 torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html
```

- Finally, install other packages if necessary
```python
pip install [xxx] # any required package if necessary, maybe do not specify the version, the packages should be compatible with rdkit
```

Here is a list of reference versions for all package

```shell
pandas: 1.3.0
dill: 0.3.4
torch: 1.8.0+cu111
rdkit: 2021.03.4
scikit-learn: 0.24.2
numpy: 1.21.1
```

Let us know any of the package dependency issue. Please pay special attention to pandas, some report that a high version of pandas would raise error for dill loading.



### Step 3: run the code

```python
python SafeDrug.py
```

here is the argument:

    usage: SafeDrug.py [-h] [--Test] [--model_name MODEL_NAME]
                   [--resume_path RESUME_PATH] [--lr LR]
                   [--target_ddi TARGET_DDI] [--kp KP] [--dim DIM]
    
    optional arguments:
      -h, --help            show this help message and exit
      --Test                test mode
      --model_name MODEL_NAME
                            model name
      --resume_path RESUME_PATH
                            resume path
      --lr LR               learning rate
      --target_ddi TARGET_DDI
                            target ddi
      --kp KP               coefficient of P signal
      --dim DIM             dimension

If you cannot run the code on GPU for SafeDrug.py, just change line 101, "cuda" to "cpu" and change line 126 to
```python
model.load_state_dict(torch.load(open(args.resume_path, 'rb'), map_location=torch.device('cpu')))
``` 

### Citation
```bibtex
@inproceedings{yang2021safedrug,
    title = {SafeDrug: Dual Molecular Graph Encoders for Safe Drug Recommendations},
    author = {Yang, Chaoqi and Xiao, Cao and Ma, Fenglong and Glass, Lucas and Sun, Jimeng},
    booktitle = {Proceedings of the Thirtieth International Joint Conference on
               Artificial Intelligence, {IJCAI} 2021},
    year = {2021}
}
```

Welcome to contact me <chaoqiy2@illinois.edu> for any question. Partial credit to a previous repo (this paper is also from our group) https://github.com/sjy1203/GAMENet
