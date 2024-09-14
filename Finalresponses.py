def get_combined_emotion_response(text_emotion, facial_emotion):
    # Define possible emotion combinations and their responses
# Dictionary containing advice for every combination of text and facial emotions
    emotion_responses = {
        ('happy', 'angry'): "Even though you're smiling, it seems like something is really bothering you. It's okay to feel frustrated—let's work through it together.",
        ('happy', 'disgust'): "You might be feeling happy, but there's something that seems to have triggered discomfort. Would you like to share what's troubling you?",
        ('happy', 'fear'): "Happiness with a touch of fear can be confusing. Is there something making you anxious despite the joy?",
        ('happy', 'happy'): "You seem to be in a great mood! Keep up the positivity.",
        ('happy', 'neutral'): "You seem calm but content. Is there something on your mind?",
        ('happy', 'sad'): "It's okay to feel conflicting emotions. How can I help you today?",
        ('happy', 'surprise'): "You seem happily surprised! What made your day better?",
        
        ('sad', 'angry'): "It looks like you're feeling both sad and angry. I'm here to listen to whatever is bothering you.",
        ('sad', 'disgust'): "You seem really upset and disappointed. Let's talk about what’s troubling you.",
        ('sad', 'fear'): "Sadness and fear can be overwhelming. I’m here to help you feel safe and heard.",
        ('sad', 'happy'): "You may be masking your sadness with a smile. Would you like to talk?",
        ('sad', 'neutral'): "It seems like you're feeling a bit low. Let's work through it together.",
        ('sad', 'sad'): "You seem really down today. I'm here to listen. What's bothering you?",
        ('sad', 'surprise'): "It looks like something unexpected has upset you. Let's unpack this together.",
        
        ('love', 'angry'): "It seems like you care deeply but are also feeling frustrated. Would you like to talk about what's bothering you?",
        ('love', 'disgust'): "There might be love, but also a sense of disappointment. Let’s figure out what’s affecting your mood.",
        ('love', 'fear'): "Your emotions are a mix of love and fear. It’s natural to feel protective. What are you worried about?",
        ('love', 'happy'): "Your love is shining through, and it seems like you're in a good place emotionally. Keep spreading the warmth!",
        ('love', 'neutral'): "You're feeling love, but also calm and composed. It’s great to be balanced. How can I support you today?",
        ('love', 'sad'): "You care deeply, but there’s also some sadness. Let’s talk about what’s on your heart.",
        ('love', 'surprise'): "You seem surprised by love! Something unexpected might be happening. How are you feeling about it?",
        
        ('anger', 'angry'): "It seems like you're feeling really upset. Let’s talk through what’s making you angry.",
        ('anger', 'disgust'): "You’re feeling anger and disgust. Something must have really bothered you—let’s address it.",
        ('anger', 'fear'): "Your anger may be coming from a place of fear. Let’s explore what's causing this.",
        ('anger', 'happy'): "You might feel angry, but something's lifting your spirits too. Let’s balance these feelings together.",
        ('anger', 'neutral'): "You’re trying to stay calm, but there’s anger bubbling underneath. Let’s discuss what’s on your mind.",
        ('anger', 'sad'): "You’re dealing with both anger and sadness. I’m here to help you process these complex emotions.",
        ('anger', 'surprise'): "It seems like something has taken you by surprise, fueling your anger. Let’s talk about what happened.",
        
        ('neutral', 'angry'): "You're trying to stay neutral, but there’s some anger behind that calm exterior. Let’s talk through it.",
        ('neutral', 'disgust'): "You seem composed, but there’s a hint of dissatisfaction. What’s bothering you beneath the surface?",
        ('neutral', 'fear'): "You may appear calm, but something’s causing fear. Let’s explore what’s worrying you.",
        ('neutral', 'happy'): "You seem neutral but there’s a bit of joy. How can I support you?",
        ('neutral', 'neutral'): "You seem calm and composed. What's on your mind?",
        ('neutral', 'sad'): "You look neutral, but deep down, you may feel sad. Let’s talk about it.",
        ('neutral', 'surprise'): "You seem calm, but something unexpected might have caught you off guard. Let’s talk about it."
    }


    # Fetch response based on the combination of text and facial emotion
    response = emotion_responses.get((text_emotion, facial_emotion), 
                                     "I'm here for you, no matter what you're feeling.")
    
    return response


# Main entry point for this script
if __name__ == "__main__":
    import sys
    # Get input arguments from the main application (text emotion and facial emotion)
    text_emotion = sys.argv[1]
    facial_emotion = sys.argv[2]
    
    text_emotion = text_emotion.strip().lower()
    facial_emotion = facial_emotion.strip().lower()

    # Get the response for the combination
    response = get_combined_emotion_response(text_emotion, facial_emotion)
    
    # Print the response to be captured by the main script
    print(response)
