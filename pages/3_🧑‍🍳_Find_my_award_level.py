import streamlit as st
from streamlit_extras.app_logo import add_logo
add_logo("gallery/ResizeWW.png", height=100)

from googletrans import Translator
translator = Translator()

st.header("Need help finding your award classification?", divider="rainbow")


translate_lang = st.selectbox(" :globe_with_meridians: "
                              "Currently supporting 10 languages. Choose your language: ",
                              ["English", "简体中文", "हिंदी", "العربية", "Bahasa Indonesia",
                               "नेपाली", "Português", "Español", "ภาษาไทย", "اردو ", "Tiếng Việt"])
# Default language English
target_lang = "en"

if translate_lang == "简体中文":
    target_lang = "zh-CN"
elif translate_lang == "हिंदी":
    target_lang = "hi"
elif translate_lang == "العربية":
    target_lang = "ar"
elif translate_lang == "Bahasa Indonesia":
    target_lang = "id"
elif translate_lang == "नेपाली":
    target_lang = "ne"
elif translate_lang == "Português":
    target_lang = "pt"
elif translate_lang == "Español":
    target_lang = "es"
elif translate_lang == "ภาษาไทย":
    target_lang = "th"
elif translate_lang == "اردو":
    target_lang = "ur"
elif translate_lang == "Tiếng Việt":
    target_lang = "vi"

st.subheader("First, we just need a few details from you.", divider="rainbow")

award = st.radio("Select your pay award",
                 ("Fast Food Industry Award",
                 "General Retail Industry Award",
                  "Hospitality Industry (General) Award"),
                 captions=("Covers fast food diners or take-away food shops. :red[NOT] :orange['SIT DOWN'] services like coffee shops, "
                           "cafes and bars.",
                           "Covers retailers, supermarkets, department stores and most retail stores inside a shopping centre",
                           "Covers hotels, wine bars, accomodation providers and 'restaurants connected with a hotel'. If you "
                           "are working in a :orange['STANDALONE'] restaurant, then you are :red[NOT COVERED] by this award."),
                 index=None)

if award is not None:
    st.subheader("Second, here is some info about your pay award", divider="rainbow")

    if award == "Fast Food Industry Award":
        st.markdown('''You have selected the Fast Food Industry Award. 
                    \n This award covers ''')

    elif award == "General Retail Industry Award":
        st.markdown('''You have selected the General Retail Industry Award.
                    \n This award covers workers in most retail stores.
                    \n What is a classification level?''')

        st.subheader("Classification levels below:")

        


    elif award == "Hospitality Industry (General) Award":
        st.markdown('''You have selected the Hospitality Industry (General) Award.''')

else:
    pass

