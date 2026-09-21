# SGMR-NER
![selection](./Figures/figure1.png)


## Generation
All experiments are conducted under a 5-shot in-context learning setting.
Therefore, `icl_cnt` is fixed to 5.

Please review `generate.py` for SGMR-NER and `utils.py` for prompts, and change some important parameters.
```{bash}
python generate.py --dataset your_dataset --mode your_mode --picl_cnt your_picl_cnt --icl_cnt 5

```

## Evaluation

Please review `eval.py` for computing entity-level F1 score.
```{bash}
python eval.py --label_path your_label_file_path --pred_path your_model_output_file_path

```
