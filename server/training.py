import json
import torch
from torch.utils.data import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

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


tokenizer = T5Tokenizer.from_pretrained("t5-small")

with open("data/training_pairs.json", "r") as f:
    train_data = json.load(f)

with open("data/training_pairs.json", "r") as f:
    val_data = json.load(f)

def preprocess(example):
    input_enc = tokenizer(example["input"], padding="max_length", truncation=True, max_length=64)
    target_enc = tokenizer(example["target"], padding="max_length", truncation=True, max_length=64)
    return {
        "input_ids": input_enc.input_ids,
        "attention_mask": input_enc.attention_mask,
        "labels": target_enc.input_ids,
    }

train_dataset = list(map(preprocess, train_data))
val_dataset = list(map(preprocess, val_data))

train_ds = RearrangementDataset(train_dataset)
val_ds = RearrangementDataset(val_dataset)


model = T5ForConditionalGeneration.from_pretrained("t5-small")

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=5,
    logging_steps=10,
    save_strategy="no"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
)

trainer.train()


test_input = "rearrange: Alex|nsubj built|root a|det boat|obj"
inputs = tokenizer(test_input, return_tensors="pt")
outputs = model.generate(**inputs, max_length=64)
print("Generated:", tokenizer.decode(outputs[0], skip_special_tokens=True))
