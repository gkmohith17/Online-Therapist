def get_combined_emotion_response(text_emotion, facial_emotion):
    emotion_responses = {
        ('happy', 'angry'): "Even though you're smiling, it seems like something is really bothering you deep inside. It’s important to acknowledge these conflicting feelings. Life can be overwhelming, and I’m here to help you explore what’s causing this frustration. Let’s work through it together and find some clarity.",
        ('happy', 'disgust'): "You might be feeling happy, but it seems like there’s something that triggered discomfort or disappointment in your surroundings. It’s okay to have mixed emotions; sometimes happiness can be overshadowed by other feelings. Would you like to share what’s troubling you? Talking about it might lighten your load.",
        ('happy', 'fear'): "Happiness mixed with a touch of fear can be confusing and disorienting. There might be something making you anxious despite the joy you’re feeling. It’s completely normal to experience these dual emotions, and I’m here to help you sort through them. What’s been on your mind lately that’s causing this unease?",
        ('happy', 'happy'): "You seem to be in a fantastic mood! Your happiness is contagious, and it’s wonderful to see you radiating such positivity. Keep embracing this joy and let it inspire you. Is there something in particular that’s made your day so bright?",
        ('happy', 'neutral'): "You seem calm but content, striking a balance between happiness and tranquility. It’s great to feel peaceful, but is there something on your mind that you’d like to explore? Sometimes, even in calmness, our thoughts can be busy, and I’m here to listen.",
        ('happy', 'sad'): "It's perfectly okay to feel conflicting emotions like happiness and sadness at the same time. Life is a complex tapestry of experiences. How can I help you today? It might be beneficial to explore these feelings further and understand what’s behind them.",
        ('happy', 'surprise'): "You seem happily surprised! Surprises can bring joy and excitement, but they can also leave us feeling a bit disoriented. What made your day better? Sharing your joy might deepen that happiness and help you appreciate the moment even more.",
        
        ('sad', 'angry'): "It looks like you're feeling both sad and angry, a combination that can feel heavy. I’m here to listen to whatever is bothering you. It’s crucial to express these emotions—what’s been on your mind? Sometimes, acknowledging these feelings can be the first step toward healing.",
        ('sad', 'disgust'): "You seem really upset and disappointed, feelings that can weigh heavily on your heart. Let’s talk about what’s troubling you; discussing it may help alleviate some of that distress. You’re not alone in this—let's work together to find a way forward.",
        ('sad', 'fear'): "Sadness and fear can be overwhelming, creating a sense of heaviness that’s hard to shake off. I’m here to help you feel safe and heard as you navigate these emotions. It’s okay to reach out; sharing your worries might lighten the burden you’re carrying.",
        ('sad', 'happy'): "You may be masking your sadness with a smile, which is more common than you might think. Would you like to talk about what’s behind your smile? I’m here to help you explore these feelings and find a way to feel more at peace.",
        ('sad', 'neutral'): "It seems like you're feeling a bit low, yet there’s a sense of calmness in your demeanor. Let’s work through it together. It’s okay to acknowledge sadness while also recognizing moments of peace. I’m here to support you through this.",
        ('sad', 'sad'): "You seem really down today, and it’s important to talk about it. I’m here to listen and help you process what’s bothering you. Remember, it’s okay to feel this way, and expressing it can often bring relief.",
        ('sad', 'surprise'): "It looks like something unexpected has upset you, which can be jarring. Let’s unpack this together; understanding the root of your surprise may help you navigate your feelings more effectively.",
        
        ('love', 'angry'): "It seems like you care deeply but are also feeling frustrated. Would you like to talk about what's bothering you? Sometimes, love can bring out strong emotions, and it’s important to address any underlying issues to find balance.",
        ('love', 'disgust'): "There might be love present, but also a sense of disappointment that’s hard to ignore. Let’s figure out what’s affecting your mood; expressing these feelings can lead to clarity and understanding.",
        ('love', 'fear'): "Your emotions are a mix of love and fear, which can create a protective instinct. It’s natural to feel worried about those we care for. What are you worried about? Talking it out might help alleviate some of that anxiety.",
        ('love', 'happy'): "Your love is shining through, and it seems like you're in a good place emotionally. Keep spreading the warmth! Embracing love can be incredibly uplifting; is there something specific that’s contributing to your happiness?",
        ('love', 'neutral'): "You're feeling love, but also calm and composed. It’s great to be balanced. How can I support you today? Sometimes, reflecting on what brings you joy can enhance that feeling even more.",
        ('love', 'sad'): "You care deeply, but there’s also some sadness lingering in your heart. Let’s talk about what’s on your mind. It’s okay to feel both love and sadness; sharing your feelings can lead to healing.",
        ('love', 'surprise'): "You seem surprised by love! Something unexpected might be happening in your life. How are you feeling about it? Understanding your feelings can lead to deeper insights and acceptance.",
        
        ('anger', 'angry'): "It seems like you're feeling really upset, and that’s entirely valid. Let’s talk through what’s making you angry; expressing your feelings can often bring relief and clarity.",
        ('anger', 'disgust'): "You’re feeling anger and disgust, emotions that often accompany each other. Something must have really bothered you—let’s address it. Understanding what’s behind those feelings can be a crucial step toward resolution.",
        ('anger', 'fear'): "Your anger may be coming from a place of fear. Let’s explore what's causing this; often, understanding the root can help in managing these intense emotions.",
        ('anger', 'happy'): "You might feel angry, but something's lifting your spirits too. Let’s balance these feelings together. It’s okay to experience a mix of emotions; acknowledging them can lead to greater emotional understanding.",
        ('anger', 'neutral'): "You’re trying to stay calm, but there’s anger bubbling underneath the surface. Let’s discuss what’s on your mind; exploring these feelings can help you find a more balanced emotional state.",
        ('anger', 'sad'): "You’re dealing with both anger and sadness, a complex combination that can be challenging. I’m here to help you process these emotions. It’s important to talk about how you’re feeling.",
        ('anger', 'surprise'): "It seems like something has taken you by surprise, fueling your anger. Let’s talk about what happened; understanding the trigger can help you navigate your feelings.",
        
        ('neutral', 'angry'): "You're trying to stay neutral, but there’s some anger behind that calm exterior. Let’s talk through it; sometimes, acknowledging these feelings can bring relief.",
        ('neutral', 'disgust'): "You seem composed, but there’s a hint of dissatisfaction. What’s bothering you beneath the surface? It’s important to explore those feelings for better emotional clarity.",
        ('neutral', 'fear'): "You may appear calm, but something’s causing fear. Let’s explore what’s worrying you; discussing it might help alleviate some of that anxiety.",
        ('neutral', 'happy'): "You seem neutral but there’s a bit of joy. How can I support you? Reflecting on those joyful moments can enhance your emotional well-being.",
        ('neutral', 'neutral'): "You seem calm and composed. What's on your mind? It’s perfectly okay to take a moment to reflect on your feelings.",
        ('neutral', 'sad'): "You look neutral, but deep down, you may feel sad. Let’s talk about it; acknowledging those feelings can be the first step toward healing.",
        ('neutral', 'surprise'): "You seem calm, but something unexpected might have caught you off guard. Let’s talk about it; understanding your reactions can lead to better emotional insight."
    }

    response = emotion_responses.get((text_emotion, facial_emotion), 
                                     "I'm here for you, no matter what you're feeling. Every emotion is valid, and talking about them can help you find clarity.")
    
    return response

if __name__ == "__main__":
    import sys
    text_emotion = sys.argv[1]
    facial_emotion = sys.argv[2]
    text_emotion = text_emotion.strip().lower()
    facial_emotion = facial_emotion.strip().lower()
    response = get_combined_emotion_response(text_emotion, facial_emotion)
    print(response)
