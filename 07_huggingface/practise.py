from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')

result = generator("old age life", max_length=30, num_return_sequences=1)

print(result[0]['generated_text'])  




