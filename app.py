import streamlit as st
import streamlit.components.v1 as stc

# File Processing Pkgs
import pandas as pd
from PIL import Image 
from PyPDF2 import PdfFileReader
import pdfplumber
import os as os


def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text

def read_pdf_with_pdfplumber(file):
	with pdfplumber.open(file) as pdf:
	    page = pdf.pages[0]
	    return page.extract_text()

# import fitz  # this is pymupdf

# def read_pdf_with_fitz(file):
# 	with fitz.open(file) as doc:
# 		text = ""
# 		for page in doc:
# 			text += page.getText()
# 		return text 

# Fxn
@st.cache_resource
def load_image(image_file):
	img = Image.open(image_file)
	return img 



def main():
	st.title("UITC File Upload")

	menu = ["Images","Dataset","DocumentFiles","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Images":
		st.subheader("Images")
		image_file = st.file_uploader("Upload Image",type=['png','jpeg','jpg'])
		if image_file is not None:
		
			# To See Details
			# st.write(type(image_file))
			# st.write(dir(image_file))
			file_details = {"Filename":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
			st.write(file_details)

			img = load_image(image_file)
			st.image(img,width=250)

			with open(os.path.join("Images", image_file.name),"wb") as f:
				f.write(image_file.getbuffer())

			st.success("Images Saved")


	elif choice == "Dataset":
		st.subheader("Dataset")
		data_file = st.file_uploader("Upload CSV",type=['csv'])
		if st.button("Process"):
			if data_file is not None:
				file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
				st.write(file_details)

				df = pd.read_csv(data_file, encoding = 'unicode escape')
				st.dataframe(df)
			
			with open(os.path.join("Dataset", data_file.name),"wb") as f:
				f.write(data_file.getbuffer())

			st.success("Dataset Saved")			

	elif choice == "DocumentFiles":
		st.subheader("DocumentFiles")
		docx_file = st.file_uploader("Upload File",type=['txt','docx','pdf'])
		if st.button("Process"):
			if docx_file is not None:
				file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
				st.write(file_details)
				# Check File Type
				if docx_file.type == "text/plain":
					# raw_text = docx_file.read() # read as bytes
					# st.write(raw_text)
					# st.text(raw_text) # fails
					st.text(str(docx_file.read(),"utf-8")) # empty
					raw_text = str(docx_file.read(),"utf-8") # works with st.text and st.write,used for futher processing
					# st.text(raw_text) # Works
					st.write(raw_text) # works
				elif docx_file.type == "application/pdf":
					# raw_text = read_pdf(docx_file)
					# st.write(raw_text)
					try:
						with pdfplumber.open(docx_file) as pdf:
						    page = pdf.pages[0]
						    st.write(page.extract_text())
					except:
						st.write("None")
					    
					
				elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
				# Use the right file processor ( Docx,Docx2Text,etc)
					raw_text = docx2txt.process(docx_file) # Parse in the uploadFile Class directory
					st.write(raw_text)

				with open(os.path.join("Documentations", docx_file.name),"wb") as f:
					f.write(docx_file.getbuffer())

				st.success("Document Saved")

	else:
		st.subheader("About")
		st.info("Built with Streamlit")


if __name__ == '__main__':
	main()