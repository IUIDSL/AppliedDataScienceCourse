from nltk import PorterStemmer, WordNetLemmatizer
from stopwords import STOPWORDS

def normalize(x,style="PorterStemmer"):
  """This normalizer will remove stopwords and normalize text"""
  x = [t.lower() for t in x.split() if t not in STOPWORDS]
  if style == "PorterStemmer":
    return " ".join(list(map(PorterStemmer().stem,x)))
  elif style == "Lemma":
    try: return " ".join(list(map(WordNetLemmatizer.lemmatize,x)))
    except: return " ".join(x)
  elif style == "CharGram":
    cs = " ".join(x)
    return " ".join([cs[i:i+3] for i in range(0,len(cs),3)])
  else:
    return " ".join(x)
