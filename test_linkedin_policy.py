import copy,json,unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
import linkedin
import linkedin_policy as p
class PolicyTests(unittest.TestCase):
 def test_numeric_comparisons_survive_html(self):
  self.assertEqual(p.clean('<h4>Results</h4> P < 0.01 and loss > 2%.'),'Results P < 0.01 and loss > 2%.')
 def test_reviewed_sources(self):
  for pmid,source in json.loads(Path('linkedin_sources.json').read_text()).items():self.assertTrue(p.source_allowed(source),pmid)
 def test_clinical_false_positives(self):
  for title in ['Tirzepatide for sleep apnea','Urinary protein and albuminuria','Diet and kidney biomarkers','Exercise and pharmacological treatment']:
   self.assertFalse(p.source_allowed(dict(id='1',title=title,abstractText='A clinical trial.')))
 def test_filter_used_before_limit(self):
  articles=[dict(id=str(i),title='Resistance training in healthy adults',abstractText='A randomized trial.') for i in range(35)]
  class R:
   def json(self):return {'resultList':{'result':copy.deepcopy(articles)}}
  with patch.object(linkedin.a,'request',return_value=R()):found=linkedin.source_candidates(datetime(2026,11,9,18,tzinfo=linkedin.a.TZ),{str(i) for i in range(20)})
  self.assertTrue(found);self.assertTrue(all(int(a['id'])>=20 for a in found))
 def test_invalid_evidence(self):
  c=json.loads(Path('linkedin_reviewed.json').read_text())[-1];c['evidence_ids']=[9999]
  with self.assertRaisesRegex(ValueError,'evidence'):p.validate_content(c,{'0':'sample'})
 def test_no_past_or_duplicate(self):
  now=datetime(2026,11,9,14,tzinfo=linkedin.a.TZ);first=linkedin.due_date(now,set());self.assertEqual((first.day,first.hour),(9,18))
  second=linkedin.due_date(now,{first.isoformat(timespec='minutes')});self.assertEqual((second.day,second.hour),(10,9))
 def test_format_repair_and_semantic_rejection(self):
  article=json.loads(Path('linkedin_sources.json').read_text())['29933347'];c=json.loads(Path('linkedin_reviewed.json').read_text())[-1]
  c['text']=c['text'].split('\n\nMakale:')[0];c.update(skip=False,evidence_ids=[0]);bad=copy.deepcopy(c);bad['title']='x'*66
  with patch.object(linkedin.a,'gemini',side_effect=[copy.deepcopy(bad),copy.deepcopy(c),{'approved':True}]):self.assertIn('pubmed.ncbi.nlm.nih.gov/29933347/',linkedin.create(article,[])['text'])
  with patch.object(linkedin.a,'gemini',side_effect=[c,{'approved':False}]):
   with self.assertRaisesRegex(ValueError,'fact check'):linkedin.create(article,[])
if __name__=='__main__':unittest.main()
