# gnn_project
Project for CSE576

- To get results, run Baseline and Baseline_xml notebooks. 

- llm_predict.ipynb is code for preprocessing the dataset for LLM-as-predictor model. 

- LLMpredictor.py is code for getting LLM-as-predictor final results, and getting the additional explanation texts in text-level enhancer model. 

All other code snippets are for supplementary tasks:

- contrastive_loss: Has the contrastive loss used in baseline experiments

- contruct_adj_matrix: Constructs the adjacency matrix used by our GNNs

- get_extra_papers: Finds papers with missing xml, queries arxiv, and dowloads the additional xml files

- data_process_for_openai_emb_share.py: Prepare "Title + Abstract + Introduction" for OpenAI API. With this code, citations in the introduction section will be replaced with their titles.

- cosine_similarity_baseline_share.py: Prepare KDD submission with the cosine similarity baseline.



