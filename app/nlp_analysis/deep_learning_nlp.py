
class EmbeddingLayer:
    def __init__(self, language):
        if language == SWEDISH:
            flair_forward_embedding = FlairEmbeddings('swedish-forward')
            flair_backward_embedding = FlairEmbeddings('swedish-backward')
            bert_embedding = BertEmbeddings('bert-base-multilingual-cased')
        else:
            flair_forward_embedding = FlairEmbeddings('swedish-forward')
            flair_backward_embedding = FlairEmbeddings('swedish-backward')
            bert_embedding = BertEmbeddings('bert-base-multilingual-cased')
