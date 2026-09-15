from flashrank import Ranker, RerankRequest

from query_rewrite import rewrite_query

ranker = Ranker()

def dense_rerank(rewritten_query:str,chunks_retrieved:str):

    passages = [{"id": i, "text": chunk} for i, chunk in enumerate(chunks_retrieved)]
        
    request = RerankRequest(query=rewritten_query, passages=passages)
    reranked_results = ranker.rerank(request)

    #Extract the newly sorted text strings (taking the top 5 best ones)
    final_chunks = [res["text"] for res in reranked_results][:5]

    print("chunks reranked")

    return final_chunks