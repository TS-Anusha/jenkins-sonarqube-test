import os
import openai
from dotenv import load_dotenv

load_dotenv()
""" use markdown to split chapterwise, take individual chapter-divide into chunks, get summary-append it to a list and provide it to get concise summary"""
from langchain.text_splitter import MarkdownHeaderTextSplitter
import textwrap
openai_api_key=os.getenv('OPENAI_API_KEY')
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

chain2 = load_summarize_chain(llm=llm, chain_type='map_reduce')

current_directory = os.path.dirname(os.path.abspath(__file__))
relative_filepath = "The_Red_Year__A_Story_of_the_Indian_Mutiny.txt"
filepath = os.path.join(current_directory, relative_filepath)

with open(filepath,'r',encoding='utf-8') as file:
    text = file.read()


num_tokens = llm.get_num_tokens(text)

print (f"The num of tokens in the file is: {num_tokens}")

text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"],chunk_size=5000, chunk_overlap=350)

docs = text_splitter.create_documents([text])
##method 3
headers_to_split_on = [
    ("The Project Gutenberg eBook of The Red Year: A Story of the Indian Mutiny", "book_intro"),
    ("CONTENTS", "content_header"),
    ("CHAPTER I", "chapter1"),
    ("CHAPTER II", "chapter2"),
     ("CHAPTER III", "chapter3"), ("CHAPTER IV", "chapter4"),
     ("CHAPTER V", "chapter5"),
       ("CHAPTER VI", "chapter6"),
     ("CHAPTER VII", "chapter7"),
    ("CHAPTER VIII", "chapter8"),("CHAPTER IX", "chapter9"),("CHAPTER X", "chapter10"),
    ("CHAPTER XI", "chapter11"),    ("CHAPTER XII", "chapter12"),
     ("CHAPTER XIII", "chapter13"),   ("CHAPTER XIV", "chapter14"), ("CHAPTER XV", "chapter15"), 
   ("CHAPTER XVI", "chapter16"),    ("CHAPTER XVII", "chapter17"),
    ("BOOKS ON NATURE STUDY BY", "rest_of_content"),   
]
md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers = False)
md_splits = md_splitter.split_text(text)

# Char-level splits
from langchain.text_splitter import RecursiveCharacterTextSplitter

chunk_size = 5000
chunk_overlap = 350
chapter_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)


chapter_summary=[]
for i in range(len(md_splits)):
    if i>18 and i<len(md_splits)-1:
        chapter_split=chapter_splitter.split_documents([md_splits[i]])
        chapter_output = chain2.run(chapter_split)
        chapter_summary.append(chapter_output)
    

chaptersummarypath=os.path.join(current_directory,"summary_Indian_mutiny.txt")
with open(chaptersummarypath, 'w',encoding='utf-8') as file:
    for summary in chapter_summary:
        file.write(summary + '\n')


print(len(chapter_summary))


with open(chaptersummarypath, 'r',encoding='utf-8') as file:
    summary_content=file.read()
# print("chapter summaries:", summary_content)

""" Summarizing list of chapter_wise summaries"""
chain3 = load_summarize_chain(llm=llm, chain_type='map_reduce', verbose=True)

from langchain.text_splitter import RecursiveCharacterTextSplitter

chunk_size = 5000
chunk_overlap = 350
summary_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)
summary_splitting=summary_splitter.split_text(summary_content)
summary_splits=summary_splitter.create_documents(summary_splitting)


final_summary=chain3.run(summary_splits)

final_list=final_summary.split()
print("length of the summary:", len(final_list))
print("summary of chapterwise summary:", final_summary)