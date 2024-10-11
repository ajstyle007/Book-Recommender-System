import streamlit as st
import numpy as np
import pickle

popular_df = pickle.load(open("popular_df.pkl", "rb"))

books = pickle.load(open("books.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))
pt_table = pickle.load(open("pt_table.pkl", "rb"))


# st.sidebar.header("BooK RecommendeR SysteM")
st.sidebar.markdown('<div style="text-align: center; color: #bf133b; font-size: 45px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">BooK RecommendeR SysteM</div>',
                        unsafe_allow_html=True)

paragraph_text = """<span style="font-size: 13px; color: #0a0a0a;  font-family: Comic Sans MS, monospace;">This is a Book Recommender System that features a homepage with the Top 50 highly-rated books, 
                                    along with personalized book recommendations based on your preferences. Additionally, 
                                    explore a curated selection of the best machine learning and deep learning books."""

st.sidebar.write("")
# sidebar_text = """This is a Book Recommender System that features a homepage with the Top 50 highly-rated
#                      books and a second tab for personalized book recommendations based on your preferences."""
st.sidebar.markdown(f'<div class="custom-box">{paragraph_text}</div>', unsafe_allow_html=True)
st.sidebar.write("")
st.sidebar.image("https://images.amazon.com/images/P/0151008116.01.LZZZZZZZ.jpg")
st.sidebar.image("https://images.amazon.com/images/P/0385504209.01.LZZZZZZZ.jpg")
st.sidebar.image("https://images.amazon.com/images/P/0439064872.01.LZZZZZZZ.jpg")
st.sidebar.image("https://images.amazon.com/images/P/0142001740.01.LZZZZZZZ.jpg")

custom_css = ("""
<style>

    .stTabs [data-baseweb="tab-list"] {
		gap: 10px;
    }

	.stTabs [data-baseweb="tab"] {
		height: 50px;
        width: 100px;
        white-space: pre-wrap;
		background-color: #4a4747;
		border-radius: 4px 4px 0px 0px;
		gap: 10px;
		padding-top: 10px;
		padding-bottom: 10px;
        font-weight: bold !important;  /* Make text bold */
        font-family: 'Arial', sans-serif;  /* Set font family */
        font-size: 50px;  /* Set font size */
    }

	.stTabs [aria-selected="false"] {
  		background-color: #FFFFFF;
        color: black;  /* Ensure the text color is visible when not selected */
        font-weight: bold  !important ;/* Bold for unselected tabs as well */
        font-family: 'Arial', sans-serif;  /* Set font family */
	}
              
    /* Disable hover effect for tabs */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #4a4747; /* Ensure the same color on hover */
    }

</style>""")

st.markdown(custom_css, unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Book Recommender","ML/DL Books", "Info", "Contact"])

book_name = popular_df["Book-Title"]
author = popular_df["Book-Author"]
image = popular_df["Image-URL-L"]
votes = popular_df["rating_num"]
rating = popular_df["avg_rating"]


with tab1:

    st.markdown('<div style="text-align: center; color: #121111; font-size: 40px; font-weight: bold; margin-top: 2px; margin-bottom: 20px; background-color: #faf5f5; font-family: Comic Sans MS, monospace; font-weight: bold;">Top 50 best rated Books</div>',
                        unsafe_allow_html=True)
    
    # st.markdown("<hr style='border: 1px solid #4a4747; margin-top: 5px; margin-bottom: 10px;'>", unsafe_allow_html=True)
    
    # st.header("Top 50 Books")

    col1, col2, col3 = st.columns(3)

    columns = [col1, col2, col3]

    for idx, (item1, item2, item3, item4, item5) in enumerate(zip(image, book_name, author, votes, rating)):
        with columns[idx % 3]:  # Cycle through columns
            # with st.container():
            # st.image(item1, width=200)
            st.markdown(
                f"<div style='text-align: center;'><img src='{item1}' width='200'></div>",
                unsafe_allow_html=True)
            # st.header(item2)
            st.markdown(f"<h3 style='text-align: center; color: #1375bf; font-size: 22px; '>{item2}</h3>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #d5db18; font-size: 20px; '>{item3}</h3>", unsafe_allow_html=True)
            #st.subheader(item3)
            st.markdown(
            f"<div style='text-align: center; color: #069419;'>"
            f"<p>Votes: <span style='color: red;'>{item4}</span></p>"
            f"<p>Rating: <span style='color: red;'>{np.round(item5, 1)}</span></p>"
            f"</div>",
            unsafe_allow_html=True)
            # st.write("Votes: ", item4)
            # st.write("Rating: ", np.round(item5,1))
            st.divider()


with tab2:
    # st.header("Books Recommender")
    st.markdown('<div style="text-align: center; color: #bf133b; font-size: 40px; font-weight: bold; margin-top: 2px; background-color: #faf5f5; font-family: Comic Sans MS, monospace; font-weight: bold;">Books Recommender</div>',
                        unsafe_allow_html=True)
    
    st.write("")
    
    # book_name = str(st.text_area("Enter your book name here:", key="textarea", placeholder="Book Name...", height=50))
    # st.write(type(book_name))

    def books_recommed(book_name):
        # fecth_index
        index = np.where(pt_table.index == book_name)[0][0]
        # fecth_selected_items
        selected_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x:x[1], reverse=True)[1:7]

        data = []
        for i in selected_items:
            items = []
            temp_df = books[books["Book-Title"] == pt_table.index[i[0]]]
            items.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
            items.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
            items.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-L"].values))

            data.append(items)
        # print(data)
        return data

    # book_name = str(st.text_area("Enter your book name here:", key="textarea", placeholder="Book Name...", height=50))
    book_name = st.text_input("Enter the book name", placeholder="Enter here...")
    if st.button("Check Books (double click)"):

        message_placeholder = st.empty()

        try:
            message_placeholder.markdown(f'<div style="text-align: center; color: #25c22a; font-size: 15px; font-weight: bold; background-color: #4f4b4b; padding: 3px 5px;">Recommended Books to Read</div>',
                            unsafe_allow_html=True)
            st.write("")

            thing1 = books_recommed(book_name)
            # thing1 = "1984"
            col1, col2, col3 = st.columns(3)
            
            # st.image(thing3)

            columns = [col1, col2, col3]

            # Display books in the columns
            for idx, (title, author, image_url) in enumerate(thing1):
                with columns[idx % 3]:
                    st.markdown(f"<div style='text-align: center;'><img src='{image_url}' width='200' height='300'></div>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='text-align: center; color: #1375bf; font-size: 22px;'>{title}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='text-align: center; color: #d5db18; font-size: 20px;'>{author}</h3>", unsafe_allow_html=True)
                    st.divider()
            
            
        except Exception as e:
            message_placeholder.markdown(f'<div style="text-align: center; color: #25c22a; font-size: 25px; font-weight: bold; background-color: #4f4b4b; padding: 3px 5px;">Enter correct book name</div>',
                        unsafe_allow_html=True)
            st.error(f"Error: {e}") 

            
with tab3:

    st.markdown('<div style="text-align: center; color: #BFC338; font-size: 40px; font-weight: bold; margin-top: 2px; background-color: #1C5593; font-family: Comic Sans MS, monospace; font-weight: bold;">Best ML/DL Books</div>',
                        unsafe_allow_html=True)
    # st.title("Best Books for Machine Learning")

    st.write("")

    st.markdown('<div style="text-align: center; color: #dc6a48; font-size: 25px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Best Books for Machine Learning and Deep learning</div>',
                        unsafe_allow_html=True)
    
    st.write("")

    col1, col2, col3 =  st.columns(3)

    image = "image3.jpg"
    image2 = "https://github.com/ajstyle007/books/blob/main/deep_learning_from_scratch.jpg?raw=true"
    image3 = "https://github.com/ajstyle007/books/blob/main/hands_on_machine_learning.jpg?raw=true"
    image4 = "https://github.com/ajstyle007/books/blob/main/designing_machine_learning_systems.jpg?raw=true"
    image5 = "https://github.com/ajstyle007/books/blob/main/deep_learning_for_coders.jpg?raw=true"
    image6 = "https://github.com/ajstyle007/books/blob/main/deep_learning_goodfellow.jpg?raw=true"
    image7 = "https://github.com/ajstyle007/books/blob/main/deep_learning_with_python.jpg?raw=true"
    image8 = "https://github.com/ajstyle007/books/blob/main/grokking_deep_learning.jpg?raw=true"
    image9 = "https://github.com/ajstyle007/books/blob/main/npl_with_transformers.jpg?raw=true"
    image10 = "https://github.com/ajstyle007/books/blob/main/practical_deep_learning_for_cloud.jpg?raw=true"
    image11 = "https://github.com/ajstyle007/books/blob/main/the_100_page_ml_book.jpg?raw=true"
    image12 = "https://github.com/ajstyle007/books/blob/main/elements_of_statistical_learning.jpg?raw=true"
    image13 = "https://github.com/ajstyle007/books/blob/main/intro_ml_R.jpg?raw=true"
    image14 = "https://github.com/ajstyle007/books/blob/main/mathematics.jpg?raw=true"
    image15 = "https://github.com/ajstyle007/books/blob/main/nn_deep_learning.jpg?raw=true"

    with col1:

        # st.image("image3.jpg", width=200)
        # first book
        st.markdown(f"<div style='text-align: center;'><img src='{image2}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Deep Learning from Scratch</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Seth Weidman</div>',
                        unsafe_allow_html=True)
        
        st.divider()
        # second book
        st.markdown(f"<div style='text-align: center;'><img src='{image5}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Deep Learning for Coders with fastai and PyTorch</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Jeremy Howard and Sylvain Gugger</div>',
                        unsafe_allow_html=True)

        st.divider()
        # third book
        st.markdown(f"<div style='text-align: center;'><img src='{image8}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Grokking Deep Learning</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Andrew W. Trask</div>',
                        unsafe_allow_html=True)
        
        st.divider()
        # fourth book
        st.markdown(f"<div style='text-align: center;'><img src='{image11}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">The Hundred-page Machine Learning Book</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Andriy Burkov</div>',
                        unsafe_allow_html=True)
        
        st.divider()
        # fourth book
        st.markdown(f"<div style='text-align: center;'><img src='{image14}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">mathematics</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">ncert</div>',
                        unsafe_allow_html=True)

    with col2:
        # st.image("image3.jpg", width=200)
        # 5th book
        st.markdown(f"<div style='text-align: center;'><img src='{image3}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Hand-On Machine Learning with Scikit-Learn, Keras and TensorFlow</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Aurellen Geron</div>',
                        unsafe_allow_html=True)
        
        st.divider()
        # 6th book
        st.markdown(f"<div style='text-align: center;'><img src='{image6}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Deep Learning</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Aaron Courville, Ian Goodfellow, and Yoshua Bengio</div>',
                        unsafe_allow_html=True)

        st.divider()
        # 7th book
        st.markdown(f"<div style='text-align: center;'><img src='{image9}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Natural Language Processing with Transformers</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Leandro von Werra, Lewis Tunstall, and Thomas Wolf</div>',
                        unsafe_allow_html=True)

        st.divider()    
        # 8th book
        st.markdown(f"<div style='text-align: center;'><img src='{image12}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">The Elements of Statistical Learning</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Jerome H. Friedman, Robert Tibshirani, and Trevor Hastie</div>',
                        unsafe_allow_html=True)

    with col3:
        # st.image("image3.jpg", width=200)
        # 9th book
        st.markdown(f"<div style='text-align: center;'><img src='{image4}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Designing Machine Learning Systems</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338 ; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Chip Huyen</div>',
                        unsafe_allow_html=True)
        
        st.divider()
        # 10th book
        st.markdown(f"<div style='text-align: center;'><img src='{image7}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Deep Learning with Python</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338 ; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">François Chollet</div>',
                        unsafe_allow_html=True)
        
        st.divider()
        # 11th book
        st.markdown(f"<div style='text-align: center;'><img src='{image10}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Practical Deep Learning for Cloud, Mobile, & Edge</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338 ; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Anirudh Koul, Meher Kasam, and Siddha Ganju</div>',
                        unsafe_allow_html=True)
        
        st.divider()
        # 12th book
        st.markdown(f"<div style='text-align: center;'><img src='{image13}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">An Introduction to Statistical Learning</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338 ; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Gareth M. James, Trevor Hastie, Daniela Witten, & Robert Tibshirani</div>',
                        unsafe_allow_html=True)
        
        st.divider()
        # fourth book
        st.markdown(f"<div style='text-align: center;'><img src='{image15}' width='200'></div>",unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #38c392; font-size: 15px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Neural Network and Deep Learning</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #7ec338; font-size: 12px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Michael Nielsen</div>',
                        unsafe_allow_html=True)



with tab4:

    st.markdown('<div style="text-align: center; color: #7155cf; font-size: 40px; font-weight: bold; margin-top: 2px; background-color: #c9e041; font-family: Comic Sans MS, monospace; font-weight: bold;">why you should read books</div>',
                        unsafe_allow_html=True)
    # st.subheader("why you should read books")

    st.write("")
    st.write("")
    st.write("")

    st.markdown("""
            <style>
            .custom-box {
                background-color: #808080; /* Light gray background */
                border: 2px solid #00000; /* Blue border */
                border-radius: 10px; /* Rounded corners */
                padding: 20px; /* Padding inside the box */
                font-family: 'Courier New', Courier, monospace; /* Change to a catchy font */
                box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
                color: #ECEAE2; 
            }
            </style>""", unsafe_allow_html=True)

    text1 = """
            Reading books is one of the most valuable habits you can develop. Books broaden your perspective, offering a window into 
            different cultures, ideas, and eras. They stimulate your mind, improve focus, and build critical thinking skills. 
            Reading regularly enhances your vocabulary, strengthens your ability to articulate thoughts, and fuels creativity. 
            It can reduce stress by providing a healthy escape from daily pressures and help you understand yourself and others more deeply."""
    

    # Adjusted paragraph text
    text2 = """Books also offer lifelong learning opportunities, allowing you to continuously grow intellectually and emotionally.
                Whether fiction or non-fiction, every book has the potential to shape your outlook and inspire new ways of thinking."""

    # Display the paragraph in a custom box
    st.markdown(f'<div class="custom-box">{text1}</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown(f'<div class="custom-box">{text2}</div>', unsafe_allow_html=True)


with tab5:

    st.markdown('<div style="text-align: center; color: #c3388b; font-size: 40px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Contact Me</div>',
                        unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3,col4 = st.columns(4)

    with col2:
        
        st.write("")
        st.write("")
        st.write("")

        email = "kumarajaypaonta.@gmail.com"
        email_image = "https://github.com/ajstyle007/images/blob/main/email.png?raw=true"

        linkedin = "https://www.linkedin.com/in/ajay-kumar-72ba861b8/"
        linkedin_image = "https://github.com/ajstyle007/images/blob/main/linkedin.png?raw=true"

        medium = "https://medium.com/@kumarajaypaonta"
        medium_image = "https://github.com/ajstyle007/images/blob/main/medium.jpg?raw=true"

        st.markdown(f'''
            <a href="mailto:{email}" style="text-decoration: none;">
            <img src="{email_image}" alt="Email" style="width:50px;height:50px;text-align: center;">
            </a>''', unsafe_allow_html=True)

        st.write("")

        st.markdown(f'''
                    <a href = "{linkedin}" target = "_blank">
                    <img src = "{linkedin_image}" alt = "LinkedIn" style = "width : 50px;"> 
                    </a>    
        ''', unsafe_allow_html=True)
    
    with col3:

        # st.image("image3.jpg", width=150)
        # st.markdown('<div style="text-align: center; color: #7ec338 ; font-size: 17px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Medium Blogs</div>',
        #                 unsafe_allow_html=True)
        st.write("")
        st.markdown(f'''<div style="text-align: center;">
        <a href="{medium}" target="_blank" style="text-decoration: none;">
            <img src="{medium_image}" alt="linkedin" style="width:150px;height:150px;text-align: center;">
            <p style="text-align:center; color: #7ec338 ; font-size: 17px; font-weight: bold; font-family: Comic Sans MS, monospace; font-weight: bold;">Medium Blogs</p>
        </a>        
        </div>''', unsafe_allow_html=True)
        

    # st.subheader("Email")
    # st.write("kumarajaypaonta.@gmail.com")
    # st.subheader("LinkedIn")
    # st.write("https://www.linkedin.com/in/ajay-kumar-72ba861b8/")


    
