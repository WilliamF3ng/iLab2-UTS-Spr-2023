import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from streamlit_extras.app_logo import add_logo
add_logo("gallery/ResizeWW.png", height=100)

from PIL import Image

from googletrans import Translator
translator = Translator()

st.header(":thinking_face: Need help finding your award level?", divider="rainbow")


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

st.subheader(translator.translate("First, we just need a few details from you.", dest=target_lang).text, divider="rainbow")

award = st.radio(translator.translate("Select your pay award", dest=target_lang).text,
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
    st.subheader(translator.translate("Second, here is some info about your pay award",dest=target_lang).text, divider="rainbow")

    if award == "Fast Food Industry Award":
        fastfood = Image.open("gallery/Fast Food.jpg")
        st.image(fastfood, width=400)

        st.subheader(translator.translate("You have selected the Fast Food Industry Award. Let's understand your work rights!",dest=target_lang).text)

        with st.expander(translator.translate("What is the Fast Food Industry Award?", dest=target_lang).text):
            st.write(translator.translate('''The Fast Food Award is a special set of rules that apply to businesses where you can quickly order food and take it away to eat somewhere else.
                                          This includes places like food courts and shops where fast food is made and sold.''',dest=target_lang).text)
        with st.expander(translator.translate("Who does it cover?",dest=target_lang).text):
            st.write(translator.translate('''The Fast Food Award covers employees who:
                                          \n - Take orders, cook, and sell fast food: If you work at the counter, in the kitchen, or at the cash register, these rules apply to you.
                                          \n - Baristas: If you make coffee in fast food shops, you are protected by these rules.
                                          \n - Delivery Drivers: If your job involves delivering food, these rules apply to you.
                                          \n - Supervisors: If you supervise other workers in the fast food industry, you are covered.
                                          \n - Managers: If you are in charge of a fast food or take-away shop, these rules protect you.
                                          \n - Temporary Workers: If you work through a temp agency and are placed in a fast food job, these rules also apply.''',dest=target_lang).text)

        with st.expander(translator.translate("What does it cover?",dest=target_lang).text):
            st.write(translator.translate('''The Fast Food Award covers all the meals, snacks, and drinks that are meant to be eaten away from the place where you buy them.
                                            It also includes food that is made by one business but delivered by another.''',dest=target_lang).text)

        with st.expander(translator.translate("What doesn't it cover?",dest=target_lang).text):
            st.write(translator.translate('''The Fast Food Award doesn’t apply to places like cafes, restaurants, or bars where you can sit and eat what you order. 
                                          \n If you are already protected by other work rules like the Restaurant, Hospitality, or Retail Awards, the Fast Food Award doesn’t apply to you either. 
                                          And it doesn’t cover delivery workers who are not directly employed by a fast food business.
                                          \n Remember, these rules are here to protect you and make sure you are treated fairly at work. If you have any questions or concerns, don’t hesitate to ask for help. Knowing your rights is the first step to a fair and respectful workplace.''',dest=target_lang).text)
                    
        with st.expander(translator.translate("None of the above sounds correct and still unsure?",dest=target_lang).text):
            st.write(translator.translate('''You might be covered by another similar award like:
            \n - Hospitality Award
            \n - Retail Award
            \n - Restaurant Award
            \n - Food and Beverage Manufacturing Award 
            \n Please visit this website [Fair Work Fast Food Industry Guide](https://www.fairwork.gov.au/find-help-for/fast-food-restaurants-cafes/fast-food-industry)''',dest=target_lang).text)

        st.subheader(translator.translate("Now, let's find your award level", dest=target_lang).text, divider="rainbow")

        st.write(translator.translate('''
        \n :fries: Level 1 Duties
        \n - You take orders, prepare/cook/serve/deliver meals, snacks and/or beverages and may perform other related tasks like cleaning including toilets.
        \n
        \n :pizza: Level 2 Duties 
        \n - You supervise and train new staff or need to use trade skills in your day-to-day job.
        \n 
        \n :hamburger: Level 3 Duties 
        \n - You manage a whole shop or delivery service, either overseeing people or not (in charge of 1 or no persons, OR in charge of 2 or more persons). 
        ''',dest=target_lang).text)

        st.subheader(translator.translate("Finally, depending on your employment status, you have entitlements", dest=target_lang).text, divider="rainbow")

        st.write(translator.translate('''
        \n Full Time 
        \n - Average 38 hours per week. Ongoing employment, with a notice of termination. 
        \n - Paid annual, sick and carer's leave. 
        \n Part Time 
        \n - Less than 38 hours per week, but regular hours. Ongoing employment, with a notice of termination. 
        \n - By law, you must have a written agreement that includes the days and hours that you work with start and finish times. Any changes must be agreed in writing.
        \n - Paid annual, sick and carer's leave. 
        \n Casual 
        \n - Irregular hours with no set pattern per week. No notice of termination is required. 
        \n - You have the right to ask to convert to permanent in some situations. 
        \n - Not eligible for annual, sick and carer's leave. 
        ''',dest=target_lang).text)

        st.subheader(translator.translate("Ready to go back?",dest=target_lang).text)
        fastfood_to_home = st.button("Take me to Know Your Wages App :arrow_forward:")
        if fastfood_to_home:
            switch_page("Know Your Wages")

    elif award == "General Retail Industry Award":
        retail = Image.open("gallery/Retail.jpg")
        st.image(retail, width=400)

        st.subheader(
            translator.translate("You have selected the General Retail Industry Award. Let's understand your work rights!",
                                 dest=target_lang).text)

        with st.expander(translator.translate("What is the General Retail Industry Award?", dest=target_lang).text):
            st.write(translator.translate('''The General Retail Industry Award is an employment regulation that applies to employers and employees in the general retail sector. 
            This sector includes businesses involved in selling goods or services to consumers for personal, household, or business use.''',
                                          dest=target_lang).text)
        with st.expander(translator.translate("Who does it cover?", dest=target_lang).text):
            st.write(translator.translate('''The award covers a variety of retail businesses, including supermarkets, clothing stores, travel agencies, and more. 
            It also includes specific job roles like check-out operators, sales assistants, managers, and tradespersons such as butchers and florists. 
            It even extends to labor hire businesses and certain apprentices and trainees in the retail industry.''',
                                          dest=target_lang).text)

        with st.expander(translator.translate("What does it cover?", dest=target_lang).text):
            st.write(translator.translate('''The General Retail Industry Award covers tasks related to retail, including customer service, clerical work, and specific retail activities like bakery shops and newspaper deliveries. 
            It also applies to employees in related roles like trolley collectors and door-to-door salespersons.''',
                                          dest=target_lang).text)

        with st.expander(translator.translate("What doesn't it cover?", dest=target_lang).text):
            st.write(translator.translate('''This award doesn't apply to certain types of retail businesses and job roles. 
            It excludes employees in establishments like community pharmacies, stand-alone nurseries, hair and beauty establishments, and those involved in manufacturing or warehousing. 
            Additionally, it doesn't cover specific industries such as fast food, hair and beauty (except in certain contexts), and motor vehicles retailing.''',
                                          dest=target_lang).text)

        with st.expander(
                translator.translate("None of the above sounds correct and still unsure?", dest=target_lang).text):
            st.write(translator.translate('''If you are uncertain whether the award applies, it's important to check if the specific job role or business type is listed in the General Retail Industry Award. 
            If not, employees and employers might be covered by other industry-specific awards, such as the Fast Food Award or the Hair and Beauty Award.
                    \n Please visit this website [Fair Work General Retail Guide](https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000004-summary)''',
                                          dest=target_lang).text)

        st.subheader(translator.translate("Now, let's find your award level", dest=target_lang).text, divider="rainbow")

        st.write(translator.translate('''
                \n Level 1 - Entry-Level Positions
                \n - For beginners in the retail industry. Employees at this level usually have simple tasks and responsibilities.
                \n - Tasks include: stocking shelves with products, assisting customers with basic queries, operating cash registers and processing payments, packing items for customers, cleaning and maintaining the store
                \n Level 2 - Skilled Support Roles 
                \n - These positions require a bit more skill and experience than Level 1. Employees perform specific tasks that require training.
                \n - Tasks include: operating machinery like forklifts, handling delicate or specialised products, assisting customers with detailed product information, organising store displays and managing store inventory.
                \n Level 3 - Supervisory and Team Leader Roles
                \n - Employees at this level manage small teams and handle more complex responsibilities.
                \n - Tasks include: supervising a section or team within the store, opening and closing the store, ensuring store security and managing cash, providing training to Level 1 and 2 employees, handling customer complaints and complex inquiries.
                \n Level 4 - Management and Specialisation 
                \n - For experienced managers. Employees are responsible for specific sections and have expertise in certain areas.
                \n - Tasks include: managing defined store sections or departments, supervising multiple employees, controlling stock levels and ordering products, utilising specialised skills (e.g., butchers, bakers) and monitoring quality and resolving operational issues.
                \n Level 5 - Leadership and Trade Expertise
                \n - Involve leading teams of skilled workers. Employees have significant expertise in specific trades or areas of the store.
                \n - Tasks include: leading teams of tradespeople, overseeing specialized departments (e.g., bakery, butchery), training and guiding employees in technical skills, ensuring high-quality products and services.
                \n Level 6 - Senior Management 
                \n - For experienced senior managers. Employees manage entire departments or sections of large stores.
                \n - Tasks include: managing departments with multiple teams, setting goals and targets for the department, implementing company policies and procedures, handling complex customer issues and supervising lower-level managers.
                \n Level 7 - Visual Merchanising and Design
                \n -  Focus on visual aspects of the store. Employees create appealing displays and enhance the store's aesthetics.
                \n - Tasks include: designing store layouts and displays, selecting and arranging products for promotions, ensuring visual consistency across the store, advising on store aesthetics and ambiance, collaborating with marketing teams for special events.
                \n Level 8 - High-Level Management 
                \n - Employees at this level have extensive experience and handle complex strategic tasks.
                \n - Tasks include: understanding organisational objectives and industry trends, analyzing financial and staffing reports, making strategic decisions for the store, managing budgets and resources, supervising and mentoring lower-level managers.
                \n
                \n NOTE: Your employment level depends on your skills, experience, and the complexity of tasks you can handle. Consider your abilities and the tasks mentioned for each level to determine your appropriate employment level in the retail industry.
                ''', dest=target_lang).text)

        st.subheader(translator.translate("Finally, depending on your employment status, you have entitlements",
                                          dest=target_lang).text, divider="rainbow")

        st.write(translator.translate('''
                \n Full Time 
                \n - Average 38 hours per week. Ongoing employment, with a notice of termination. 
                \n - Paid annual, sick and carer's leave. 
                \n Part Time 
                \n - Less than 38 hours per week, but regular hours. Ongoing employment, with a notice of termination. 
                \n - By law, you must have a written agreement that includes the days and hours that you work with start and finish times. Any changes must be agreed in writing.
                \n - Paid annual, sick and carer's leave. 
                \n Casual 
                \n - Irregular hours with no set pattern per week. No notice of termination is required. 
                \n - You have the right to ask to convert to permanent in some situations. 
                \n - Not eligible for annual, sick and carer's leave. 
                ''', dest=target_lang).text)

        st.subheader(translator.translate("Ready to go back?", dest=target_lang).text)
        retail_to_home = st.button("Take me to Know Your Wages App :arrow_forward:")
        if retail_to_home:
            switch_page("Know Your Wages")

    elif award == "Hospitality Industry (General) Award":
        hospo = Image.open("gallery/Hospitality.png")
        st.image(hospo, width=400)

        st.subheader(
            translator.translate("You have selected the Hospitality Industry (General) Award. Let's understand your work rights!",
                                 dest=target_lang).text)

        with st.expander(translator.translate("What is the Hospitality Industry (General) Award?", dest=target_lang).text):
            st.write(translator.translate('''The Hospitality Industry (General) Award is an employment regulation that applies to various sectors in the hospitality industry, such as hotels, restaurants, and casinos.''',
                                          dest=target_lang).text)
        with st.expander(translator.translate("Who does it cover?", dest=target_lang).text):
            st.write(translator.translate('''It covers employers in the hospitality industry, including hotels, motels, restaurants, and catering businesses. It also includes labor hire businesses and their employees placed within the hospitality sector.''',
                                          dest=target_lang).text)

        with st.expander(translator.translate("What does it cover?", dest=target_lang).text):
            st.write(translator.translate('''The award includes a wide range of employees like waiters, kitchen staff, clerical workers, and managerial staff who are not in senior positions. It also encompasses catering employees and casino staff.''',
                                          dest=target_lang).text)

        with st.expander(translator.translate("What doesn't it cover?", dest=target_lang).text):
            st.write(translator.translate('''The Hospitality Award does not apply to certain entities like registered clubs, in-flight catering for airlines, hospitals, local councils, and musicians performing in hotels. Additionally, senior management roles and specific contract services outside the hospitality sector are exempt.''',
                                          dest=target_lang).text)

        with st.expander(
                translator.translate("None of the above sounds correct and still unsure?", dest=target_lang).text):
            st.write(translator.translate('''You might be covered by another similar award like:
                    \n - Registered Clubs Award
                    \n - Restaurant Award
                    \n - Fast Food Award
                    \n Please visit this website [Fair Work Hospitality Industry Guide](https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000009-summary)''',
                                          dest=target_lang).text)

        st.subheader(translator.translate("Now, let's find your award level", dest=target_lang).text, divider="rainbow")

        st.write(translator.translate('''
                \n Introductory
                \n - If a new hospitality employee isn't skilled enough for level 1, they stay at their current level for 3 months. 
                After that, they go to level 1, unless both the employee and employer agree they need more training, which can last another 3 months.
                ''', dest=target_lang).text)

        st.write(translator.translate('''Select from the categories below and look for your **WAGE LEVEL**.''',dest=target_lang).text)
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Food & Beverages",
                                          "Kitchen",
                                          "Guest Services",
                                          "Admin",
                                          "Security",
                                          "Leisure",
                                          "Stores",
                                          "Maintenance & Trade",
                                          "Managerial Staff"])

        with tab1:
            st.write(translator.translate('''
            \n Attendant Grade 1 **(Wage Level 1)** - 
Doing tasks like picking up glasses, emptying ashtrays, helping in various ways, taking away used food plates, preparing and cleaning tables, and keeping places neat and clean.
            \n Attendant Grade 2 **(Wage Level 2)** - 
Providing alcohol, helping in the bottle section, serving food and drinks, cleaning tables, handling money, working at a snack bar, making deliveries, and taking reservations, welcoming and seating guests.
            \n Attendant Grade 3 **(Wage Level 3)** - 
Using a machine to lift heavy items, working with betting machines and electronic games, managing a liquor store, including receiving and recording goods, making fancy drinks, teaching and supervising lower-level food and beverage workers.
            \n Attendant Grade 4 **(Wage Level 4)** - 
An employee who finished special training for serving food or passed a test, doing skilled tasks in a fine dining room or a restaurant.
            \n Supervisor Grade 5 **(Wage Level 5)** - 
An employee who received proper training, including supervision training, and is responsible for guiding, training, and organizing food and beverage staff, or managing stock for one or more bars.
            ''', dest=target_lang).text)

        with tab2:
            st.write(translator.translate('''
            \n Kitchen Attendant Grade 1 **(Wage Level 1)** - 
Cleaning tasks in a kitchen or food area, like washing dishes and utensils, helping cooks, preparing ingredients, and general pantry duties.
            \n Kitchen Attendant Grade 2 **(Wage Level 2)** - 
A trained employee doing specific non-cooking tasks in a kitchen or supervising kitchen assistants.
            \n Kitchen Attendant Grade 3 **(Wage Level 3)** - 
An employee with proper training, including supervision training, who oversees, trains, and coordinates lower-level kitchen assistants.
            \n Cook Grade 1 **(Wage Level 2)** - 
An employee who cooks breakfasts and snacks, bakes, makes pastries, or works with meat as a butcher.
            \n Cook Grade 2 **(Wage Level 3)** - 
An employee who has the appropiate level of training and works higher than Cook Grade 1. 
            \n Cook Grade 3 **(Wage Level 4)** - 
A commi chef or similar, who finished training or passed a test, and is responsible for cooking, baking, making pastries, or butchering tasks.
            \n Cook Grade 4 **(Wage Level 5)** - 
A demi chef or similar, who finished training or passed a test, and is tasked with general or specific cooking, butchering, baking, or pastry cooking responsibilities. They may also supervise and train other cooks and kitchen staff.
            \n Cook Grade 5 **(Wage Level 6)** - 
A chef de partie or equivalent, who finished training or passed a test in cooking, butchering, baking, or pastry cooking, and 
performing various tasks, such as supervising and training kitchen staff, managing orders and controlling stock, and overseeing kitchen employees in one specific kitchen area.
            ''', dest=target_lang).text)

        with tab3:
            st.write(translator.translate('''
            \n Guest Services Grade 1 **(Wage Level 1)** - 
An employee involved in laundry tasks, minor clothing repairs, collecting and delivering guests' dry cleaning and laundry, performing general cleaning duties, and parking guests' vehicles.
            \n Guest Services Grade 2 **(Wage Level 2)** - 
An employee without adequate training engaged in tasks like cleaning rooms, assisting guests, driving vehicles, handling luggage, assisting in dry cleaning, using specialized cleaning equipment, and providing basic butler services.
            \n Guest Services Grade 3 **(Wage Level 3)** - 
An employee with proper training who supervises lower-level guest service employees, provides butler services, performs major repairs on linen or clothing, including basic tailoring and alterations, and handles dry cleaning tasks.
            \n Guest Services Grade 4 **(Wage Level 4)** - 
An employee who has finished an apprenticeship, passed a trade test, or received suitable training to work as a tradesperson in dry cleaning, tailoring, or as a butler.
            \n Guest Services Supervisor **(Wage Level 5)** - 
An employee with proper training and supervisory skills who oversees, trains, and coordinates staff in the housekeeping department.
            \n Front Office Grade 1 **(Wage Level 2)** - 
An employee who assists with front office tasks, including night auditing, answering phones, welcoming guests, handling cash, providing information, and making reservations.
            \n Front Office Grade 2 **(Wage Level 3)** - 
An employee with suitable training working in the front office, performing tasks such as answering phones, welcoming guests, handling cash, providing information, and making reservations.
            \n Front Office Grade 3 **(Wage Level 4)** - 
An employee with adequate training, working in the front office, assisting in training, and supervising lower-level front office staff.
            \n Front Office Supervisor **(Wage Level 5)** - 
An employee with proper training and supervisory skills who oversees, trains, and coordinates front office staff.
            ''', dest=target_lang).text)

        with tab4:
            st.write(translator.translate('''
            \n Clerical Grade 1 **(Wage Level 2)** - 
An employee responsible for basic clerical tasks like collating, filing, photocopying, and delivering messages.
            \n Clerical Grade 2 **(Wage Level 3)** - 
An employee performing general office tasks including typing, filing, basic data entry, and calculations.
            \n Clerical Grade 3 **(Wage Level 4)** - 
A trained employee operates office equipment, handles data entry, transcribes information, manages financial documents, and uses computer software. They also arrange travel, screen calls, respond to inquiries, and handle financial records.
            \n Clerical Supervisor **(Wage Level 5)** - 
An employee with proper training, including supervisory skills, who organises other clerical staff.
            ''', dest=target_lang).text)

        with tab5:
            st.write(translator.translate('''
            \n Doorperson/Security Officer Grade 1 **(Wage Level 2)** - 
A person who helps maintain dress standards and good order at a place or establishment.
            \n Timekeeper/Security Officer Grade 2 **(Wage Level 3)** - 
A person in charge of employee timekeeping, key security, checking delivery vehicles, or supervising doorperson/security officer grade 1 employees.
            ''', dest=target_lang).text)

        with tab6:
            st.write(translator.translate('''
            \n Leisure Attendant Grade 1 **(Wage Level 2)** - 
A trained person who assists instructors, oversees pool activities, sets up equipment, manages distribution, and handles bookings.
            \n Leisure Attendant Grade 2 **(Wage Level 3)** - 
A trained person who leads classes or supervises leisure activities like sports, health clubs, and swimming pools.
            \n Leisure Attendant Grade 3 **(Wage Level 4)** - 
A trained person who organises leisure activities for guests and may oversee other leisure attendants.
            ''', dest=target_lang).text)

        with tab7:
            st.write(translator.translate('''
            \n Storeperson Grade 1 **(Wage Level 2)** - 
An employee responsible for receiving, storing general and perishable goods, and cleaning the storage area.
            \n Storeperson Grade 2 **(Wage Level 3)** -
An employee in storeperson grade 1, who can also operate machinery like a forklift or perform more complex tasks.
            \n Storeperson Grade 3 **(Wage Level 4)** - 
A trained employee overseeing quality control, managing a warehouse area, guiding staff, and coordinating activities. They handle communication with management, suppliers, and customers, maintain inventory records, supervise goods receipt and delivery, and may assist in on-the-job training.
            ''', dest=target_lang).text)

        with tab8:
            st.write(translator.translate('''
            \n Handyperson **(Wage Level 3)** - 
Someone who is not a professional tradesperson but is responsible for regular repair and maintenance tasks within the employer's premises.
            \n Forklift Driver **(Wage Level 3)** - 
An employee with a valid forklift license, hired specifically to operate a forklift vehicle.
            \n Gardener Grade 1 **(Wage Level 2)** - 
An employee mainly responsible for tasks such as cleaning, weeding, watering, trimming, and preparing areas for play. They assist in maintenance, use limited vehicles, and perform related non-trade duties.
            \n Gardener Grade 2 **(Wage Level 3)** - 
An employee in this grade, beyond grade 1 duties, operates and maintains motorized equipment under supervision, assists in maintaining playing surfaces and trees, applies chemicals with general supervision, does gardening tasks, maintains play surfaces, keeps basic records, aids in facility construction, performs related tasks, handles minor repairs, and supervises lower-level gardeners.
            \n Gardener Grade 3 **(Wage Level 4)** - 
An employee with trade qualifications who performs various tasks, including operating and maintaining machinery, cleaning and inspecting machinery, applying chemicals as directed, preparing playing surfaces, maintaining vehicles, doing repairs and renovation work, gardening, planting trees, and supervising lower-level employees.
            \n Gardener Grade 4 **(Wage Level 5)** - 
An employee with proper training and additional supervision skills who supervises lower-level workers, presents reports, liaises with management, and applies specialist skills, besides performing duties from levels 1 to 3.
            ''', dest=target_lang).text)

        with tab9:
            st.write(translator.translate('''
            \n Hotel Manager - 
Oversees different hotel areas, directing staff and ensuring rules are followed. They manage finance or human resources, but not top managers. Titles like company secretary or chief accountant can be hotel managers. Training or hotel staff experience is needed.
            ''', dest=target_lang).text)

        st.subheader(translator.translate("Finally, depending on your employment status, you have entitlements",
                                          dest=target_lang).text, divider="rainbow")

        st.write(translator.translate('''
                \n Full Time 
                \n - Average 38 hours per week. Ongoing employment, with a notice of termination. 
                \n - Paid annual, sick and carer's leave. 
                \n Part Time 
                \n - Less than 38 hours per week, but regular hours. Ongoing employment, with a notice of termination. 
                \n - By law, you must have a written agreement that includes the days and hours that you work with start and finish times. Any changes must be agreed in writing.
                \n - Paid annual, sick and carer's leave. 
                \n Casual 
                \n - Irregular hours with no set pattern per week. No notice of termination is required. 
                \n - You have the right to ask to convert to permanent in some situations. 
                \n - Not eligible for annual, sick and carer's leave. 
                ''', dest=target_lang).text)

        st.subheader(translator.translate("Ready to go back?", dest=target_lang).text)
        hospo_to_home = st.button("Take me to Know Your Wages App :arrow_forward:")
        if hospo_to_home:
            switch_page("Know Your Wages")

else:
    pass

