import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def generate_advice(personal_details, emotions):
    model_name = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    prompt = f"""Task: Generate helpful and safe mental health advice
Context: Person details:
{', '.join([f'{k}: {v}' for k, v in personal_details.items()])}
Current emotions: {' and '.join(emotions)}

Instructions: Provide caring and practical advice considering their:
1. Demographics and life situation
2. Current emotional state
3. Health and trauma history
4. Coping strategies and self-care tips
5. Guidelines for seeking professional help

Generate advice:"""
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
        **inputs,
        max_length=512,
        min_length=100,
        num_return_sequences=1,
        temperature=0.7,
        do_sample=True,
        no_repeat_ngram_size=2,
        length_penalty=1.0
    )

    advice = tokenizer.decode(outputs[0], skip_special_tokens=True)

    disclaimer = "\n\nDisclaimer: This advice is meant to offer suggestions but should not replace professional mental health care."
    return advice + disclaimer

if __name__ == "__main__":
    text_emotion = sys.argv[1]
    facial_emotion = sys.argv[2]
    user_details = {sys.argv[i]: sys.argv[i+1] for i in range(3, len(sys.argv), 2)}

    emotions = [text_emotion, facial_emotion]
    advice = generate_advice(user_details, emotions)
    print(advice)
