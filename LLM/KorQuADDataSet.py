from datasets import load_dataset, Dataset
from transformers import AutoTokenizer
import os
import datasets

file_path = 'train.json'
if not os.path.exists(file_path):
    print('train.json 파일이 없습니다.')

try:
    dataset = load_dataset('json', data_files='data',cache_dir=None)
    print('데이터 로드 성공')
except Exception as e:
    print(f"에러 : {e}")
    raise ValueError()

# 데이터 플랫화
def flatten_data(dataset):
    temp_datasets = []
    for item in dataset['train']:
        for pragraph in item['pragraphs']:
            context = pragraph.get('context','')
            for qa in pragraph['qas']:
                


def main():
    if __name__ == "__main__":
        print('trai')

        # Load the KorQuAD dataset
        dataset = load_dataset('KorQuAD', split='train')

        # Print the first example
        print(dataset[0])

        # Load the tokenizer
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

        # Tokenize the dataset
        def tokenize_function(examples):
            return tokenizer(examples['context'], examples['question'], truncation=True)

        tokenized_datasets = dataset.map(tokenize_function, batched=True)

        # Print the first tokenized example
        print(tokenized_datasets[0])