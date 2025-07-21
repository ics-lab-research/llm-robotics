# Empowering Universal Robot Programming with Fine-Tuned Large Language Models

This repository contains the official code and resources for the paper:

**"Empowering Universal Robot Programming with Fine-Tuned Large Language Models"**
DOI: [10.4108/airo.8983](https://doi.org/10.4108/airo.8983)

## 🎥 Demo Video
Watch our demo video showcasing the capabilities of Qwen2.5 fine-tuned for URScript generation:
[Qwen2.5 for URScript: A Fine-Tuned Demo](https://www.youtube.com/watch?v=yr4ICo1q6MQ)

## 🌟 Overview
This project focuses on leveraging Large Language Models (LLMs) to simplify and enhance the programming of Universal Robots (UR) using URScript. We provide a comprehensive framework for generating high-quality URScript code from natural language instructions by fine-tuning state-of-the-art LLMs.

## ✨ Features
*   **Dataset Generation**: Scripts to create a diverse dataset of URScript programming tasks.
*   **Instruction Tuning**: Code for fine-tuning LLMs (e.g., Qwen) on URScript generation tasks.
*   **Evaluation Benchmarks**: Tools to evaluate the performance of fine-tuned models using metrics like CodeBLEU.
*   **Deployment Examples**: Python scripts to connect to UR robots and deploy generated URScript programs.
*   **Interactive GUI**: A Chainlit-based web interface for real-time interaction with the fine-tuned LLM.

## 🚀 Getting Started

### Prerequisites
*   Python 3.9+
*   Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
    *(Note: Replace `your-username/your-repo-name` with the actual repository path)*

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    Install core dependencies:
    ```bash
    pip install -r dev-requirements.txt
    ```
    For specific components, install their respective requirements:
    ```bash
    pip install -r dataset/requirements.txt
    pip install -r instruct-tuning/requirements.txt
    pip install -r eval/requirements.txt
    pip install -r deploying/requirements.txt
    pip install -r gui/requirements.txt
    pip install -r notebooks/requirements.txt
    pip install -r tests/requirements.txt
    ```
    Or, to install all at once:
    ```bash
    pip install -r dev-requirements.txt -r dataset/requirements.txt -r instruct-tuning/requirements.txt -r eval/requirements.txt -r deploying/requirements.txt -r gui/requirements.txt -r notebooks/requirements.txt -r tests/requirements.txt
    ```

## 📂 Repository Structure

*   `dataset/`: Contains scripts for dataset generation, raw URScript examples, and processed seed tasks.
    *   `gen_seeds.py`: Script to generate `seed_tasks.json`.
    *   `raw-data/`: Original URScript examples categorized by complexity.
    *   `tasks/`: Structured tasks for instruction tuning (input, instruction, output).
*   `instruct-tuning/`: Scripts and prompts for fine-tuning LLMs.
    *   `generate_instruction_gemini.py`: Script to generate instruction-following data using Gemini.
    *   `prompts/`: Prompt templates for instruction generation.
    *   `utils.py`: Utility functions for data handling and API calls.
*   `eval/`: Evaluation scripts and test cases.
    *   `bleu_score.py`: Script for calculating CodeBLEU scores.
    *   `get_output_gemini.py`: Script to get model outputs for evaluation.
    *   `test-cases/`: Example test URScript files.
*   `deploying/`: Scripts for deploying URScript to a robot.
    *   `deploying-urscript.py`: Main script for sending URScript to the robot.
    *   `example.py`: Example usage of the deployment script.
    *   `get_position.py`: Script to retrieve robot's current position.
    *   `rtde.py`: Example using RTDE for real-time data exchange.
*   `gui/`: Chainlit application for interactive demonstration.
    *   `app.py`: Main Chainlit application.
    *   `app-groq.py`: Chainlit application configured for Groq API.
*   `notebooks/`: Jupyter notebooks for experimentation, data analysis, and model testing.
*   `refs/`: Relevant research papers and UR documentation.
*   `tests/`: Unit tests for various components.

## 🛠️ Usage

### 1. Dataset Preparation
To prepare the instruction-following dataset:
```bash
python dataset/gen_seeds.py
python instruct-tuning/generate_instruction_gemini.py
```
This will generate `seed_tasks.json` and then `test_instructions.json` (or `gen_instructions.json`) in `instruct-tuning/results/`.

### 2. Model Fine-tuning
*(Details on fine-tuning specific LLMs like Qwen would go here, e.g., commands for Hugging Face `transformers` or specific training scripts. This part is not explicitly in the provided file summaries, so it's a placeholder.)*

### 3. Evaluation
To evaluate the performance of a generated model output:
```bash
python eval/get_output_gemini.py # To generate outputs from a model
python eval/bleu_score.py # To calculate BLEU scores
```

### 4. Deploying to a UR Robot
Ensure your robot's IP address is correctly configured in the deployment scripts (e.g., `deploying/deploying-urscript.py`, `deploying/example.py`).
```bash
python deploying/deploying-urscript.py
```
You can modify `deploying/example.py` to test sending a sample script.

### 5. Running the GUI
To run the interactive Chainlit application:
```bash
chainlit run gui/app.py -w
```
If you are using Groq API:
```bash
chainlit run gui/app-groq.py -w
```
Make sure to set your `GROQ_API` environment variable if using `app-groq.py`.

## 🤝 Contributing
Contributions are welcome! Please feel free to open an issue or submit a pull request.

## 📄 License
This project is licensed under the [MIT License](LICENSE). *(Note: Assuming MIT License, please create a LICENSE file if it doesn't exist or specify the correct license.)*

## ✍️ Citation
If you find this work useful, please cite our paper:

```bibtex
@article{your_paper_title,
  title={Empowering Universal Robot Programming with Fine-Tuned Large Language Models},
  author={Author One and Author Two and Author Three},
  journal={AIRO},
  year={2024}, # Adjust year if needed
  doi={10.4108/airo.8983}
}
```
*(Note: Please replace `Author One`, `Author Two`, `Author Three`, and `your_paper_title` with the actual author names and title from your paper.)*
