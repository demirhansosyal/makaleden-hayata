"""LinkedIn-only source screening and literal evidence validation."""
import html
import re
import unicodedata

TOPICS = {
 'nutrition': ['dietary protein', 'dietary fibre', 'dietary fiber', 'whole grain', 'fruit and vegetable', 'Mediterranean diet', 'breakfast', 'meal timing', 'carbohydrate intake', 'food intake'],
 'sport': ['resistance training', 'strength training', 'aerobic exercise', 'endurance training', 'exercise training', 'physical activity', 'walking', 'sedentary breaks', 'sports nutrition', 'hydration'],
 'health': ['sleep regularity', 'sleep duration', 'sleep quality', 'sleep extension', 'sitting breaks', 'breaking up prolonged sitting'],
}
# A relevant word in a clinical test or drug trial must never be sufficient.
EXCLUDED = re.compile(r'\b(tirzepatid\w*|semaglutid\w*|liraglutid\w*|glp.?1|sglt.?2|pharmac\w*|drug\w*|medication\w*|placebo tablet|chemotherap\w*|antidepressant\w*|antipsychotic\w*|dialysis|renal|kidney|urinar\w*|albuminur\w*|proteinur\w*|dipstick|biomarker\w*|diagnostic\w*|screening|staging|surgery|surgical|cancer treatment|carcinoma|covid\w*|sars.cov\w*|animal model|mice|rats|murine)\b', re.I)
RELEVANT = re.compile(r'\b(dietary (?:protein|fibre|fiber)|whole.grain\w*|fruit\w*|vegetable\w*|mediterranean diet|nutrition\w*|food\w*|meal\w*|breakfast|carbohydrate\w*|exercise\w*|physical activit\w*|walking|step count|daily steps|resistance train\w*|strength train\w*|sedentary|sitting|sleep\w*|circadian|hydrat\w*|dehydrat\w*|endurance|sports? performance)\b', re.I)

def clean(text):
 # Remove HTML tags, never a numeric '< ... >' comparison in a plain abstract.
 return ' '.join(html.unescape(re.sub(r'</?[A-Za-z][^>]*>', ' ', text or '')).split())

def norm(text):
 text=unicodedata.normalize('NFKC',clean(text)).translate(str.maketrans({'−':'-','–':'-','—':'-','’':"'"}))
 return ' '.join(text.casefold().split())

def source_allowed(article):
 title=clean(article.get('title','')); abstract=clean(article.get('abstractText',''))
 quantitative=bool(re.search(r'confidence interval|credible interval|95\s*%|\d+(?:[.,]\d+)?\s*%|\b(?:g|es|smd)\s*[+=:]?\s*[-−]?\d',abstract,re.I))
 return bool(quantitative and article.get('id') and abstract and RELEVANT.search(title) and not EXCLUDED.search(title+' '+abstract) and article.get('isRetracted')!='Y')

def evidence_spans(abstract):
 # IDs point to source-owned snippets; the model cannot invent a quotation.
 words=clean(abstract).split()
 return {str(i//15):' '.join(words[i:i+20]) for i in range(0,len(words),15)}

def validate_content(content,spans):
 limits={'text':2700,'title':65,'stat':25,'stat_label':100,'finding':160,'interpretation':140,'limitation':160}
 for key,limit in limits.items():
  value=content.get(key)
  if not isinstance(value,str) or not value.strip() or len(value)>limit:raise ValueError('Invalid '+key)
 if not 140<=len(content['text'].split())<=230:raise ValueError('Text must contain 140-230 words')
 if not re.search(r'\d',content['stat']):raise ValueError('Card needs a source-supported numeric finding')
 if not 2<=len(re.findall(r'#[\w]+',content['text']))<=3:raise ValueError('Hashtag count')
 if '#MakaledenHayata' not in content['text']:raise ValueError('Missing series tag')
 if re.search(r'eyüpspor|eyupspor|demirhan eren|çalışmalarımız|pratiğimiz|kliniğimiz|hastalarım|danışanlarım|tecrübem|deneyimim|takip ediyoruz|sahada gözlem',content['text'],re.I):raise ValueError('Unverified personal or employer practice')
 if re.search(r'katlanarak|kesin sonuç sağlar|garanti eder|garanti ediyor|tirzepatid|semaglutid|ilaç dozu',content['text'],re.I):raise ValueError('Overstatement or drug content')
 ids=content.get('evidence_ids')
 if not isinstance(ids,list) or not 1<=len(ids)<=8 or any(type(i) is not int or str(i) not in spans for i in ids):raise ValueError('Invalid evidence IDs')
 return [spans[str(i)] for i in ids]
