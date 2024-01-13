import PyPDF2
import os
import re
import pandas as pd

def parse_pdf(file_path):
    alltext = []
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            alltext.append(text)

    return alltext

def process_pdfs_in_directory(directory_path):
    data = []
    titles = []  #Store the titles of the PDF files for level 1 index
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            pdf_texts = parse_pdf(file_path)

            
            cleaned_texts = [remove_unusual_punctuation(text) for text in pdf_texts] #Clean and concatenate text for each page
            cleaned_text = ' '.join(cleaned_texts)

            data.extend(cleaned_texts)  #Extend the data list with individual pages
            titles.extend([filename] * len(pdf_texts))  #Extend the titles list

    return titles, data

def remove_unusual_punctuation(text):
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?]', ' ', text)
    cleaned_text = ' '.join(cleaned_text.split()).lower()
    return cleaned_text

if __name__ == "__main__":
    
    pdf_directory = "/Project Pribadi/parser_pdf" #Directory containing the PDF files
    titles, extracted = process_pdfs_in_directory(pdf_directory)

    df = pd.DataFrame(extracted, index=pd.MultiIndex.from_arrays([titles, range(1, len(extracted) + 1)], names=['Title', 'Page']))

    df = df.rename(columns={0: 'Text'})

    path = "parser_pdf/data.csv" 
    df.to_csv(path, index=False) #Output CSV files