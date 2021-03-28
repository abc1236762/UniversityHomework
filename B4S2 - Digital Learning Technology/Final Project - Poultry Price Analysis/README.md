# Poultry Price Analysis

## Setup

1. Install [Node.js LTS](https://nodejs.org/en/download/) and [Yarn](https://classic.yarnpkg.com/en/docs/install).

2. Use [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/individual) to setup Python environment.

    ```sh
    conda create -n ppa --strict-channel-priority -y \
          python=3 numpy scikit-learn pylint autopep8 rope
    conda activate ppa
    conda config --env --set channel_priority strict
    conda deactivate
    ```

3. Execute below script in `./ppa/frontend` to build the project.

    ```sh
    yarn
    yarn build
    ```

## Run

Execute below script in  in project directory to run.

```sh
conda activate ppa
python -m ppa
```
