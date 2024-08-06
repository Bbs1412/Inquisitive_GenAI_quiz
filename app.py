from datetime import datetime
import app_gemini as api
import streamlit as st
import pandas as pd
import json
import time


# ======================================================================
# Page Configuration
# ======================================================================

st.set_page_config(
    # page_title="Bhushan Songire",
    page_title="Inquisitive - Quiz Generator",

    page_icon="✨",
    # Can also use a path to an image file as the favicon

    layout="centered",
    # layout="wide",

    # initial_sidebar_state="collapsed"
    initial_sidebar_state="expanded"
)

# ======================================================================
# Header and sidebar section:
# ======================================================================

st.logo("./images/Infinity.jpg")

st.header(":red[GenAI] powered :green[_Quiz_] Generator 📝", divider="rainbow")
# st.header(":rainbow[GenAI powered _Quiz_ Generator ] 📝", divider='rainbow')


# st.header(":rainbow[GenAI powered _Quiz_ Generator ]", divider="rainbow")
# st.divider()


# Sidebar for page choice:
st.sidebar.header(':orange[Page Selection :]')
pages = ['Main Page', 'Debug Section']
# curr_page = st.sidebar.radio(
#     label="Which Page to See:",
#     options=pages,
#     label_visibility="collapsed"
# )
curr_page = st.sidebar.selectbox(
    label="Which Page to See:",
    options=pages,
    label_visibility="collapsed"
)

st.sidebar.header(":orange[Made By :]", anchor='credits')
cont = st.sidebar.container(border=True)


cont.subheader("Profile:", divider='red')
cont.image("./images/my_pic_720.png", caption='Bhushan Songire')
# cont.image("./images/my_pic_1080.png")
# cont.write(":blue[Bhushan Songire]")

cont.text("Hi👋, I'm Bhushan Songire.")
cont.text("CSE 💻 student @ VIT-Chennai.")

cont.subheader("Connect With me:", divider='red')


def get_url(image_id: str, size: int = 30, color: str = '000000', format: str = "png") -> str:
    # url = "https://img.icons8.com/?size=30&id=3AYCSzCO85Qw&format=png&color=000000"
    url = f"https://img.icons8.com/?size={size}&id={image_id}&format={format}&color={color}"
    return url


c1, c2 = cont.columns([2, 11], vertical_alignment="center", gap='small')
c1.image(get_url(13930))
c2.markdown('[/bhushan-songire](https://www.linkedin.com/in/bhushan-songire)')

c1, c2 = cont.columns([2, 11], vertical_alignment="center", gap='small')
c1.image(get_url(106564))
c2.markdown('[/Bbs1412](https://github.com/Bbs1412/)')

c1, c2 = cont.columns([2, 11], vertical_alignment="center", gap='small')
c1.image(get_url('P7UIlhbpWzZm'))
c2.markdown('[bhushanbsongire@gmail.com](mailto:bhushanbsongire@gmail.com)')


# Feel free to connect with me on social media!
st.sidebar.header(':orange[Upcoming Features :]')
st.sidebar.markdown("""
                    1. Certificate Generation
                    1. Multilingual Support
                    1. Result Sharing
                    """)


# ======================================================================
# Global Variables (necessary for the functioning):
# ======================================================================
# State variables are like global variables but, streamlit version
# Initialize session state variables

if 'user_topic' not in st.session_state:
    st.session_state.user_topic = ""

if 'user_context' not in st.session_state:
    st.session_state.user_context = ""

if "customized" not in st.session_state:
    st.session_state.customized = False

if "quiz_config" not in st.session_state:
    st.session_state.quiz_config = {
        "count": 10,
        "difficulty": 'Easy',
        "hint": True,
    }

if "lock_config" not in st.session_state:
    st.session_state.lock_config = False

if 'api_called_once' not in st.session_state:
    st.session_state.api_called_once = False

if 'lock_generate_btn' not in st.session_state:
    st.session_state.lock_generate_btn = False

if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'result_btn' not in st.session_state:
    st.session_state.result_btn = False

if 'answer_checked' not in st.session_state:
    st.session_state.answer_checked = False

if 'celebrate' not in st.session_state:
    st.session_state.celebrate = True

if 'certificate' not in st.session_state:
    st.session_state.certificate = False


# ar = np.arange(10, 50, 0.5).reshape(8, 10)
# st.write(ar)

# ======================================================================
# User Input Section:
# ======================================================================
st.subheader(":orange[Text Input]",
             #  divider="violet",
             )
# 📋

c1, c2 = st.columns([4, 6], vertical_alignment='center')

ip_name = c1.text_input(
    "Your Name:",
    placeholder='Name'
)

if ip_name:
    st.session_state.user_name = ip_name

# st.text("Please paste some text paragraph or entire news article to generate quiz.")

ip_context = st.text_area(
    label="Context:",
    help="You can provide me with a news article, scientific study, historical event, fictional story, technical specification, or any large text.",
    placeholder="Paste an article, text paragraphs, or a complete news article here to generate a quiz... (Press ❓ icon for quick help)",
)

if ip_context:
    st.session_state.user_context = ip_context


ip_topic = st.text_input(
    label="Or",
    help="Provide a topic or a brief context to receive a paragraph and generate a quiz based on it.",
    placeholder="Ask me some topic to generate quiz on...",
)

if ip_topic:
    st.session_state.user_topic = ip_topic

# ======================================================================
# Customizations in quiz:
# ======================================================================

# advanced = st.button("Customize Quiz 🔽 :gear:")
advanced = st.button(":gear:")
lock_btn = False

if advanced:
    st.session_state.customized = not st.session_state.customized

if st.session_state.customized:

    st.markdown("""
            <h5 class="tt">You can customize the quiz using available options:</h5>

            <style>
                .tt{
                    color: #FBC045;
                }
            </style>
        """, unsafe_allow_html=True)

    c1, c2, cx = st.columns([3, 4, 3], vertical_alignment='center')
    c1.text("Difficulty Level")
    opts = 'Easy Medium Hard'.split()
    que_difficulty = c2.selectbox(
        label="Difficulty Level",
        options=opts,
        index=opts.index(st.session_state.quiz_config['difficulty']),
        disabled=st.session_state.lock_config,
        label_visibility='collapsed'
    )

    # c1, c2 = st.columns(2)
    c1, c2, cx = st.columns([3, 4, 3], vertical_alignment='center')
    c1.text("Number of Questions")

    que_count = c2.slider(
        label="Number of questions",
        min_value=5,
        step=5,
        max_value=20,
        value=st.session_state.quiz_config['count'],
        disabled=st.session_state.lock_config,
        label_visibility='collapsed'
    )

    # c1, c2 = st.columns(2)
    c1, c2, cx = st.columns([3, 4, 3], vertical_alignment='top')
    c1.text("Do you want Hints?")
    que_hint = c2.toggle(
        label="\n Hints show up only when you click :bulb: icon.",
        value=st.session_state.quiz_config['hint'],
        disabled=st.session_state.lock_config,
        # label_visibility='collapsed'
    )

    c1, c2, cx = st.columns([3, 4, 3], vertical_alignment='center')
    c1.text("Mark Changes")
    lock_btn = c2.button(
        label="Done",
        disabled=st.session_state.lock_config,
        # label_visibility='collapsed'
    )

# Set config as per user input, and if unchanged, then set to some defaults:

# if config customizations is not locked, means not yet customized:
if not st.session_state.lock_config:
    # if config is created for first time:
    if lock_btn:
        st.session_state.quiz_config = {
            "count": que_count,
            "difficulty": que_difficulty,
            "hint": que_hint,
        }
        st.session_state.lock_config = True
        st.rerun()

# ======================================================================
# Question Generation engine
# ======================================================================
generate_btn = st.button(
    "Generate Quiz ✨",
    type='primary',
    disabled=st.session_state.lock_generate_btn
)

# Check n lock the quiz customization (if not done yet) and lock generate button
if generate_btn:
    # If lock_config is false, means user didn't customize
    if not st.session_state.lock_config:
        st.session_state.lock_config = True

    if not st.session_state.lock_generate_btn:
        st.session_state.lock_generate_btn = True
    st.rerun()

# If generate button is locked, generate the quiz:
if st.session_state.lock_generate_btn and (not st.session_state.api_called_once):
    st.session_state.api_called_once = True

    # no context or topic:
    if (not st.session_state.user_context) and (not st.session_state.user_topic):
        with st.spinner('Generating the quiz...'):
            time.sleep(2)
            st.session_state.quiz_config['count'], st.session_state.user_context, st.session_state.quiz_ques = api.blank_call_default(
            )
            st.session_state.quiz_generated = True

    else:                                                   # context or topic is given
        tmp_cont = st.container()
        tmp_cont.write("Status:")

        with st.spinner('Setting up the requirements...'):
            time.sleep(0.6)
            resp = api.set_up_requirements(st.secrets['API'])

            if (resp == "Error"):
                st.warning("Some Error Occurred, Sorry for inconvenience.")
            else:
                tmp_cont.write("✅ Setup Successful...")

        with st.spinner('Starting the question engine...'):
            time.sleep(1)
            resp = api.start_question_engine()

            if (resp == "Error"):
                st.warning("Some Error Occurred, Sorry for inconvenience.")
            else:
                tmp_cont.write("✅ Question Engine started successfully...")

        with st.spinner('Generating the quiz...'):
            time.sleep(1)

            # Here, first it will look if topic is entered,
            # if yes,
            # generate para as context
            # immediate next `if` will check the context being present or not,
            # and since we filled this generated para as context, it will continue its quiz routine
            # if no:
            # then proceed to take entered context and generate quiz

            if st.session_state.user_topic:                 # if topic entered
                resp = api.generate_para(st.session_state.user_topic)

                if (resp == "Error"):
                    st.warning("Some Error Occurred, Sorry for inconvenience.")
                else:
                    tmp_cont.write("✅ Paragraph generated successfully...")
                    st.session_state.user_context = resp['paragraph']

            if st.session_state.user_context:               # if context entered
                resp = api.generate_quiz(
                    context=st.session_state.user_context,
                    no_of_ques=st.session_state.quiz_config['count'],
                    difficulty=st.session_state.quiz_config['difficulty'],
                )
                if (resp == "Error"):
                    st.warning("Some Error Occurred, Sorry for inconvenience.")
                else:
                    st.session_state.quiz_config['count'], st.session_state.quiz_ques = resp
                    tmp_cont.write("✅ Created Quiz based on context...")
                    st.session_state.quiz_generated = True

            else:
                st.warning(
                    "Some Logical Error Occurred, Sorry for inconvenience.")

        tmp_cont.empty()

    st.toast("You can attempt the quiz now!!!")
    time.sleep(1.5)
    # st.rerun()


def generate_mcq(que_no: int, que: str, options: list,
                 hint: str | None = None,
                 pre_selected: int | None = None) -> int | None:
    """_summary_

    Args:
        que_no (int): Number of the question
        que (string): What is the question?
        options (list): list which contains the options as strings
        hint (string): Hint for the answer if available
        pre_selected (optional): Option number of pre-selected radio button

    Returns:
        selected: the option number of selected option
    """

    col_que_no, col_que, col_hint = st.columns([0.1, 0.85, 0.05], gap='small')
    col_que_no.write(f"Q{que_no}]")
    col_que.write(f"{que}")
    # st.text(f"Q{que_no}]  {que}")

    need_hint = col_hint.button(":bulb:",
                                key=f"h_q{que_no}",
                                disabled=not st.session_state.quiz_config['hint']
                                )
    if need_hint:
        col_none, col_hint = st.columns([0.1, 0.9], gap='small')
        col_hint.info(f"{hint}")

    col_none, col_opts = st.columns([0.1, 0.9], gap='small')

    def mapper(param, opts=options):

        dic = {}
        for i in range(0, len(opts)):
            dic[f'{i+1}'] = opts[i]

        return dic[param]

    selected = col_opts.radio(
        label="Options:",
        options=[str(i+1) for i in range(len(options))],
        format_func=mapper,
        index=pre_selected-1 if (pre_selected != None) else None,
        key=f"q_{que_no}",
        disabled=st.session_state.submitted,
    )
    # this 'selected' is 1..4 (but string)
    # so return with typecast
    return int(selected) if selected else None


def generate_multiple(que_no: int, que: str, options: list,
                      hint: str | None = None,
                      pre_selected: list | None = None) -> list | None:
    """_summary_

    Args:
        que_no (int): Number of the question
        que (string): What is the question?
        options (list): list which contains the options as strings
        hint (string): Hint for the answer if available
        pre_selected (list): Option number of pre-selected radio button

    Returns:
        selected: the option number of selected option
    """

    col_que_no, col_que, col_hint = st.columns([0.1, 0.85, 0.05], gap='small')
    col_que_no.write(f"Q{que_no}]")
    col_que.write(f"{que}")
    # st.text(f"Q{que_no}]  {que}")

    need_hint = col_hint.button(":bulb:",
                                disabled=not st.session_state.quiz_config['hint'],
                                key=f"h_q{que_no}"
                                )
    if need_hint:
        col_none, col_hint = st.columns([0.1, 0.9], gap='small')
        col_hint.info(f"{hint}")

    col_none, col_opts = st.columns([0.1, 0.9], gap='small')

    def mapper(param, opts=options):
        dic = {}
        for i in range(0, len(opts)):
            dic[f'{i+1}'] = opts[i]
        return dic[param]

    selected = col_opts.multiselect(
        label="Multiple correct options:",
        options=[str(i+1) for i in range(len(options))],
        format_func=mapper,
        default=pre_selected-1 if (pre_selected != None) else None,
        placeholder="Please select one or more from below options",
        key=f"q_{que_no}",
        disabled=st.session_state.submitted
    )

    if selected:
        # return [int(i) for i in selected]
        return sorted([int(i) for i in selected])
    return None


def generate_numeric(que_no: int, que: str,
                     hint: str | None = None,
                     pre_selected: int = 0) -> int:
    """_summary_

    Args:
        que_no (int): Number of question
        que (str): Question string
        hint (string): Hint for the answer if available
        pre_selected (optional): Pre-selected number from user
    Returns:
        ans (integer): default 0 or user input integer
    """

    col_que_no, col_que, col_hint = st.columns([0.1, 0.85, 0.05], gap='small')
    col_que_no.write(f"Q{que_no}]")
    col_que.write(f"{que}")
    # st.text(f"Q{que_no}]  {que}")

    need_hint = col_hint.button(":bulb:",
                                disabled=not st.session_state.quiz_config['hint'],
                                key=f"h_q{que_no}"
                                )
    if need_hint:
        col_none, col_hint = st.columns([0.1, 0.9], gap='small')
        col_hint.info(f"{hint}")

    col_blank, col_input = st.columns([0.1, 0.9], gap='small')
    col2_ip, col2_text = col_input.columns(
        [0.4, 0.6], gap='small', vertical_alignment='bottom')

    col2_text.info("Enter the answer in ***integer*** only!", icon="ℹ️")
    ans = col2_ip.number_input(
        "Input:",
        min_value=0,
        step=1,
        value=pre_selected if pre_selected != None else 0,
        key=f"q_{que_no}",
        disabled=st.session_state.submitted
    )

    return ans


def generate_bool(que_no: int, que: str,
                  hint: str | None = None,
                  pre_selected: None | str = None) -> str | None:
    """_summary_

    Args:
        que_no (int): Number of question
        que (str): Question string
        hint (string): Hint for the answer if available
        pre_selected (optional): Pre-selected answer from user

    Returns:
        sel (str | None): selected option as string or default None
    """

    col_que_no, col_que, col_hint = st.columns([0.1, 0.85, 0.05], gap='small')
    col_que_no.write(f"Q{que_no}]")
    col_que.write(f"{que}")
    # st.text(f"Q{que_no}]  {que}")

    need_hint = col_hint.button(":bulb:",
                                disabled=not st.session_state.quiz_config['hint'],
                                key=f"h_q{que_no}"
                                )
    if need_hint:
        col_none, col_hint = st.columns([0.1, 0.9], gap='small')
        col_hint.info(f"{hint}")

    col_none, col_input = st.columns([0.1, 0.9], gap='small')
    col2_dropdown, col2_text = col_input.columns(
        [0.4, 0.6], gap='small', vertical_alignment='bottom')

    # col2_text.info("Select `True` or `False`", icon="ℹ️")
    sel = col2_dropdown.selectbox(
        label="Select `True` or `False`:",
        options=['True', 'False'],
        index=None if pre_selected == None else pre_selected,
        key=f"q_{que_no}",
        disabled=st.session_state.submitted
    )

    return sel


# ======================================================================
# The main logic for evaluation of user responses!
# ======================================================================
main_thing = {}

if st.session_state.quiz_generated:                 # Show ques on page
    st.subheader(":orange[Context:]", divider='gray')
    c = st.container(border=True)
    c.write(st.session_state.user_context)

    st.subheader(
        ":orange[Quiz]",
        # divider="violet",
        divider='grey'
    )
    # ✏️

    for que in st.session_state.quiz_ques:
        # st.write(i)
        if que['type'] == "MCQ":
            response = generate_mcq(
                que_no=que['que_no'],
                que=que['question'],
                options=que['options'],
                hint=que['hint'],
                pre_selected=None
            )

        elif que['type'] == "Multiple":
            response = generate_multiple(
                que_no=que['que_no'],
                que=que['question'],
                options=que['options'],
                hint=que['hint'],
                pre_selected=None
            )

        elif que['type'] == "Bool":
            response = generate_bool(
                que_no=que['que_no'],
                que=que['question'],
                hint=que['hint'],
                pre_selected=None
            )

        elif que['type'] == "Numeric":
            response = generate_numeric(
                que_no=que['que_no'],
                hint=que['hint'],
                que=que['question']
            )

        # st.write(response)

        q_no = que['que_no']
        main_thing[f'Q{q_no}'] = {
            "type": que['type'],
            "que": que['question'],
            "user": response,
            "answer": que['answer'],
            "hint": que['hint'],
        }

    # Now, first give user submit button, then enable results button.
    # Submit button

    linkedin = "https://www.linkedin.com/in/bhushan-songire/"
    cond = st.checkbox(f"I agree to [Terms and Conditions]({linkedin}) ...",
                       disabled=st.session_state.submitted)

    agreed = False
    if cond:
        agreed = True

    submit_btn = st.button("Submit 📤",
                           type='primary',
                           # block the button once clicked
                           disabled=st.session_state.submitted
                           )

    if submit_btn:
        if agreed:
            st.session_state.submitted = True
            # Re-run for blocking the button
            time.sleep(0.5)
            st.toast("You can see the result now")
            st.rerun()
        else:
            st.error(" Agree T&C first", icon="⚠️")


# Enable "Get Results" button only if submitted
# Also, lock the answer submitting of the questions
if st.session_state.submitted:
    st.success(" Submitted your responses successfully...", icon="✅")

    time.sleep(1)
    result_btn = st.button("Get Results 🎯",
                           # Need not block this button like submit
                           # disabled=st.session_state.result_btn
                           )
    if result_btn:
        st.session_state.result_btn = True
        # Re-run for blocking the button
        # st.rerun()

# ======================================================================
# Show results if "Get Results" button is clicked
# ======================================================================
if st.session_state.result_btn:                     # get results
    st.subheader(":orange[Results: ]", divider='grey')

    # Each question will be given diff weighage
    # in each question, total_marks will be updated
    # in the end, divide to get the final % score
    marks_obtained = 0
    marks_total = 0
    ques_count = st.session_state.quiz_config['count']

    # if changing marking scheme, do update checking logic for "multiple" as well in the below snippet...
    mark_scheme = {
        "MCQ": 3,
        "Multiple": 10,
        "Bool": 2,
        "Numeric": 6
    }

    for i in range(0, ques_count):                  # iterate-questions
        curr = main_thing[f'Q{i+1}']
        # st.write(curr)

        max_marks = 0
        curr_marks = 0

        if curr['type'] == 'MCQ':                   # Q:mcq
            max_marks = mark_scheme['MCQ']
            if curr['user'] == curr['answer']:
                curr_marks = max_marks
            else:
                curr_marks = 0

        elif curr['type'] == 'Multiple':            # Q:multiple correct
            max_marks = mark_scheme['Multiple']
            # if answer is empty (means, user didn't attempt que)
            if not curr['user']:                    # que-unattempted
                curr_marks = 0
            else:                                   # que-attempted
                # extra logic for partial correct and all
                m_total_correct_options = len(curr['answer'])
                m_user_correct_options = 0

                for usr_ans in curr['user']:        # iterate-submissions

                    if usr_ans in curr['answer']:   # correct-answer
                        m_user_correct_options += 1

                    else:                           # wrong-answer
                        m_user_correct_options = 0
                        break

                # Full marks:
                if m_user_correct_options == m_total_correct_options:
                    curr_marks = max_marks

                # Partial marks (near full) (just missed):
                elif m_user_correct_options == m_total_correct_options-1:
                    curr_marks = max_marks - 2

                # Partial marks:
                elif m_user_correct_options < m_total_correct_options:
                    curr_marks = max_marks // 2

                # Incorrect answer marks:
                else:
                    curr_marks = 0

        elif curr['type'] == 'Numeric':             # Q:numeric type
            max_marks = mark_scheme['Numeric']
            if curr['user'] == curr['answer']:
                curr_marks = max_marks
            else:
                curr_marks = 0

        elif curr['type'] == 'Bool':                # Q:True-False
            max_marks = mark_scheme["Bool"]
            if curr['user'] == curr['answer']:
                curr_marks = max_marks
            else:
                curr_marks = 0

        # Section to show progress bar...
        marks_obtained += curr_marks
        marks_total += max_marks
        main_thing[f'Q{i+1}']['marks_obt'] = curr_marks
        main_thing[f'Q{i+1}']['marks_max'] = max_marks

    marks_percentage = marks_obtained / marks_total * 100
    st.session_state.answer_checked = True


# ======================================================================
# Output Section
# ======================================================================
if st.session_state.answer_checked:                 # result-display

    # To avoid that repeated balloons celebration when section is changed
    if st.session_state.celebrate:
        bar_level = 0
        info_text = st.text("Evaluating your responses 📊")
        time.sleep(2)
        wait_time = 5
        processing = st.progress(bar_level)

        for i in range(0, ques_count):
            time.sleep(wait_time / ques_count)
            # time.sleep(0.01)
            info_text.text(f"Checking Question [ {i+1} / {ques_count} ] ...")
            bar_level = int((i+1) / ques_count * 100)
            processing.progress(bar_level)

        # Remove the progress bar and related things
        info_text.empty()
        processing.empty()
        st.balloons()
        st.session_state.celebrate = False

    actions = st.columns(4, vertical_alignment='center')

    act_btn_showResults = actions[0].button("Show Result")
    # act_btn_certificate = actions[1].button("Certificate")
    act_btn_marks_table = actions[1].button("Marks Split")
    act_btn_analyze_ans = actions[2].button("Analyze Ans")
    act_btn_feedbackDev = actions[3].button("Dev Feedback")

    # create form to get that nice outline or border:
    # result_box = st.form(key="bbs", clear_on_submit=False)
    result_box = st.container(border=True)

    i1, display, ignore2 = result_box.columns([0.5, 99, 0.5])

    # Fixed section to display everywhere:
    def fixed_part(cont):                           # always show this
        """
        cont: Container name
        """
        cont.subheader(
            f"Congratulations :blue[{st.session_state.user_name}] 🎆")
        # cont.markdown("###### Your quiz score is:")

    fixed_part(display)

    if act_btn_showResults:                         # result section
        display.latex(fr"""
            \frac {{Obtained\ Marks}} {{Total\  Marks}}
            =
            \frac {{{marks_obtained}}} {{{marks_total}}}
        """)

        display.latex(f"You \ got: \ {{{round(marks_percentage,2)}}}\ \%")

        # result_box.form_submit_button("Thank You 🙏", disabled=True)

    elif act_btn_marks_table:                       # marks split
        df = pd.DataFrame(main_thing).transpose()
        # (que_no), type, que, user, answer, hint, marks-obt, max
        df.drop(columns=['que', 'hint'], axis=1, inplace=True)
        df.columns = ["Que type", "Your Answer",
                      "Correct Answer", "Obt Marks", "Max Marks"]

        # display.dataframe(df, use_container_width=True)
        display.table(df)

        # result_box.form_submit_button("Thank You 🙏", disabled=True)

    elif act_btn_feedbackDev:                       # developer feedback
        display.text_area("Please provide your input: ",
                          placeholder="Please enter your invaluable feedback here which is not connected to any database at all! \nBut you can always mail me at: bhushanbsongire@gmail.com")

        # result_box.form_submit_button("Submit Feedback")
        result_box.button("Submit Feedback")

    elif act_btn_analyze_ans:                       # analyze answers
        display.markdown("#### _Question Wise Result Analysis:_ ")
        for i in main_thing:                        # iterate ques
            q = main_thing[i]

            one = 0.2
            two = 1 - one
            color = 'grey'
            display.divider()

            sec_1, sec_2 = display.columns([one, two])
            sec_1.write(f":{color}[Que Number]")
            sec_2.write(f"{i}")

            sec_1, sec_2 = display.columns([one, two])
            sec_1.write(f":{color}[Question]")
            sec_2.write(f"{q['que']}")

            sec_1, sec_2 = display.columns([one, two])
            sec_1.write(f":{color}[Your Answer]")
            sec_2.write(f"{q['user']}")

            sec_1, sec_2 = display.columns([one, two])
            if (q['marks_obt'] == q['marks_max']):
                sec_2.success("Correct Answer !")
            elif (q['marks_obt'] <= q['marks_max']):
                sec_2.error("Incorrect / Partially Correct Answer !")

            sec_1, sec_2 = display.columns([one, two])
            sec_1.write(f":{color}[Correct Answer]")
            sec_2.write(f"{q['answer']}")

            sec_1, sec_2 = display.columns([one, two])
            sec_1.write(f":{color}[Answer Hint]")
            sec_2.write(f"{q['hint']}")

            sec_1, sec_2 = display.columns([one, two])
            sec_1.write(f":{color}[Your Score]")
            sec_2.write(f"{q['marks_obt']} / {q['marks_max']}")

        display.divider()
        display.latex(fr"""
                    \frac {{Obtained\ Marks}} {{Total\  Marks}}
                    =
                    \frac {{{marks_obtained}}} {{{marks_total}}}
                """)

        # result_box.form_submit_button("Thank You 🙏", disabled=True)

        a = result_box.download_button(
            label="Save Quiz ⬇️",
            data=json.dumps(main_thing),
            file_name="bbs_quiz.json",
            mime="application/json",
        )

        warn_text, _ = display.columns(2)
        warn_text.warning(" Please open one of the above sections!", icon="⚠️")

        # result_box.form_submit_button("Thank You 🙏", disabled=True)


# ======================================================================
# Certificate Generator:
# ======================================================================
if st.session_state.answer_checked:
    st.subheader(":orange[Certificate: ]", divider='grey')
    cert_btn = st.button("Generate Certificate", type='secondary')
    if cert_btn:
        st.session_state.certificate = True


if st.session_state.certificate:                    # certificate
    info_text, _ = st.columns(2)
    info_text.info(" This feature will be available soon!", icon="♾️")

# ======================================================================
# Debugging section of page:
# In deployment, set this variable as false
# while coding, can keep true
# ======================================================================
if (curr_page == pages[1]):

    st.header(":rainbow[Debugging Section] :bug::", divider="grey")

    st.subheader(":red[Config] :")
    st.write(st.session_state.quiz_config)

    st.subheader(":red[Questions] :")
    st.error(" Unauthorized!", icon="💥")

    st.subheader(":red[User solutions] :")
    st.error(" Unauthorized!", icon="💥")


# ======================================================================
# Bottom bar
# ======================================================================

# st.divider()
st.subheader("", divider='rainbow')
_, rights, __ = st.columns([3, 4, 3])
rights.text("©️ Bhushan Songire, Jul 2024")
