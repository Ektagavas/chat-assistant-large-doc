from pypdf import PdfReader
# import numpy as np

reader = PdfReader("/Users/kaustubh/Downloads/Modi-Ki-Guarantee-Sankalp-Patra-English_2.pdf")
number_of_pages = len(reader.pages)
with open('parsed_manifesto_pg8-19.txt', 'a') as f:
    for i in range(7,19):
        page = reader.pages[i]
        text = page.extract_text()
        print(text, file=f)


# f = open("parsed_manifesto.txt", "r")
# print(f.read())

# while True:
#     val = input("Message: ") 
#     print(val) 

# try:
#   while True:
#     val = input("Message: ") 
#     print(val) 
# except KeyboardInterrupt:
#   print('')

