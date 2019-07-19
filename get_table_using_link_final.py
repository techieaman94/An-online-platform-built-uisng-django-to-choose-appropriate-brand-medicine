#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests

#MAIN INPUT

#gen_name='Paracetamol'
#gen_name='Gabapentin'
#gen_name='Tamsulosin'
#gen_name='Acarbose'

def QF(gen_name):
    title_head='Brands for '


    #url_h=
    url = 'https://www.medicineindia.org/medicine-generics/'+gen_name[0].lower()
     
    # Getting the webpage, creating a Response object.
    response = requests.get(url)
     
    # Extracting the source code of the page.
    data = response.text
     
    # Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(data, 'lxml')



    title_gn=title_head+gen_name

    # Extracting all the <a> tags into a list.
    #tags = soup.find_all('a' , {'title': 'Brands for Gabapentin'})

    tags = soup.find_all('a' , {'title': title_gn})
     
    # Extracting URLs from the attribute href in the <a> tags.
    for tag in tags:
        #print(tag.get('href'))
        u_address = tag.get('href')
        print(u_address)
     


    # In[2]:


    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    """
    Created on Tue Jan 15 10:26:29 2019

    @author: techieaman94
    """

    import requests
    import lxml.html as lh
    import pandas as pd
    import numpy as np


    # In[3]:


    #making the URL for the search

    #gen_name='gabapentin'
    #code_num = '921'
    #u_address='https://www.medicineindia.org/brands-for-generic/'


    #url=u_address+code_num+"/"+gen_name

    url='https:'+u_address

    #url='https://www.medicineindia.org/brands-for-generic/921/gabapentin'
    #url='https://www.medicineindia.org/brands-for-generic/1622/acarbose'
    #Create a handle, page, to handle the contents of the website

    page = requests.get(url)

    #print(page.text)
    #Store the contents of the website under doc

    doc = lh.fromstring(page.content)

    #print(doc)
    #Parse data that are stored between <tr>..</tr> of HTML

    tr_elements = doc.xpath('//tr')

    #print(tr_elements)


    # In[4]:


    print("\n---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+--")

    print("\nThe number of BRAND medicine available in INDIA for --",gen_name ,"-- GENERIC medicine is : " , len(tr_elements) - 1 ,"\n")
    print("__________________________________________________________________________________________\n")
    #Check the length of the first 12 rows
    #print( [ len(T) for T in tr_elements[:12] ] )
    #print(len(tr_elements[0]))

    for i in range( len(tr_elements) - 1 ) :
    	if (  (len( tr_elements[ i ] ) ) != ( len( tr_elements[ i+1 ]  ) )  ):
    		quit()

    length_of_row = len(tr_elements[0])
    #print(length_of_row)



    tr_elements = doc.xpath('//tr')
    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        #print (i,name)
        col.append((name,[]))
        

    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
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
            
            
    #print(  [len(C) for (title,C) in col] )


    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)


    # In[5]:


    df


    # In[6]:


    df["Price"]= df["Price"].str.slice(2,-3,1)
    #df["Strength"] = df["Strength"].str.slice(0,-3,1)

    df['Price']=pd.to_numeric(df['Price'])
    #df['Strength']=pd.to_numeric(df['Strength'])


    # In[7]:


    filter1 = df.Strength != ' '
    filter2 = df.Price > 0 
    filtered_df = df[ filter1 & filter2 ]
    filtered_df


    # In[8]:


    filtered_df = filtered_df.sort_values(by=['Strength'])
    filtered_df


    # In[9]:


    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df


    # In[10]:


    Strength_catagories=[]
    Strength_catagories = (filtered_df.Strength.unique())
    Strength_catagories


    # In[11]:


    for i in Strength_catagories:
        
        df_ = filtered_df[ filtered_df.Strength == i ]
        
        print("Details of medicine, with minimum price for Strength",i," is : ",'\n')
        print( df_.loc[df_['Price'].idxmin()] ,'\n' )
        
        
        mean_price = df_.mean()['Price']
        print ("Avg price is :",int(mean_price) )
        print("Details of medicine, closest to Average price for strength",i,"is : ",'\n')
        print(df_.loc[abs(df_['Price'] - mean_price ).idxmin() ],'\n')
        
        
        print("Details of medicine with maximum price for Strength",i," is : ",'\n')
        print( df_.loc[df_['Price'].idxmax()] )
        print("---+----------+----------+----------+----------+----------+----------+----------+----------+----------+---",'\n\n')
    


QF('Paracetamol')
# In[12]:


#df.groupby(['Strength']).groups


# In[13]:


#df.to_csv('med_data')

#df = pd.read_csv('med_data')

