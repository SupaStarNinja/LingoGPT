import json
import torch
import os
from torch.utils.data import Dataset
from yoda import Yoda
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

import torch
print("CUDA available?", torch.cuda.is_available())
print("GPU count:", torch.cuda.device_count())
print("GPU name:", torch.cuda.get_device_name(0))

class RearrangementDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __len__(self):
        return len(self.encodings)

    def __getitem__(self, idx):
        return {
            "input_ids": torch.tensor(self.encodings[idx]["input_ids"]),
            "attention_mask": torch.tensor(self.encodings[idx]["attention_mask"]),
            "labels": torch.tensor(self.encodings[idx]["labels"]),
        }

print("Training")
tokenizer = T5Tokenizer.from_pretrained("t5-small")
input_parser = Yoda(training=True)
data_dir = os.path.join(os.path.dirname(__file__), 'data')

with open(os.path.join(data_dir, 'training_pairs.json'), 'r') as f:
    train_data = json.load(f)

with open(os.path.join(data_dir, 'testing_pairs.json'), 'r') as f:
    val_data = json.load(f)

def preprocess(example):
    input_enc = tokenizer(input_parser.prepare_input(example["input"]), padding="max_length", truncation=True, max_length=256)
    target_enc = tokenizer(example["output"], padding="max_length", truncation=True, max_length=256)
    return {
        "input_ids": input_enc.input_ids,
        "attention_mask": input_enc.attention_mask,
        "labels": target_enc.input_ids,
    }

train_dataset = list(map(preprocess, train_data['examples']))
val_dataset = list(map(preprocess, val_data['examples']))

train_ds = RearrangementDataset(train_dataset)
val_ds = RearrangementDataset(val_dataset)


model = T5ForConditionalGeneration.from_pretrained("t5-base")

training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=10,
    per_device_eval_batch_size=10,
    num_train_epochs=500,
    warmup_steps=500,
    learning_rate=3e-5,
    logging_steps=10,
    load_best_model_at_end=True,
    save_strategy="best",
    fp16=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
)

trainer.train()

model_save_path = os.path.join(os.path.dirname(__file__), 'models', 'testing_model')
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)

# Load the fine-tuned model for testing
model = T5ForConditionalGeneration.from_pretrained(model_save_path)
tokenizer = T5Tokenizer.from_pretrained(model_save_path)

test_input = "My name is ruthusford"
inputs = tokenizer(test_input, return_tensors="pt")
outputs = model.generate(**inputs, max_length=256)
print("Generated:", tokenizer.decode(outputs[0], skip_special_tokens=True))

test_input = "He will be tested."
inputs = tokenizer(test_input, return_tensors="pt")
outputs = model.generate(**inputs, max_length=256)
print("Generated:", tokenizer.decode(outputs[0], skip_special_tokens=True))

test_input = "The future is in your hands."
inputs = tokenizer(test_input, return_tensors="pt")
outputs = model.generate(**inputs, max_length=256)
print("Generated:", tokenizer.decode(outputs[0], skip_special_tokens=True))
