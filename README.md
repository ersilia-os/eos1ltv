# SIMG Chemical Embeddings

Chemical Representation and Interaction Discovery with Stereoelectronics-Infused Molecular Graphs. This work introduces a novel approach to infusing quantum-chemical-rich information into molecular graphs via stereoelectronic effects.

This model was incorporated on 2026-09-07.Last packaged on 2026-09-15.

## Information
### Identifiers
- **Ersilia Identifier:** `eos1ltv`
- **Slug:** `simg-chemical-embeddings`

### Domain
- **Task:** `Representation`
- **Subtask:** `Featurization`
- **Biomedical Area:** `Any`
- **Target Organism:** `Any`
- **Tags:** `Embedding`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `128`
- **Output Consistency:** `Fixed`
- **Interpretation:** The output of this template model should be interpreted like this.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| feat_000 | float |  | embedding feature 0 |
| feat_001 | float |  | embedding feature 1 |
| feat_002 | float |  | embedding feature 2 |
| feat_003 | float |  | embedding feature 3 |
| feat_004 | float |  | embedding feature 4 |
| feat_005 | float |  | embedding feature 5 |
| feat_006 | float |  | embedding feature 6 |
| feat_007 | float |  | embedding feature 7 |
| feat_008 | float |  | embedding feature 8 |
| feat_009 | float |  | embedding feature 9 |

_10 of 128 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos1ltv](https://hub.docker.com/r/ersiliaos/eos1ltv)
- **Docker Architecture:** `AMD64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos1ltv.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos1ltv.zip)

### Resource Consumption
- **Model Size (Mb):** `21`
- **Environment Size (Mb):** `1630`
- **Image Size (Mb):** `1725.48`

**Computational Performance (seconds):**
- 10 inputs: `33.02`
- 100 inputs: `253.29`
- 10000 inputs: `-1`

### References
- **Source Code**: [https://github.com/gomesgroup/simg](https://github.com/gomesgroup/simg)
- **Publication**: [https://doi.org/10.1038/s42256-025-01031-9](https://doi.org/10.1038/s42256-025-01031-9)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2025`
- **Ersilia Contributor:** [SoufianeAatab](https://github.com/SoufianeAatab)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [CC-BY-4.0](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos1ltv
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos1ltv
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
