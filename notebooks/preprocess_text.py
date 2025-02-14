#!/usr/bin/env python
# coding: utf-8

# In[5]:


import re
import unicodedata
from nltk.stem import PorterStemmer 
from nltk.stem import WordNetLemmatizer
from queue import Queue


# In[79]:


class Preprocess:
        
        # --------------------------------------- Constructor --------------------------------------- 
        
        def __init__(self,stopword_list):
            self.data_path = ''
            self.stopword_list = stopword_list
                

        # --------------------------------------- Preprocess --------------------------------------- 
        
        def expand_concatenations(self, word):
            
            
            if not re.match('[a-zA-Z]+', word) or re.match('/d+',word):
                for i in range(len(word)):
                    if not('DEVANAGARI ' in unicodedata.name(word[i])):
                        word = word[:i] if( len(word[i:]) < 2 and not word[i:].isnumeric()) else word[:i] + " " + word[i:]
                        break
            else:
                for i in range(len(word)):
                    if ('DEVANAGARI ' in unicodedata.name(word[i])):
                        word = word[i:] if( len(word[:i]) < 2 and not word[:i].isnumeric() ) else word[:i] + " " + word[i:]
                        break

            return(word)
    
        
        def clean_text(self,text: str) -> str:
            try:
                special_chars = r'''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                stemmer = PorterStemmer()
                lemmatizer = WordNetLemmatizer()

                if not(isinstance(text, str)): text = str(text)

                #Removing unprintable characters
                text = ''.join(x for x in text if x.isprintable())

                # Cleaning the urls
                text = re.sub(r'https?://\S+|www\.\S+', '', text)

                # Cleaning the html elements
                text = re.sub(r'<.*?>', '', text)

                # Removing the punctuations
                text = re.sub('[!#?,.:";-@#$%^&*_~<>()-]', '', text)


                # Removing stop words
                text = ' '.join([word for word in text.split() if word not in self.stopword_list])

                # Expanding noisy concatenations (Eg: algorithmआणि  -> algorithm आणि ) 
                text = ' '.join([self.expand_concatenations(word) for word in text.split()])

#                 preprocessed_text = ""

#                 for word in text.split(): 
#                     if (re.match('\d+', word)):
#                         if(word.isnumeric()):
#                             preprocessed_text = preprocessed_text + '#N' + " "
#                         else:
#                             preprocessed_text = preprocessed_text + word.lower() + " "

#                     else:
#                         if(re.match('[a-zA-Z]+', word)):
#                             if not len(word) < 2:
#                                 word = word.lower()
#     #                             word = lemmatizer.lemmatize(word, pos='v')
#                                 preprocessed_text = preprocessed_text + word + " "

#                         else:
#                             preprocessed_text = preprocessed_text + word + " "

#                 return preprocessed_text
                return text
            
            except ValueError as ve:
                print('Error processing:\t',text)
                return ''
    
        def preprocess_text(self,text: str) -> str:

            try:
                if not(isinstance(text, str)): text = str(text)
                preprocessed_text = ""

                for word in text.split(): 
                    if (re.match('\d+', word)):
                        if(word.isnumeric()):
                            preprocessed_text = preprocessed_text + '#N' + " "
                        else:
                            preprocessed_text = preprocessed_text + word.lower() + " "

                    else:
                        if(re.match('[a-zA-Z]+', word)):
                            if not len(word) < 2:
                                word = word.lower()
    #                             word = lemmatizer.lemmatize(word, pos='v')
                                preprocessed_text = preprocessed_text + word + " "

                        else:
                            preprocessed_text = preprocessed_text + word + " "

                return preprocessed_text

            except ValueError as ve:
                print('Error processing:\t',text)
                return ''
            
        def split_devanagri_word(self,word: str, punctuations = True) -> str:
            try:
                q = Queue()
                if not(isinstance(word, str)): word = str(word)
                tokens = []
                
                for char in word:
#                     print(char, '--->', unicodedata.name(char))

                    if 'letter' in unicodedata.name(char).lower():
                        if q.empty():
                            tokens.append(char)
                        else:
                            while not q.empty():
                                tokens[len(tokens)-1] += q.get() 
                            tokens.append(char)   
                    else:
                        if punctuations == True:
                            q.put(char)

                while not q.empty():
                    tokens[len(tokens)-1] += q.get() 
                
                return tokens
                
            except ValueError as ve:
                print('Error processing:\t',text)
                return ''
        
        def text2characters(self,text:str, punctuations = True)->str:
            try:
                if not(isinstance(text, str)): text = str(text)
                char_sequence = ""
                char_list = []
                
                for word in text.split():
                    seq = ' '.join([char for char in self.split_devanagri_word(word, punctuations)])                
                    char_sequence = char_sequence + seq + ' '
    
                    print(word,'--->',seq)
                    
                return char_sequence
            
            except ValueError as ve:
                print('Error processing:\t',text)
                return ''
            
        def devanagri_tokenizer(self,char_sequence):
            for char in char_sequence:
                print(char)


# In[80]:


if __name__ == '__main__':
    
    import pandas as pd
    df = pd.read_csv('../Technodifacation/Data/training_data_marathi.csv')
    
    sampletext1 = df['text'].sample().values
    print(sampletext1)
    pp = Preprocess([])
    sampletext2 = 'त्यांना जनतेला पटवून द्यावे लागेल99'

    test_list1 = ['त्यांना','H20', '2H20','Animal2Animal' ,'सी२ओ२', 'लागेल99', 'Animalत्यांना',
                 'त्यांनाAnimal', 'Analogy_त्यांना', 'Science२१', '१२Number', '!@)$&%!#)&$!&$!$B Bo ', '११.२२','I', '१','1','11.22','a','B','सी']

    test_list2 = ['त्यांना CO2 2H20 सीओ२ लागेल99 , Animalत्यांना त्यांनाAnimal Analogy_त्यांना Science२१ १२Number',
                 '!@)$&%!#)&$!&$!$I am Atharva ११.२२ Kulkarni 11.22 a B 1 सी']

    for text in test_list2:
        print(text, '\t--->\t', pp.clean_text(text),'\n')   


# In[81]:


pp = Preprocess([])


# In[ ]:


sample_word =  "दर्शविले"
tokens = pp.split_devanagri_word(sample_word, punctuations=True)
tokens


# In[82]:


text = 'पहिला,  स्तंभ आपल्याला अंदाज देतो.'

clean_text = pp.clean_text(text)

char_sequence_1 = pp.text2characters(clean_text)
char_sequence_2 = pp.text2characters(clean_text, punctuations=False)
print('\nText: ',clean_text,'\n\nWith Punctuations: ',char_sequence_1,'\n\nOnly Letters: ',char_sequence_2)


# <h4>Idiotic Keras<h4>

# In[89]:


import tensorflow as tf

tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level = True, split = " ")

tokenizer.fit_on_texts(char_sequence_1)

print(tokenizer.word_counts)


# <h4>Max Jugaad<h4>

# In[91]:


from indicnlp.tokenize.indic_tokenize import trivial_tokenize_indic

tokens_indic = trivial_tokenize_indic(char_sequence_1)

tokens_indic = pd.Series(tokens_indic)

word_counts = tokens_indic.value_counts()
print(word_counts)


# In[ ]:




