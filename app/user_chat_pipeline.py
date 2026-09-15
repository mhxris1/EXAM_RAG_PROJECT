
import os
import time

from ambiguity_check import is_ambiguous 
from chat import chat_response
from database import save_chat_message
from hyDe import hyDe
from query_rewrite import rewrite_query
from reranker import dense_rerank
from search import dense_search


def chat(chat_id):


    prompt = input("")
    save_chat_message(chat_id,"user",prompt)        
    rewritten_query=rewrite_query(chat_id,prompt)
    ambiguity=is_ambiguous(rewritten_query)

    if ambiguity.is_ambiguous:
        print("query it ambiguous")
        question = ambiguity.clarifying_question
        save_chat_message(chat_id,"system",question)
        return {
            "response": question,
            "requires_clarification": True,
            "chat_id": chat_id
        }

    else:
        search = hyDe(rewritten_query)
        chunks_retrieved=dense_search(search)
        reranked_chunks=dense_rerank(rewritten_query,chunks_retrieved)
        response=chat_response(rewritten_query,reranked_chunks)
        save_chat_message(chat_id,"system",response)
        return {
            "response": response,
            "requires_clarification": False,
            "chat_id": chat_id,
        }