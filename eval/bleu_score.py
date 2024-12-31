# function to calculate bleu-score for evaluate code-relate tasks for LLM
from nltk.translate.bleu_score import sentence_bleu
import tokenize
import io

def code_tokenize(code_string):
    """Tokenizes a code string using Python's tokenize module."""
    tokens = []
    try:
      for token_info in tokenize.generate_tokens(io.StringIO(code_string).readline):
          if token_info.type != tokenize.COMMENT and token_info.type != tokenize.ENDMARKER and token_info.string.strip():
              tokens.append(token_info.string)
    except tokenize.TokenError:
          tokens = code_string.split() # Fallback to word splitting
    return tokens

def calculate_bleu_score(reference_code, hypothesis_code):
    """Calculates BLEU score for code snippets, using code-specific tokenization."""
    reference_tokens = [code_tokenize(ref) for ref in reference_code] # Allow multiple references
    hypothesis_tokens = code_tokenize(hypothesis_code)
    bleu_score = sentence_bleu(reference_tokens, hypothesis_tokens)

    return bleu_score

reference_code_examples = [
    "def add(x, y):\n    return x + y",
    "def my_sum(a, b):\n  result = a + b\n  return result"
]

hypothesis_code_example_1 = "def add_nums(a, b):\n  return a + b"
hypothesis_code_example_2 = "print('hello')"

# calculate the score
score1 = calculate_bleu_score(reference_code_examples, hypothesis_code_example_1)
score2 = calculate_bleu_score(reference_code_examples, hypothesis_code_example_2)

print(f"BLEU Score 1: {score1:.4f}") # print the score of hypothesis code example 1
print(f"BLEU Score 2: {score2:.4f}") # print the score of hypothesis code example 2
