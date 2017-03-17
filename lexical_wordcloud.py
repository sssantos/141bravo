
# coding: utf-8

# In[ ]:

lexical_no_stop = lexical_words_in_songs_no_top
lex_df = final_data
lex_df["Lexical"] = lexical_no_stop

def word_cloud_time(df, beginYear, endYear):
    # get range of entries
    temp = df[df["Year"] >= beginYear]
    lex_list = temp[temp["Year"] <= 1969]["Lexical"]
    
    #lex_list = df[(df["Year"] >= beginYear) and (df["Year"] <= endYear)]
    # get the lexical
    entries = reduce(lambda x, y: x + y, lex_list, [])
    long_string = " ".join(entries)
    
    #print long_string
    
     GENERATE WORD CLOUD
    wc.generate(long_string)

    # COLORING
    def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(50, 0%%, %d%%)" % random.randint(10, 50)

    # PLOTTING
    plt.figure(figsize=(20,10))
    plt.imshow(wc.recolor(color_func = grey_color_func, random_state=3))
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    
    
word_cloud_time(lex_df, 1950, 1959)    
word_cloud_time(lex_df, 1960, 1969)
word_cloud_time(lex_df, 1970, 1979)
word_cloud_time(lex_df, 1980, 1989)
word_cloud_time(lex_df, 1990, 1999)
word_cloud_time(lex_df, 2000, 2009)
word_cloud_time(lex_df, 2010, 2019)

