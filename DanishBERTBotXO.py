from transformers import AutoTokenizer, AutoModelForPreTraining, AutoModelForMaskedLM, pipeline
from utility_fcs import idx_occ_pron, remove_sq_br, load_texts
from predict_mask import predict_masked
from group_pronouns import group_pronouns
from model_evaluation import evaluate_model
import torch, os, spacy, random 

#set seed 
# whnat is up
torch.manual_seed(3)

#define model, pipeline and tokenizer
model = "Maltehb/danish-bert-botxo"
nlp =  pipeline(task = "fill-mask", model = model) 
tokenizer = spacy.load("da_core_news_lg") 

#load data set
anti_lines, pro_lines = [], []
path = os.path.join('data')
anti_lines = load_texts(path,'anti','both')
pro_lines = load_texts(path,'pro', 'both')

# flatten lists
anti_lines = [sentence for sublist in anti_lines for sentence in sublist]
pro_lines = [sentence for sublist in pro_lines for sentence in sublist]

# randomize data 
random.shuffle(anti_lines)
random.shuffle(pro_lines)

#mask and predict pronoun 
anti_labels, anti_preds = predict_masked(lines = anti_lines, nlp = nlp, tokenizer = tokenizer)
pro_labels, pro_preds = predict_masked(lines = pro_lines, nlp = nlp, tokenizer = tokenizer)

#group pronouns
anti_labels, anti_preds = group_pronouns(anti_labels),group_pronouns(anti_preds) 
pro_labels, pro_preds = group_pronouns(pro_labels),group_pronouns(pro_preds) 

#evaluate performance
evaluate_model(anti_labels, anti_preds, filename = 'results/anti_results_mlm')
evaluate_model(pro_labels, pro_preds, filename = 'results/pro_results_mlm')