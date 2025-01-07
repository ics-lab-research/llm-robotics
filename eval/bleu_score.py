# function to calculate bleu-score for evaluate code-relate tasks for LLM
import fire
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

from utils import instruction_data_loader


# calculate avg of a list
def calculate_average(lst):
    if not isinstance(lst, list) or len(lst) == 0:
        raise ValueError("Input must be a non-empty list")
    return sum(lst) / len(lst)


def calculate_code_bleu(reference_code, candidate_code, n=4):
    """
    Calculates the BLEU score for code-related tasks.

    Args:
        reference_code: A string representing the reference code.
        candidate_code: A string representing the candidate (generated) code.
        n: The maximum n-gram order for BLEU calculation (default is 4).

    Returns:
        The BLEU score as a float between 0 and 1.
    """

    reference_tokens = [
        code.split() for code in [reference_code]
    ]  # convert to list of list of token
    candidate_tokens = candidate_code.split()

    smoothing = SmoothingFunction().method1  # adjust for zero scores
    bleu_score = sentence_bleu(
        reference_tokens,
        candidate_tokens,
        weights=tuple([1 / n] * n),
        smoothing_function=smoothing,
    )

    return bleu_score


def benchmark_bleu_score(instruction_path="./results/output_qwen7b_coder.json"):
    bleu_scores = []
    reference_code_data = instruction_data_loader()
    hypothesis_code_data = instruction_data_loader(
        instruction_path=instruction_path
    )

    for idx, item in enumerate(reference_code_data):
        reference_code = item["output"]
        hypothesis_code = hypothesis_code_data[idx]["output"]

        bleu_score = calculate_code_bleu(reference_code, hypothesis_code)
        bleu_scores.append(bleu_score)
        # print(bleu_score)

    result = calculate_average(bleu_scores)
    print(f"Avg bleu score is {result}")
    # print(bleu_scores)


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
