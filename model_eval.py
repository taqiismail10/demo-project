import re

import evaluate
import numpy as np
import torch
from datasets import load_dataset
from scipy.stats import spearmanr
from transformers import (
    AutoModelForQuestionAnswering,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline,
)

SQUAD_MODEL_NAME = "distilbert-base-uncased-distilled-squad"
GSM8K_MODEL_NAME = "google/flan-t5-small"
SQUAD_SAMPLE_SIZE = 10
GSM8K_SAMPLE_SIZE = 10
PLOT_PATH = "model_eval_plot.png"


# Pretraining loss prediction function (log-law)
def predict_loss(pretraining_data_size, A, alpha, beta):
    return (np.log(A * pretraining_data_size**alpha)) ** beta


# Function to compute task performance for SQuAD and GSM8K

def evaluate_squad(model_name, sample_size=SQUAD_SAMPLE_SIZE):
    squad_eval = load_dataset("squad", split="validation").select(range(sample_size))
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    qa_pipeline = pipeline(
        "question-answering",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,
    )
    predictions = []
    references = []
    for row in squad_eval:
        prediction = qa_pipeline(question=row["question"], context=row["context"])
        predictions.append({"id": row["id"], "prediction_text": prediction["answer"]})
        references.append({"id": row["id"], "answers": row["answers"]})
    metric = evaluate.load("squad")
    scores = metric.compute(predictions=predictions, references=references)
    return scores["exact_match"], scores["f1"]


def extract_gsm8k_answer(text):
    match = re.search(r"####\s*([-+]?\d+[\d,]*)", text)
    if match:
        return match.group(1).replace(",", "")
    fallback = re.findall(r"[-+]?\d+[\d,]*", text)
    if not fallback:
        return ""
    return fallback[-1].replace(",", "")


def evaluate_gsm8k(model_name, sample_size=GSM8K_SAMPLE_SIZE):
    gsm8k_eval = load_dataset("gsm8k", "main", split="test").select(range(sample_size))
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    correct = 0
    for row in gsm8k_eval:
        inputs = tokenizer(
            row["question"],
            return_tensors="pt",
            truncation=True,
        ).to(device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=64,
        )
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
        predicted_answer = extract_gsm8k_answer(prediction)
        target_answer = extract_gsm8k_answer(row["answer"])
        if predicted_answer == target_answer and predicted_answer != "":
            correct += 1
    return correct / sample_size


# Define the function to calculate Pearson & Spearman correlations

def compute_correlation(predicted_losses, task_scores):
    # Pearson correlation
    pearson_corr = np.corrcoef(predicted_losses, task_scores)[0, 1]

    # Spearman correlation
    spearman_corr, _ = spearmanr(predicted_losses, task_scores)

    return pearson_corr, spearman_corr


# Main loop for training and evaluating models with different pretraining data sizes
pretraining_data_sizes = [10**6, 10**7, 10**8]  # Example sizes
A, alpha, beta = 0.5, 1.2, 2.1  # Example log-law parameters

predicted_losses = []
task_scores_squad = []
task_scores_gsm8k = []

for data_size in pretraining_data_sizes:
    # Predict pretraining loss
    predicted_loss = predict_loss(data_size, A, alpha, beta)
    predicted_losses.append(predicted_loss)

    # Evaluate on SQuAD
    em, f1 = evaluate_squad(SQUAD_MODEL_NAME)
    task_scores_squad.append((em, f1))

    # Evaluate on GSM8K
    accuracy = evaluate_gsm8k(GSM8K_MODEL_NAME)
    task_scores_gsm8k.append(accuracy)

# Evaluate correlations between predicted loss and task scores
pearson_corr_squad, spearman_corr_squad = compute_correlation(
    predicted_losses, [score[1] for score in task_scores_squad]
)
pearson_corr_gsm8k, spearman_corr_gsm8k = compute_correlation(
    predicted_losses, task_scores_gsm8k
)

# Print results
print("SQuAD Exact Match scores: ", [score[0] for score in task_scores_squad])
print("SQuAD F1 scores: ", [score[1] for score in task_scores_squad])
print("GSM8K Accuracy scores: ", task_scores_gsm8k)
print("SQuAD Pearson Correlation: ", pearson_corr_squad)
print("SQuAD Spearman Correlation: ", spearman_corr_squad)
print("GSM8K Pearson Correlation: ", pearson_corr_gsm8k)
print("GSM8K Spearman Correlation: ", spearman_corr_gsm8k)

# Plot the results for visualization
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(
    predicted_losses,
    [score[1] for score in task_scores_squad],
    label="SQuAD F1",
    marker="o",
)
plt.plot(
    predicted_losses,
    task_scores_gsm8k,
    label="GSM8K Accuracy",
    marker="x",
)
plt.xlabel("Predicted Loss")
plt.ylabel("Task Performance")
plt.legend()
plt.tight_layout()
plt.savefig(PLOT_PATH)
