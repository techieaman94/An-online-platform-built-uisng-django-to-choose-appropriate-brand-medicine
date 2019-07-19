from django.shortcuts import render, get_object_or_404
from django.shortcuts import Http404
from django.http import HttpResponse

from .forms import InputForm_g2b , InputForm_b2g


from bs4 import BeautifulSoup
import requests
import requests
import lxml.html as lh
import pandas as pd
import numpy as np

g_DF = pd.DataFrame()
strength_options = []


def home_view(request):

	return render(request,"pages/home.html",{})



def gen_to_brand_view(request):

	form = InputForm_g2b(request.POST or None)
	if form.is_valid():
		form.save()
		form = InputForm_g2b()
	context={
	'form': form
	}

	return render(request,"pages/g2bform.html",context)


def brand_to_gen_view(request):

	form = InputForm_b2g(request.POST or None)
	if form.is_valid():
		form.save()
		form = InputForm_b2g()
	context={
	'form': form
	}

	return render(request,"pages/b2gform.html",context)




def brand_to_generic_result_view(request):

	def Find_Generic_Name(brand_name):

		url = 'https://www.medicineindia.org/medicine-brands/'+brand_name[0].lower()
		# Getting the webpage, creating a Response object.

		response = requests.get(url)
		 
		# Extracting the source code of the page.
		data = response.text

		# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
		soup = BeautifulSoup(data, 'lxml')

		title_bn = brand_name.upper()

		# Extracting all the <a> tags into a list.
		#tags = soup.find_all('a' , {'title': 'Brands for Gabapentin'})
		tags = soup.find_all('a')

		#print(tags)
		u_address2 = ""
		found = 1
		# Extracting URLs from the attribute href in the <a> tags.
		for tag in tags:
		    if ( tag.get_text() == title_bn ):
		        u_address2 = tag.get('href')
		        break

		if u_address2 == "":

			return "Not found"

			

		url2='https:'+u_address2

		#Create a handle, page, to handle the contents of the website
		page = requests.get(url2)

		data2 = page.text

		new_title = 'View Alternatives/Replacements For '+title_bn
		# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.

		soup2 = BeautifulSoup(data2, 'lxml')

		tags_a = soup2.find_all('a')

		for tag in tags_a:
		    
		    if ( tag.get_text() == ( new_title ) ):
		        u_address = tag.get('href')
		        gen_name_2 =  u_address[(u_address.rfind('/'))+1:] 
		        return gen_name_2
		        break


	if (request.method == 'GET'  ):
		global brand_name
		brand_name=request.GET['Name_of_Brand_Medicine']

		brand_name = brand_name.upper()

		generic_name_found = Find_Generic_Name(brand_name)

		if generic_name_found == "Not found":
			return render(request,"pages/error.html",{}) 


		context = {
		'brand_name'         : brand_name, 
		'generic_name'		 : generic_name_found
		}

	return render (request,"pages/b2g_result.html",context)





def results_strength_view(request):

	def Find_strength_options(gen_name):	    

	    title_head='Brands for '

	 
	    url = 'https://www.medicineindia.org/medicine-generics/'+gen_name[0].lower()
	    # Getting the webpage, creating a Response object.
	    response = requests.get(url)
	    # Extracting the source code of the page.
	    data = response.text

	    # Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
	    soup = BeautifulSoup(data, 'lxml')



	    title_gn=title_head+gen_name
	    # Extracting all the <a> tags into a list.

	    tags = soup.find_all('a' , {'title': title_gn})

	    u_address = ""

	    for tag in tags:
	    	u_address = tag.get('href')	  

	    if u_address == "":
	    	return "Not found"   

	    url='https:'+u_address

	    page = requests.get(url)

	    #Store the contents of the website under doc

	    doc = lh.fromstring(page.content)

	    #Parse data that are stored between <tr>..</tr> of HTML

	    tr_elements = doc.xpath('//tr')

	    for i in range( len(tr_elements) - 1 ) :
	    	if (  (len( tr_elements[ i ] ) ) != ( len( tr_elements[ i+1 ]  ) )  ):
	    		quit()

	    length_of_row = len(tr_elements[0])

	    tr_elements = doc.xpath('//tr')
	    #Create empty list
	    col=[]
	    i=0
	    #For each row, store each first element (header) and an empty list
	    for t in tr_elements[0]:
	        i+=1
	        name=t.text_content()
	        col.append((name,[]))
	        

	    #Since out first row is the header, data is stored on the second row onwards
	    for j in range(1,len(tr_elements)):

	        T=tr_elements[j]
	        
	        #If row is not of size 5, the //tr data is not from our table 
	        if len(T) != length_of_row :
	            break
	        
	        #i is the index of our column
	        i=0
	        
	        #Iterate through each element of the row
	        for t in T.iterchildren():
	            data=t.text_content() 
	            #Check if row is empty
	            if i>0:
	            #Convert any numerical value to integers
	                try:
	                    data=int(data)
	                except:
	                    pass
	            #Append the data to the empty list of the i'th column
	            col[i][1].append(data)
	            #Increment i for the next column
	            i+=1

	    Dict={title:column for (title,column) in col}
	    df=pd.DataFrame(Dict)

	    df["Price"]= df["Price"].str.slice(2,-3,1)

	    df['Price']=pd.to_numeric(df['Price'])

	    filter1 = df.Strength != ' '
	    filter2 = df.Price > 0 
	    filtered_df = df[ filter1 & filter2 ]

	    filtered_df = filtered_df.sort_values(by=['Strength'])

	    filtered_df = filtered_df.reset_index(drop=True)

	    Strength_catagories=[]
	    Strength_catagories = (filtered_df.Strength.unique())


	    for i in Strength_catagories:
	        
	        df_ = filtered_df[ filtered_df.Strength == i ]	        
	        mean_price = df_.mean()['Price']
	        return filtered_df

	if (request.method == 'GET'  ):
		global gen_name
		gen_name=request.GET['Name_of_Generic_Medicine']

		gen_name = gen_name[0].upper()+gen_name[1:].lower()

		df = Find_strength_options(gen_name)

		if type(df) == str and df == "Not found":
			return render(request,"pages/error.html",{}) 



		global g_DF
		g_DF = df

		global strength_options
		strength_options = df.Strength.unique()

		context = {
		'gen_name'         : gen_name , 
		'df'               : df ,
		'strength_options' : strength_options
		}

		return render(request,"pages/options_available.html",context)



def results_price_view(request):
	if (request.method == 'GET'):

		strength_dict={}

		for i in range (1, len(strength_options)+1):
			strength_dict[i]=strength_options[i-1]

		strength_ = request.GET['strength']
		strength_ = strength_dict[int(strength_)]

		global g_DF

		df= g_DF
		g_DF = g_DF [ g_DF.Strength == strength_ ]
		g_DF = g_DF.sort_values(by=['Price'])

		info_price= pd.DataFrame()

		info_price = info_price.append( g_DF.loc[g_DF['Price'].idxmin()]  )

		mean_price = g_DF.mean()['Price']

		info_price = info_price.append( g_DF.loc[abs(g_DF['Price'] - mean_price ).idxmin() ] )
		info_price = info_price.append( g_DF.loc[g_DF['Price'].idxmax()]  )

		context={
		'gen_name' : gen_name,
		'strength' : strength_,

		'df': g_DF.to_html(),

		'info_price' : info_price.to_html()
		}
		

		return render(request,"pages/price_available.html",context)
