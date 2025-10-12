import torch
from transformers import DistilBertTokenizer, DistilBertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ..base_algorithm import BaseAlgorithm
import logging
import re

logger = logging.getLogger(__name__)


class DistilBERTAnalyzer(BaseAlgorithm):
    """
    INTELLIGENT DistilBERT with multi-faceted scoring and penalty system
    to ensure realistic score distribution (0.2-0.95 range)
    """
    
    def __init__(self, config: dict = None):
        super().__init__('distilbert', config)
        self.model_name = 'distilbert-base-uncased'
        self.max_length = 512
        self.tokenizer = None
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"DistilBERT device: {self.device}")
    
    def load_model(self):
        try:
            logger.info("Loading DistilBERT...")
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_name)
            self.model = DistilBertModel.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            self.is_loaded = True
            logger.info("✓ DistilBERT loaded")
        except Exception as e:
            logger.error(f"Load failed: {e}")
            raise
    
    def _clean(self, text: str) -> str:
        if not text: return ""
        text = ' '.join(text.split())
        text = re.sub(r'[•●◆▪▫■□▲►]', '', text)
        return ' '.join(text.split()[:250])  # Limit length
    
    def _embed(self, text: str) -> np.ndarray:
        """Mean-pooled embedding"""
        with torch.no_grad():
            enc = self.tokenizer(text, max_length=self.max_length, truncation=True,
                                padding=True, return_tensors='pt', return_attention_mask=True)
            ids, mask = enc['input_ids'].to(self.device), enc['attention_mask'].to(self.device)
            out = self.model(input_ids=ids, attention_mask=mask)
            emb = out.last_hidden_state
            mask_exp = mask.unsqueeze(-1).expand(emb.size()).float()
            sum_emb = torch.sum(emb * mask_exp, dim=1)
            sum_mask = torch.clamp(mask_exp.sum(dim=1), min=1e-9)
            return (sum_emb / sum_mask).cpu().numpy()
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """INTELLIGENT multi-metric scoring with penalties"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            if not resume_text or not job_description:
                return {'algorithm': self.name, 'score': 0.0, 'details': {'error': 'Empty'}}
            
            r_clean = self._clean(resume_text)
            j_clean = self._clean(job_description)
            
            # === METRIC 1: BERT Semantic Similarity (baseline) ===
            r_emb = self._embed(r_clean)
            j_emb = self._embed(j_clean)
            bert_sim = float(cosine_similarity(r_emb, j_emb)[0][0])
            
            # Normalize BERT score (it's naturally 0.85-0.99, map to 0.3-0.9)
            bert_normalized = max(0.0, min(1.0, (bert_sim - 0.85) / 0.14))  # Maps 0.85-0.99 to 0-1
            bert_normalized = 0.3 + (bert_normalized * 0.6)  # Now 0.3-0.9 range
            
            # === METRIC 2: Hard Skill Matching ===
            hard_skills = {
                'languages': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin'],
                'frontend': ['react', 'angular', 'vue', 'html', 'css', 'tailwind', 'bootstrap', 'sass', 'webpack'],
                'backend': ['node', 'express', 'django', 'flask', 'spring', 'fastapi', 'laravel', 'rails'],
                'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql', 'nosql', 'elasticsearch'],
                'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible'],
                'tools': ['git', 'jira', 'postman', 'graphql', 'rest', 'api', 'microservices']
            }
            
            r_lower = resume_text.lower()
            j_lower = job_description.lower()
            
            # Find required skills in job
            required_skills = []
            for category, skills in hard_skills.items():
                for skill in skills:
                    if skill in j_lower:
                        required_skills.append((skill, category))
            
            # Calculate match ratio
            if required_skills:
                matched_skills = sum(1 for skill, _ in required_skills if skill in r_lower)
                skill_match_ratio = matched_skills / len(required_skills)
            else:
                skill_match_ratio = 0.5  # Neutral if no specific skills
            
            # === METRIC 3: Experience Level Match ===
            r_years = self._extract_years(resume_text)
            j_years = self._extract_years(job_description)
            
            if j_years > 0:
                if r_years >= j_years:
                    exp_score = min(1.0, r_years / (j_years + 2))  # Cap at 1.0
                else:
                    exp_score = r_years / j_years * 0.8  # Penalty for insufficient exp
            else:
                exp_score = 0.7  # Neutral
            
            # === METRIC 4: Domain Relevance (word overlap) ===
            r_tokens = set(r_clean.lower().split())
            j_tokens = set(j_clean.lower().split())
            
            if j_tokens:
                common = r_tokens & j_tokens
                domain_score = len(common) / len(j_tokens)
            else:
                domain_score = 0.0
            
            # === PENALTY SYSTEM ===
            penalties = []
            
            # Penalty 1: Missing critical skills
            if skill_match_ratio < 0.3:
                penalties.append(('low_skill_match', 0.15))
            
            # Penalty 2: Experience mismatch
            if j_years > 0 and r_years < j_years * 0.5:
                penalties.append(('experience_gap', 0.12))
            
            # Penalty 3: Very low domain overlap
            if domain_score < 0.15:
                penalties.append(('low_domain_overlap', 0.10))
            
            # Penalty 4: Resume too short/generic
            if len(r_tokens) < 50:
                penalties.append(('short_resume', 0.08))
            
            total_penalty = sum(p[1] for p in penalties)
            
            # === BONUS SYSTEM ===
            bonuses = []
            
            # Bonus 1: Perfect skill match
            if skill_match_ratio >= 0.9:
                bonuses.append(('excellent_skills', 0.10))
            
            # Bonus 2: Exceeds experience requirement
            if j_years > 0 and r_years >= j_years * 1.5:
                bonuses.append(('senior_candidate', 0.08))
            
            # Bonus 3: High domain relevance
            if domain_score > 0.5:
                bonuses.append(('strong_domain', 0.05))
            
            total_bonus = sum(b[1] for b in bonuses)
            
            # === FINAL SCORE CALCULATION ===
            # Weighted combination WITHOUT transformation
            base_score = (
                bert_normalized * 0.15 +     # BERT semantic (reduced to 15%)
                skill_match_ratio * 0.45 +   # Skills MOST important
                exp_score * 0.20 +           # Experience match
                domain_score * 0.20          # Domain relevance
            )
            
            # Apply penalties and bonuses
            adjusted_score = base_score - total_penalty + total_bonus
            
            # Final bounds
            final_score = max(0.15, min(0.95, adjusted_score))  # Range: 0.15-0.95
            
            logger.info(f"DistilBERT - BERT:{bert_sim:.2f}→{bert_normalized:.2f}, Skills:{skill_match_ratio:.2f}, "
                       f"Exp:{exp_score:.2f}, Domain:{domain_score:.2f}, Penalty:{total_penalty:.2f}, "
                       f"Bonus:{total_bonus:.2f}, Final:{final_score:.2f}")
            
            return {
                'algorithm': self.name,
                'score': float(final_score),
                'details': {
                    'bert_raw': bert_sim,
                    'bert_normalized': bert_normalized,
                    'skill_match_ratio': skill_match_ratio,
                    'experience_score': exp_score,
                    'domain_score': domain_score,
                    'base_score': base_score,
                    'penalties': dict(penalties),
                    'bonuses': dict(bonuses),
                    'total_penalty': total_penalty,
                    'total_bonus': total_bonus,
                    'required_skills_count': len(required_skills),
                    'matched_skills_count': matched_skills if required_skills else 0,
                    'resume_years': r_years,
                    'job_years': j_years,
                    'model': 'distilbert-base-uncased'
                }
            }
            
        except Exception as e:
            logger.error(f"DistilBERT failed: {e}", exc_info=True)
            return {'algorithm': self.name, 'score': 0.0, 'details': {'error': str(e)}}
    
    def _extract_years(self, text: str) -> int:
        """Extract years of experience"""
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)'
        ]
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(m) for m in matches if m.isdigit()])
        return max(years) if years else 0
    
    def cleanup(self):
        try:
            if self.model:
                del self.model
                self.model = None
            if self.tokenizer:
                del self.tokenizer
                self.tokenizer = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            self.is_loaded = False
            logger.info("✓ DistilBERT cleaned")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
