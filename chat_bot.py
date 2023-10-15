
#CHATBOT USING CHATTERBOT 

#Import Libraries
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import collections.abc
collections.Hashable=collections.abc.Hashable
import nltk
import warnings
warnings.filterwarnings('ignore')
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Initialize NLTK downloads
nltk.download('punkt')
nltk.download('wordnet')


conversations=['',"I'm sorry, I don't understand. Please ask me something else.",'Hi','Hello! Welcome to Medicare Hospital How can I assist you today?',
                'How can I make an appointment','You can contact the number 7845968245 and book your appointment.',
                'What services does the hospital offer',' provides a range of services including medical consultations, diagnostic tests, surgeries, and more. Is there a specific service you are interested in?',
                'When are the visiting hours','Visiting hours are from 10:00 AM to 3:00 PM. Please note that there may be specific policies in place, especially considering the current health situation. It is advisable to check with the reception for the latest information.',
                'Are there any restrictions on the number of visitors','Yes, Only 2 persons are allowed.',
                'Do you have canteen available','Yes, You can find it near the parking.',
                'What are the main departments in the hospital','Emergency Department, Pediatrics, Surgery, Obstetrics and Gynecology(OB/GYN). Cardiology, Neurology, Oncology, Raiology, Pharmacy, Physical Therapy, Occupational Therapy, Intensive Care Unit (ICU), Psychiatry, Pulmonology, Nephrology, Orthopedics, Urology, Endocrinology, Gastroenterology, Dermatology.',
                'What are the normal time slots for a general check-up','It usually starts from morning 7:00 AM.',
                'Is there a pharmacy on-site','Yes. Pharmacy is located near OP.',
                'From where I can get my medical report','You can enquire about it in the reception.',
                'Can you provide information about your COVID-19 safety protocols','We conduct pre-screening assessments, including temperature checks and symptom questionnaires, at entry points to identify potentially infected individuals.Increased frequency and thoroughness of cleaning and disinfecting high-touch surfaces, equipment, and common areas.Increased frequency and thoroughness of cleaning and disinfecting high-touch surfaces, equipment, and common areas.',
                'How can I get my lab test results online','We do not provide medical results online. Please inquire about it in the Clinical Laboratory Department.',
                'Thanks','Thank You','thank you','Thank you']

#vectorization
tfidf_vectorizer = TfidfVectorizer(tokenizer=word_tokenize, stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(conversations)

#Create a Chatbot
chatbot=ChatBot('mybot')

#Train the bot using the ChatterBotCorpusTrainer
trainer=ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english','chatterbot.corpus.english.conversations')

#Training using ListTrainer
trainer2=ListTrainer(chatbot)
trainer2.train(['',"I'm sorry, I don't understand. Please ask me something else.",'Hi','Hello! Welcome to Medicare Hospital How can I assist you today?',
                'How can I make an appointment','You can contact the number 7845968245 and book your appointment.',
                'What services does the hospital offer',' provides a range of services including medical consultations, diagnostic tests, surgeries, and more. Is there a specific service you are interested in?',
                'When are the visiting hours','Visiting hours are from 10:00 AM to 3:00 PM. Please note that there may be specific policies in place, especially considering the current health situation. It is advisable to check with the reception for the latest information.',
                'Are there any restrictions on the number of visitors','Yes, Only 2 persons are allowed.',
                'Do you have canteen available','Yes, You can find it near the parking.',
                'What are the main departments in the hospital','Emergency Department, Pediatrics, Surgery, Obstetrics and Gynecology(OB/GYN). Cardiology, Neurology, Oncology, Raiology, Pharmacy, Physical Therapy, Occupational Therapy, Intensive Care Unit (ICU), Psychiatry, Pulmonology, Nephrology, Orthopedics, Urology, Endocrinology, Gastroenterology, Dermatology.',
                'What are the normal time slots for a general check-up','It usually starts from morning 7:00 AM.',
                'Is there a pharmacy on-site','Yes. Pharmacy is located near OP.',
                'From where I can get my medical report','You can enquire about it in the reception.',
                'Can you provide information about your COVID-19 safety protocols','We conduct pre-screening assessments, including temperature checks and symptom questionnaires, at entry points to identify potentially infected individuals.Increased frequency and thoroughness of cleaning and disinfecting high-touch surfaces, equipment, and common areas.Increased frequency and thoroughness of cleaning and disinfecting high-touch surfaces, equipment, and common areas.',
                'How can I get my lab test results online','We do not provide medical results online. Please inquire about it in the Clinical Laboratory Department.',
                'Thanks','Thank You','thank you','Thank you'])

def preprocess_text(text):

    tokens=word_tokenize(text)
    lemmatizer=WordNetLemmatizer()
    tokens=[lemmatizer.lemmatize(word) for word in tokens]
    preprocessed_text=' '.join(tokens)
    preprocessed_text = ''.join(e for e in preprocessed_text if (e.isalnum() or e.isspace()))
    return preprocessed_text

def get_bot_response(user_input):
    preprocessed_input = preprocess_text(user_input)
    response = chatbot.get_response(preprocessed_input)
    return str(response)

def get_most_similar_response(user_input):
    user_tfidf = tfidf_vectorizer.transform([user_input])
    similarities = cosine_similarity(user_tfidf, tfidf_matrix)
    most_similar_index = similarities.argmax()
    most_similar_response = conversations[most_similar_index+1]
    return most_similar_response
    

while True:
    user_input = input('You: ')
    if user_input.lower()=='bye':
        print('Bot: Bye')
        break
    else:
        if user_input.lower() in ['','Hi','How can I make an appointment','What services does the hospital offer','When are the visiting hours',
                                 'Are there any restrictions on the number of visitors','Do you have canteen available','What are the main departments in the hospital',
                                 'What are the normal time slots for a general check-up','Is there a pharmacy on-site','From where I can get my medical report',
                                 'Can you provide information about your COVID-19 safety protocols','How can I get my lab test results online','Thanks','thank you']:
            bot_response=chatbot.get_response(user_input)
            
        else: 

            bot_response=get_most_similar_response(user_input)
        print("Bot:", bot_response)
        

