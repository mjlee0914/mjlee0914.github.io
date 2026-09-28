import streamlit as st
import pandas as pd

st.set_page_config(page_title="Streamlit 학습", layout="wide")
st.sidebar.title("📚 Streamlit 학습")
section = st.sidebar.radio("메뉴", ["주제별 학습", "종합실습"])

if section == "주제별 학습":
    st.title("주제별 학습")
    t0, t1, t2, t3, t4, t5 = st.tabs(['텍스트 출력', '데이터 표시', '버튼·선택 위젯', '입력·파일 위젯', '인터랙티브 차트', '상태·진행률'])

    with t0:
        st.title("st.title")
        st.header("st.header")
        st.subheader("st.subheader")

        st.write("st.write()")
        st.write("st.write method 안 변수 넣어서 출력 가능")

        st.text("st.text")

        st.markdown("st.markdown **bold** *italic*")

        code_block = '''
        def instruction():
            print("python code in a text variable")

        st.code(code_block, language="python")
        '''

        st.code(code_block, language="python")

        st.text('수학 공식 쓰기: st.latex(r"equation")')
        st.latex(r"E =mc^2")

        st.caption("st.caption()")



    with t1:
        st.title("My Data Dashboard")

        # 두 번째 섹션의 중간 제목을 출력합니다.
        st.header("1. 오늘의 핵심 지표")

        # 오늘의 총 방문자 수를 나타내는 요약표를 화면에 띄웁니다.
        # label은 제목, value는 현재 수치, delta는 어제보다 얼마나 늘었는지(변화량)를 나타냅니다.
        st.metric(label="오늘의 방문자 수", value="1,250명", delta="120명")

        # 팁: delta 값에 마이너스(-)를 붙이면 자동으로 빨간색 하락 화살표가 표시됩니다.
        st.metric(label="이번 달 지출", value="450,000원", delta="-50,000원")

        # 세 번째 섹션의 중간 제목을 출력합니다.
        st.header("2. 스크롤이 가능한 데이터프레임")
        st.subheader("st.dataframe(df)")
        st.text("상하좌우 스크롤 o, 동적 데이터 프레임")

        # 파이썬 딕셔너리 형태로 학생들의 성적 데이터를 만듭니다.
        data = {
            "이름": ["김철수", "이영희", "박지민", "최동훈", "정수진"],
            "점수": [85, 92, 78, 88, 95],
            "합격여부": ["Pass", "Pass", "Fail", "Pass", "Pass"]
        }

        # 딕셔너리 데이터를 판다스의 표(DataFrame) 형태로 변환하여 df 변수에 저장합니다.
        df = pd.DataFrame(data)

        # 데이터프레임(df)을 스크롤과 정렬이 가능한 스마트한 표 형태로 화면에 출력합니다.
        st.dataframe(df)

        # 네 번째 섹션의 중간 제목을 출력합니다.
        st.header("3. 한눈에 보는 정적 테이블")
        st.subheader("st.table(df)")
        st.text("스크롤 x -> 데이터 양이 적을 때 유용")

        # 위에서 만든 df 데이터를 이번에는 스크롤이 없는 고정된 표 형태로 출력합니다.
        # 데이터가 적을 때는 한눈에 파악하기 훨씬 좋습니다.
        st.table(df)

        # 다섯 번째 섹션의 중간 제목을 출력합니다.
        st.header("4. 내 맘대로 수정하는 데이터 테이블")
        st.subheader("st.data_editor(df)")

        # 앞서 만든 표(df)를 화면에 띄우되, 사용자가 클릭해서 수정할 수 있도록 만듭니다.
        # 수정된 전체 표 데이터는 edited_df 라는 새로운 변수에 저장됩니다.
        edited_df = st.data_editor(df)

        # 사용자가 값을 수정하면, 수정된 결과가 아래 문장과 함께 반영됩니다.
        st.write("위 표의 값을 클릭하여 자유롭게 수정 가능")

        # 여섯 번째 섹션의 중간 제목을 출력합니다.
        st.header("5. 데이터 원본 구조 확인 (JSON)")
        st.text("데이터 검증시 사용")
        # 딕셔너리 데이터(data)를 JSON 형태의 계층 구조로 화면에 예쁘게 출력합니다.
        # 화살표를 클릭해서 데이터를 접었다 펼칠 수 있습니다.
        st.json(data)


    with t2:
        st.title("버튼과 선택 위젯 실습하기")

        st.header("1. 기본 버튼")

        # '클릭해 보세요!'라는 이름의 버튼을 화면에 만듭니다.
        # 사용자가 이 버튼을 누르면 버튼의 상태가 잠시 '참(True)'이 됩니다.
        if st.button("click"):
            # 버튼이 눌렸을 때만 아래 축하 메시지가 화면에 나타납니다.
            st.write("clicked!")

        button_code = '''
        # 'click'이라는 이름의 버튼 만들기
        # 사용자가 이 버튼을 누르면 버튼의 상태가 잠시 '참(True)'이 됨.
        if st.button("click"):
            # 버튼이 눌렸을 때만 아래 메시지가 화면에 나타남.
            st.write("clicked!")
        '''

        st.code(button_code, language="python")

        st.header("2. 다운로드 버튼")

        # 다운로드할 텍스트 데이터를 문자열 변수에 미리 저장합니다.
        my_text = "file_content"

        # 다운로드 버튼을 만들고, 버튼 이름, 들어갈 데이터, 저장될 파일명을 설정합니다.
        st.download_button(
            label="download doc",
            data=my_text,
            file_name="sample.txt"
        )

        download_code = '''
        # 다운로드할 텍스트 데이터를 문자열 변수에 미리 저장합니다.
        my_text = "file_content"

        # 다운로드 버튼을 만들고, 버튼 이름, 들어갈 데이터, 저장될 파일명을 설정합니다.
        st.download_button(
            label="download doc",
            data=my_text,
            file_name="sample.txt"
        )
        '''
        st.code(download_code, language="python")

        st.header("3. 단일 선택 위젯")

        # '개인정보 수집에 동의하십니까?'라는 체크박스를 만듭니다.
        # 사용자가 마우스로 체크하면 agree 변수에 참(True) 값이 저장됩니다.
        agree = st.checkbox("개인정보 수집에 동의하십니까?")

        # 만약 체크박스에 체크가 되었다면(True 상태라면) 아래 메시지를 보여줍니다.
        if agree:
            st.write("동의해 주셔서 감사합니다!")

        checkbox_code = '''
        # '개인정보 수집에 동의하십니까?'라는 체크박스를 만듭니다.
        # 사용자가 마우스로 체크하면 agree 변수에 참(True) 값이 저장됩니다.
        agree = st.checkbox("개인정보 수집에 동의하십니까?")

        # 만약 체크박스에 체크가 되었다면(True 상태라면) 아래 메시지를 보여줍니다.
        if agree:
            st.write("동의해 주셔서 감사합니다!")
        '''

        st.code(checkbox_code, language="python")

        # 라디오 버튼을 만들고, 선택할 수 있는 항목을 리스트(대괄호)로 넣어줍니다.
        # 사용자가 선택한 항목의 이름 글자가 choice 변수에 그대로 저장됩니다.
        choice = st.radio(
            "가장 좋아하는 과목을 선택하세요.",
            ["프로그래밍", "데이터 분석", "웹 디자인"]
        )

        # 선택된 과목 이름을 안내 문장과 합쳐서 화면에 출력합니다.
        st.write("당신의 선택은: " + choice + " 입니다.")

        radio_code = '''
        # 라디오 버튼을 만들고, 선택할 수 있는 항목을 리스트(대괄호)로 넣어줍니다.
        # 사용자가 선택한 항목의 이름 글자가 choice 변수에 그대로 저장됩니다.
        choice = st.radio(
            "가장 좋아하는 과목을 선택하세요.",
            ["프로그래밍", "데이터 분석", "웹 디자인"]
        )

        # 선택된 과목 이름을 안내 문장과 합쳐서 화면에 출력합니다.
        st.write("당신의 선택은: " + choice + " 입니다.")
        '''

        st.code(radio_code, language="python")

        # 셀렉트박스를 만들고, 선택지를 리스트로 제공합니다.
        # 기본적으로는 첫 번째 항목이 선택되어 접혀 있고, 클릭하면 전체 선택지가 보입니다.
        major = st.selectbox(
            "소속 학과를 선택해 주세요.",
            ["경영학과", "경제학과", "컴퓨터공학과", "심리학과"]
        )

        # 최종적으로 선택한 학과를 화면에 텍스트로 보여줍니다.
        st.write("선택된 학과: " + major)

        select_code = '''
        # 셀렉트박스를 만들고, 선택지를 리스트로 제공합니다.
        # 기본적으로는 첫 번째 항목이 선택되어 접혀 있고, 클릭하면 전체 선택지가 보입니다.
        major = st.selectbox(
            "소속 학과를 선택해 주세요.",
            ["경영학과", "경제학과", "컴퓨터공학과", "심리학과"]
        )

        # 최종적으로 선택한 학과를 화면에 텍스트로 보여줍니다.
        st.write("선택된 학과: " + major)
        '''
        st.code(select_code, language="python")


        st.header("4. 다중 선택과 스위치")

        # 멀티셀렉트 박스를 만들고 4개의 관심사 선택지를 줍니다.
        # 사용자가 선택한 여러 개의 항목이 묶여서 hobbies 변수에 저장됩니다.
        hobbies = st.multiselect(
            "관심 있는 분야를 모두 골라주세요.",
            ["음악 감상", "독서", "게임", "운동"]
        )

        # 선택된 관심사 목록 전체를 화면에 출력하여 확인합니다.
        st.write("선택한 관심사 목록:", hobbies)

        multi_code = '''
        # 멀티셀렉트 박스를 만들고 4개의 관심사 선택지를 줍니다.
        # 사용자가 선택한 여러 개의 항목이 묶여서 hobbies 변수에 저장됩니다.
        hobbies = st.multiselect(
            "관심 있는 분야를 모두 골라주세요.",
            ["음악 감상", "독서", "게임", "운동"]
        )

        # 선택된 관심사 목록 전체를 화면에 출력하여 확인합니다.
        st.write("선택한 관심사 목록:", hobbies)
        '''

        st.code(multi_code, language="python")

        # '야간 모드 켜기'라는 이름의 토글 스위치를 만듭니다.
        # 스위치를 오른쪽으로 켜면 on 변수에 참(True)이 저장됩니다.
        on = st.toggle("야간 모드 켜기")

        # 스위치가 켜졌을 때만 아래 메시지가 화면에 출력됩니다.
        if on:
            st.write("🌙 야간 모드가 활성화되었습니다.")

        toggle_code = '''
        # '야간 모드 켜기'라는 이름의 토글 스위치를 만듭니다.
        # 스위치를 오른쪽으로 켜면 on 변수에 참(True)이 저장됩니다.
        on = st.toggle("야간 모드 켜기")

        # 스위치가 켜졌을 때만 아래 메시지가 화면에 출력됩니다.
        if on:
            st.write("🌙 야간 모드가 활성화되었습니다.")
        '''

        st.code(toggle_code, language="python")



    with t3:
        st.title("다양한 입력 위젯 실습하기")
        st.header("1. 텍스트 입력받기")

        # 사용자에게 이름을 입력받는 한 줄짜리 입력 창을 만듭니다.
        # 사용자가 키보드로 친 글자가 name 변수에 쏙 들어갑니다.
        name = st.text_input("당신의 이름을 입력해 주세요.")

        # name 변수에 값이 들어있다면(사용자가 이름을 입력했다면) 아래 문장을 출력합니다.
        if name:
            st.write(f"반갑습니다, {name}님! 오늘 하루도 파이팅하세요.")

        input_code = '''
        # 사용자에게 이름을 입력받는 한 줄짜리 입력 창을 만듭니다.
        # 사용자가 키보드로 친 글자가 name 변수에 쏙 들어갑니다.
        name = st.text_input("당신의 이름을 입력해 주세요.")

        # name 변수에 값이 들어있다면(사용자가 이름을 입력했다면) 아래 문장을 출력합니다.
        if name:
            st.write(f"반갑습니다, {name}님! 오늘 하루도 파이팅하세요.")
        '''

        st.code(input_code, language="python")

        # 여러 줄의 긴 글을 입력받는 텍스트 공간을 만듭니다.
        # 입력 칸 안에 연하게 보일 힌트 글(placeholder)을 미리 적어둘 수 있습니다.
        feedback = st.text_area(
            "우리 서비스에 대한 의견을 자유롭게 남겨주세요.", 
            placeholder="여기에 내용을 입력하세요..."
        )

        # 입력된 내용이 있다면 화면에 다시 출력해서 확인시켜 줍니다.
        if feedback:
            st.write("소중한 의견 감사합니다. 입력하신 내용은 다음과 같습니다:")
            st.write(feedback)

        text_area_code = '''
        # 여러 줄의 긴 글을 입력받는 텍스트 공간을 만듭니다.
        # 입력 칸 안에 연하게 보일 힌트 글(placeholder)을 미리 적어둘 수 있습니다.
        feedback = st.text_area(
            "우리 서비스에 대한 의견을 자유롭게 남겨주세요.", 
            placeholder="여기에 내용을 입력하세요..."
        )

        # 입력된 내용이 있다면 화면에 다시 출력해서 확인시켜 줍니다.
        if feedback:
            st.write("소중한 의견 감사합니다. 입력하신 내용은 다음과 같습니다:")
            st.write(feedback)
        '''

        st.code(text_area_code, language="python")

        st.header("2. 숫자와 범위 입력받기")

        # 숫자를 입력받는 창을 만듭니다.
        # min_value(최솟값), max_value(최댓값), step(한 번에 커지는 단위)을 설정할 수 있습니다.
        age = st.number_input(
            "당신의 나이는 몇 살인가요?", 
            min_value=0,   # 0살보다 작게 내려갈 수 없습니다.
            max_value=120, # 120살보다 높게 올라갈 수 없습니다.
            step=1         # 버튼을 누를 때마다 1씩 바뀝니다.
        )

        st.write(f"입력하신 나이는 {age}세 입니다.")

        num_input_code = '''
        # 숫자를 입력받는 창을 만듭니다.
        # min_value(최솟값), max_value(최댓값), step(한 번에 커지는 단위)을 설정할 수 있습니다.
        age = st.number_input(
            "당신의 나이는 몇 살인가요?", 
            min_value=0,   # 0살보다 작게 내려갈 수 없습니다.
            max_value=120, # 120살보다 높게 올라갈 수 없습니다.
            step=1         # 버튼을 누를 때마다 1씩 바뀝니다.
        )

        st.write(f"입력하신 나이는 {age}세 입니다.")
        '''

        st.code(num_input_code, language="python")


        # 0부터 100 사이의 숫자를 막대를 끌어서 선택하도록 만듭니다.
        # 맨 끝에 있는 50은 화면이 처음 켜졌을 때 슬라이더가 위치할 '기본값'입니다.
        volume = st.slider("스피커 볼륨을 조절하세요.", 0, 100, 50)

        st.write(f"현재 볼륨은 {volume}%로 설정되었습니다.")


        slider_code = '''
        # 0부터 100 사이의 숫자를 막대를 끌어서 선택하도록 만듭니다.
        # 맨 끝에 있는 50은 화면이 처음 켜졌을 때 슬라이더가 위치할 '기본값'입니다.
        volume = st.slider("스피커 볼륨을 조절하세요.", 0, 100, 50)

        st.write(f"현재 볼륨은 {volume}%로 설정되었습니다.")
        '''

        st.code(slider_code, language="python")

        # 대괄호([]) 안에 우리가 원하는 단계들을 차례대로 적어줍니다.
        size = st.select_slider(
            "원하는 커피 사이즈를 선택하세요.",
            options=["Small", "Medium", "Large", "Venti"]
        )

        st.write(f"선택하신 음료 사이즈는 {size}입니다.")

        select_slider_code = '''
        # 대괄호([]) 안에 우리가 원하는 단계들을 차례대로 적어줍니다.
        size = st.select_slider(
            "원하는 커피 사이즈를 선택하세요.",
            options=["Small", "Medium", "Large", "Venti"]
        )

        st.write(f"선택하신 음료 사이즈는 {size}입니다.")
        '''
        st.code(select_slider_code, language="python")


        # 날짜 기능을 사용하기 위해 파이썬에 기본으로 있는 datetime을 불러옵니다.
        import datetime

        st.header("3. 날짜와 시간 예약하기")

        # 달력 위젯을 화면에 띄웁니다.
        # 기본값으로 오늘 날짜(datetime.date.today())가 선택되어 있도록 합니다.
        reservation_date = st.date_input(
            "식당 방문 날짜를 선택해 주세요.",
            datetime.date.today()
        )

        st.write(f"예약 날짜: {reservation_date}")

        date_code = '''
        # 날짜 기능을 사용하기 위해 파이썬에 기본으로 있는 datetime을 불러옵니다.
        import datetime

        st.header("3. 날짜와 시간 예약하기")

        # 달력 위젯을 화면에 띄웁니다.
        # 기본값으로 오늘 날짜(datetime.date.today())가 선택되어 있도록 합니다.
        reservation_date = st.date_input(
            "식당 방문 날짜를 선택해 주세요.",
            datetime.date.today()
        )

        st.write(f"예약 날짜: {reservation_date}")
        '''

        st.code(date_code, language="python")

        # 시간 선택 창을 화면에 띄웁니다.
        # 기본적으로 현재 시간이 표시되거나 직접 설정할 수 있습니다.
        # 여기서는 기본값으로 19시 00분(저녁 7시)을 세팅해 둡니다.
        reservation_time = st.time_input(
            "방문하실 시간을 선택해 주세요.",
            datetime.time(19, 0) # 19시 0분
        )

        st.write(f"예약 시간: {reservation_time}")

        time_code = '''
        # 시간 선택 창을 화면에 띄웁니다.
        # 기본적으로 현재 시간이 표시되거나 직접 설정할 수 있습니다.
        # 여기서는 기본값으로 19시 00분(저녁 7시)을 세팅해 둡니다.
        reservation_time = st.time_input(
            "방문하실 시간을 선택해 주세요.",
            datetime.time(19, 0) # 19시 0분
        )

        st.write(f"예약 시간: {reservation_time}")
        '''

        st.code(time_code, language="python")


        st.header("1. 파일 업로드 위젯 실습")

        # 파일을 업로드할 수 있는 공간을 만듭니다.
        # type=['png', 'jpg']를 적어주면 이미지 파일만 선택하도록 제한합니다.
        uploaded_file = st.file_uploader("프로필 사진을 업로드해 주세요.", type=['png', 'jpg'])

        # 사용자가 파일을 정상적으로 업로드했다면 아래 코드를 실행합니다.
        if uploaded_file is not None:
            # 성공했다는 안내 메시지를 띄웁니다.
            st.success("파일 업로드가 완료되었습니다.")
    
            # 업로드받은 이미지 파일을 화면에 보여줍니다.
            st.image(uploaded_file)

        upload_code = '''
        # 파일을 업로드할 수 있는 공간을 만듭니다.
        # type=['png', 'jpg']를 적어주면 이미지 파일만 선택하도록 제한합니다.
        uploaded_file = st.file_uploader("프로필 사진을 업로드해 주세요.", type=['png', 'jpg'])

        # 사용자가 파일을 정상적으로 업로드했다면 아래 코드를 실행합니다.
        if uploaded_file is not None:
            # 성공했다는 안내 메시지를 띄웁니다.
            st.success("파일 업로드가 완료되었습니다.")
    
            # 업로드받은 이미지 파일을 화면에 보여줍니다.
            st.image(uploaded_file)
        '''

        st.code(upload_code, language="python")

        st.subheader("2.1 카메라로 사진 찍기")

        # 카메라 뷰파인더를 화면에 띄우고 촬영된 사진을 변수에 저장합니다.
        picture = st.camera_input("웹캠으로 사진을 찍어보세요.")

        # 사용자가 사진을 찰칵 찍었다면 아래 코드를 실행합니다.
        if picture is not None:
            # 찍힌 사진을 화면에 출력하여 확인시켜 줍니다.
            st.image(picture)

        camera_code = '''
        # 카메라 뷰파인더를 화면에 띄우고 촬영된 사진을 변수에 저장합니다.
        picture = st.camera_input("웹캠으로 사진을 찍어보세요.")

        # 사용자가 사진을 찰칵 찍었다면 아래 코드를 실행합니다.
        if picture is not None:
            # 찍힌 사진을 화면에 출력하여 확인시켜 줍니다.
            st.image(picture)
        '''
        st.code(camera_code, language="python")

        st.subheader("2.2 목소리 녹음하기")

        # 마이크를 켜서 녹음할 수 있는 위젯을 띄웁니다.
        audio_data = st.audio_input("여기를 눌러 목소리를 남겨주세요.")

        # 사용자가 녹음을 완료했다면 아래 코드를 실행합니다.
        if audio_data is not None:
            # 녹음된 파일을 재생할 수 있는 오디오 플레이어를 화면에 만듭니다.
            st.audio(audio_data)

        audio_code  = '''
        # 마이크를 켜서 녹음할 수 있는 위젯을 띄웁니다.
        audio_data = st.audio_input("여기를 눌러 목소리를 남겨주세요.")

        # 사용자가 녹음을 완료했다면 아래 코드를 실행합니다.
        if audio_data is not None:
            # 녹음된 파일을 재생할 수 있는 오디오 플레이어를 화면에 만듭니다.
            st.audio(audio_data)
        '''

        st.code(audio_code, language="python")

        st.subheader("2.3 테마 색상 고르기")

        # 색상표를 띄우고 기본값으로 파란색(#00f900)을 설정해 둡니다.
        color = st.color_picker("가장 좋아하는 색상을 골라주세요.", "#00f900")

        # 사용자가 고른 색상의 코드를 화면에 글자로 출력합니다.
        st.write("선택하신 색상의 코드는 다음과 같습니다:", color)

        color_code = '''
        # 색상표를 띄우고 기본값으로 파란색(#00f900)을 설정해 둡니다.
        color = st.color_picker("가장 좋아하는 색상을 골라주세요.", "#00f900")

        # 사용자가 고른 색상의 코드를 화면에 글자로 출력합니다.
        st.write("선택하신 색상의 코드는 다음과 같습니다:", color)
        '''

        st.code(color_code, language="python")

        # 데이터 표를 다루기 위해 pandas 도구를 불러옵니다.

    with t4:
        import streamlit as st
        import matplotlib.pyplot as plt
        import plotly.express as px
        import pandas as pd

        st.title("나의 첫 인터랙티브 대시보드")

        # --- 데이터 준비 영역 ---
        # 부서별 예산 데이터를 표(데이터프레임)로 만듭니다.
        budget_data = pd.DataFrame({
            'department': ['marketing', 'development', 'design', 'sales'],
            'budget': [500, 1200, 800, 600]
        })

        # --- 첫 번째 차트: Matplotlib (정적) ---
        st.subheader("1. 부서별 예산 비율 (Matplotlib)")

        # 스케치북을 만들고 파이 차트를 그립니다.
        fig1, ax1 = plt.subplots()
        ax1.pie(budget_data['budget'], labels=budget_data['department'], autopct='%1.1f%%', startangle=90)

        # 완성된 파이 차트를 화면에 출력합니다.
        st.pyplot(fig1)

        # --- 두 번째 차트: Plotly (동적) ---
        st.subheader("2. 부서별 예산 상세 (Plotly)")
        st.write("막대그래프 위에 마우스를 올려보세요!")

        # 동적인 막대그래프를 생성합니다.
        fig2 = px.bar(budget_data, x='department', y='budget', color='department')

        # 완성된 동적 그래프를 화면에 출력합니다.
        st.plotly_chart(fig2)

        st.success("화려한 대시보드 생성이 완료되었습니다!")

        plotly_code = '''
        import streamlit as st
        import matplotlib.pyplot as plt
        import plotly.express as px
        import pandas as pd

        st.title("나의 첫 인터랙티브 대시보드")

        # --- 데이터 준비 영역 ---
        # 부서별 예산 데이터를 표(데이터프레임)로 만듭니다.
        budget_data = pd.DataFrame({
            'department': ['marketing', 'development', 'design', 'sales'],
            'budget': [500, 1200, 800, 600]
        })

        # --- 첫 번째 차트: Matplotlib (정적) ---
        st.subheader("1. 부서별 예산 비율 (Matplotlib)")

        # 스케치북을 만들고 파이 차트를 그립니다.
        fig1, ax1 = plt.subplots()
        ax1.pie(budget_data['budget'], labels=budget_data['department'], autopct='%1.1f%%', startangle=90)

        # 완성된 파이 차트를 화면에 출력합니다.
        st.pyplot(fig1)

        # --- 두 번째 차트: Plotly (동적) ---
        st.subheader("2. 부서별 예산 상세 (Plotly)")
        st.write("막대그래프 위에 마우스를 올려보세요!")

        # 동적인 막대그래프를 생성합니다.
        fig2 = px.bar(budget_data, x='department', y='budget', color='department')

        # 완성된 동적 그래프를 화면에 출력합니다.
        st.plotly_chart(fig2)

        st.success("화려한 대시보드 생성이 완료되었습니다!")
        '''
        st.code(plotly_code, language="python")


    with t5:
        import time
        import streamlit as st

        # 메인 화면의 큰 제목을 설정합니다.
        st.title("AI 데이터 자동 분석기")

        # 버튼을 눌러 작업을 시작하도록 설정합니다.
        if st.button("데이터 분석 시작하기"):
    
            # 작업 상태를 상세히 보여주는 상자를 만듭니다.
            with st.status("분석 파이프라인 가동 중...", expanded=True) as status:
        
                # 1단계: 텍스트 문구로 현재 작업을 안내합니다.
                st.write("1단계: 원본 데이터를 서버에서 다운로드합니다.")
                # 다운로드가 진행되는 시간을 흉내 냅니다.
                time.sleep(1.5)
        
                # 2단계: 문구를 출력하고 진행 바를 만들어 보여줍니다.
                st.write("2단계: AI 모델을 활용해 데이터를 분석합니다.")
                # 진행 바를 0 상태로 만듭니다.
                progress_bar = st.progress(0)
        
                # 진행 바를 1부터 100까지 채워 나갑니다.
                for i in range(1, 101):
                    # 순식간에 차지 않도록 아주 조금씩 지연시킵니다.
                    time.sleep(0.01)
                    # 진행 바의 수치를 i로 업데이트합니다.
                    progress_bar.progress(i)
            
                # 3단계: 문구를 출력합니다.
                st.write("3단계: 결과를 정리하여 표를 만듭니다.")
                time.sleep(1)
        
                # 모든 작업이 끝나면 상태 상자의 제목을 바꾸고 상자를 닫습니다.
                status.update(label="모든 분석이 성공적으로 끝났습니다!", state="complete", expanded=False)
        
            # 상태 상자 바깥으로 나와서 완료 알림과 효과를 실행합니다.
            # 화면 구석에 작은 완료 메시지를 띄웁니다.
            st.toast("리포트 생성이 완료되었습니다!", icon="🎉")
            # 화면 전체에 축하 풍선을 띄웁니다.
            st.balloons()

        status_code = '''
        import time
        import streamlit as st

        # 메인 화면의 큰 제목을 설정합니다.
        st.title("AI 데이터 자동 분석기")

        # 버튼을 눌러 작업을 시작하도록 설정합니다.
        if st.button("데이터 분석 시작하기"):
    
            # 작업 상태를 상세히 보여주는 상자를 만듭니다.
            with st.status("분석 파이프라인 가동 중...", expanded=True) as status:
        
                # 1단계: 텍스트 문구로 현재 작업을 안내합니다.
                st.write("1단계: 원본 데이터를 서버에서 다운로드합니다.")
                # 다운로드가 진행되는 시간을 흉내 냅니다.
                time.sleep(1.5)
        
                # 2단계: 문구를 출력하고 진행 바를 만들어 보여줍니다.
                st.write("2단계: AI 모델을 활용해 데이터를 분석합니다.")
                # 진행 바를 0 상태로 만듭니다.
                progress_bar = st.progress(0)
        
                # 진행 바를 1부터 100까지 채워 나갑니다.
                for i in range(1, 101):
                    # 순식간에 차지 않도록 아주 조금씩 지연시킵니다.
                    time.sleep(0.01)
                    # 진행 바의 수치를 i로 업데이트합니다.
                    progress_bar.progress(i)
            
                # 3단계: 문구를 출력합니다.
                st.write("3단계: 결과를 정리하여 표를 만듭니다.")
                time.sleep(1)
        
                # 모든 작업이 끝나면 상태 상자의 제목을 바꾸고 상자를 닫습니다.
                status.update(label="모든 분석이 성공적으로 끝났습니다!", state="complete", expanded=False)
        
            # 상태 상자 바깥으로 나와서 완료 알림과 효과를 실행합니다.
            # 화면 구석에 작은 완료 메시지를 띄웁니다.
            st.toast("리포트 생성이 완료되었습니다!", icon="🎉")
            # 화면 전체에 축하 풍선을 띄웁니다.
            st.balloons()
        '''

else:
    st.title("종합실습")
    t0, t1, t2, t3, t4, t5, t6, t7 = st.tabs(['맞춤형 데이터 뷰어', '대출 이자 계산기·상담 예약 폼', 'CSV 리포트 생성기', '나의 첫 데이터 대시보드', '종합 미디어 대시보드', '오늘의 추천 메뉴', '캠퍼스 동아리 안내', '중앙 도서관 서비스 안내'])

    with t0:
        with st.expander('맞춤형 데이터 뷰어 실습 내용', expanded=True):
            # 종합 실습을 위한 제목을 화면에 출력합니다.
            st.header("5. [종합 실습] 맞춤형 데이터 뷰어")

            # 파이썬 딕셔너리 문법을 사용해 과일 재고 데이터를 만듭니다.
            data = {
                "과일명": ["사과", "사과", "바나나", "바나나", "포도"],
                "등급": ["A", "B", "A", "B", "A"],
                "가격": [5000, 3000, 4000, 2500, 7000]
            }

            # 딕셔너리 데이터를 판다스의 표(DataFrame) 형태로 변환합니다.
            df = pd.DataFrame(data)

            # 사용자에게 셀렉트박스를 보여주고 과일 하나를 고르도록 합니다.
            selected_fruit = st.selectbox(
                "어떤 과일의 재고를 확인하시겠어요?",
                ["사과", "바나나", "포도"]
            )

            # 전체 데이터(df) 중에서 '과일명' 열이 사용자가 선택한 과일과 똑같은 줄만 걸러냅니다.
            # 이것을 '데이터 필터링'이라고 부릅니다.
            filtered_df = df[df["과일명"] == selected_fruit]

            # 걸러진 데이터를 지난 시간에 배운 동적인 데이터프레임으로 화면에 출력합니다.
            st.write(f"선택하신 {selected_fruit}의 데이터입니다:")
            st.dataframe(filtered_df)

            practice_code = '''
            # 파이썬 딕셔너리 문법을 사용해 과일 재고 데이터를 만듭니다.
            data = {
                "과일명": ["사과", "사과", "바나나", "바나나", "포도"],
                "등급": ["A", "B", "A", "B", "A"],
                "가격": [5000, 3000, 4000, 2500, 7000]
            }

            # 딕셔너리 데이터를 판다스의 표(DataFrame) 형태로 변환합니다.
            df = pd.DataFrame(data)

            # 사용자에게 셀렉트박스를 보여주고 과일 하나를 고르도록 합니다.
            selected_fruit = st.selectbox(
                "어떤 과일의 재고를 확인하시겠어요?",
                ["사과", "바나나", "포도"]
            )

            # 전체 데이터(df) 중에서 '과일명' 열이 사용자가 선택한 과일과 똑같은 줄만 걸러냅니다.
            # 이것을 '데이터 필터링'이라고 부릅니다.
            filtered_df = df[df["과일명"] == selected_fruit]

            # 걸러진 데이터를 지난 시간에 배운 동적인 데이터프레임으로 화면에 출력합니다.
            st.write(f"선택하신 {selected_fruit}의 데이터입니다:")
            st.dataframe(filtered_df)
            '''

            st.code(practice_code, language="python")



    with t1:
        with st.expander('대출 이자 계산기·상담 예약 폼 실습 내용', expanded=True):

            st.header("4. [종합 실습] 실시간 대출 이자 계산기")

            # 대출 금액을 숫자 입력창으로 받습니다. (100만원 단위로 증감)
            principal = st.number_input("대출 원금을 입력하세요 (원)", min_value=0, step=1000000)

            # 이자율을 슬라이더로 직관적으로 받습니다. (1% ~ 20% 사이)
            interest_rate = st.slider("연 이자율을 선택하세요 (%)", 1.0, 20.0, 5.0)

            # 대출 기간을 숫자 입력창으로 받습니다. (최대 30년)
            years = st.number_input("대출 기간을 입력하세요 (년)", min_value=1, max_value=30, step=1)

            # 계산 로직: 대출 원금 * (이자율 / 100) * 기간
            # 수학 계산 결과를 total_interest 변수에 저장합니다.
            total_interest = principal * (interest_rate / 100) * years

            # 버튼을 누르면 최종 계산 결과를 보여줍니다.
            if st.button("이자 계산하기"):
                st.write(f"총 발생 이자는 **{int(total_interest):,}원** 입니다.")
                st.write(f"원금과 이자를 합친 총 상환 금액은 **{int(principal + total_interest):,}원** 입니다.")

            # ---------------------------------------------------------
            st.divider() # 화면을 가로지르는 구분선을 하나 그어줍니다.
            st.header("상담 예약 폼")

            # 이름, 날짜, 시간을 복합적으로 입력받습니다.
            client_name = st.text_input("상담자 성함")
            meet_date = st.date_input("상담 희망 날짜")
            meet_time = st.time_input("상담 희망 시간")

            # 입력이 모두 완료되었을 때만 예약 완료 메시지를 띄우는 조건문입니다.
            if st.button("예약 확정하기"):
                if client_name: # 이름이 비어있지 않다면
                    st.write(f"{client_name}님, {meet_date} {meet_time}에 상담 예약이 완료되었습니다.")
                else:
                    st.write("성함을 입력해 주세요!")

            practice2_code = '''
            # 대출 금액을 숫자 입력창으로 받습니다. (100만원 단위로 증감)
            principal = st.number_input("대출 원금을 입력하세요 (원)", min_value=0, step=1000000)

            # 이자율을 슬라이더로 직관적으로 받습니다. (1% ~ 20% 사이)
            interest_rate = st.slider("연 이자율을 선택하세요 (%)", 1.0, 20.0, 5.0)

            # 대출 기간을 숫자 입력창으로 받습니다. (최대 30년)
            years = st.number_input("대출 기간을 입력하세요 (년)", min_value=1, max_value=30, step=1)

            # 계산 로직: 대출 원금 * (이자율 / 100) * 기간
            # 수학 계산 결과를 total_interest 변수에 저장합니다.
            total_interest = principal * (interest_rate / 100) * years

            # 버튼을 누르면 최종 계산 결과를 보여줍니다.
            if st.button("이자 계산하기"):
                st.write(f"총 발생 이자는 **{int(total_interest):,}원** 입니다.")
                st.write(f"원금과 이자를 합친 총 상환 금액은 **{int(principal + total_interest):,}원** 입니다.")

            # ---------------------------------------------------------
            st.divider() # 화면을 가로지르는 구분선을 하나 그어줍니다.
            st.header("상담 예약 폼")

            # 이름, 날짜, 시간을 복합적으로 입력받습니다.
            client_name = st.text_input("상담자 성함")
            meet_date = st.date_input("상담 희망 날짜")
            meet_time = st.time_input("상담 희망 시간")

            # 입력이 모두 완료되었을 때만 예약 완료 메시지를 띄우는 조건문입니다.
            if st.button("예약 확정하기"):
                if client_name: # 이름이 비어있지 않다면
                    st.write(f"{client_name}님, {meet_date} {meet_time}에 상담 예약이 완료되었습니다.")
                else:
                    st.write("성함을 입력해 주세요!")
            '''

            st.code(practice2_code, language="python")

    with t2:
        with st.expander('CSV 리포트 생성기 실습 내용', expanded=True):
            # 실습의 큰 제목을 작성합니다.
            st.header("3. [종합 실습] CSV 리포트 생성기")

            # 이번에는 CSV 파일만 업로드할 수 있도록 제한한 위젯을 만듭니다.
            csv_file = st.file_uploader("분석할 CSV 데이터 파일을 올려주세요.", type=['csv'])

            # 사용자가 CSV 파일을 올렸다면 아래 코드를 실행합니다.
            if csv_file is not None:
                # pandas 도구를 이용해 업로드된 파일을 표 형태로 읽어옵니다.
                df = pd.read_csv(csv_file)
    
                # 데이터가 총 몇 줄인지 계산해서 화면에 출력합니다.
                st.write(f"이 데이터는 총 {len(df)}개의 행으로 이루어져 있습니다.")
    
                # 읽어온 데이터 표를 깔끔한 형태로 화면에 출력합니다.
                st.dataframe(df)

            practice3_code = '''
            # 데이터 표를 다루기 위해 pandas 도구를 불러옵니다.
            import pandas as pd
            import streamlit as st

            # 화면과 데이터를 나누는 구분선을 긋습니다.
            st.divider()

            # 실습의 큰 제목을 작성합니다.
            st.header("3. [종합 실습] CSV 리포트 생성기")

            # 이번에는 CSV 파일만 업로드할 수 있도록 제한한 위젯을 만듭니다.
            csv_file = st.file_uploader("분석할 CSV 데이터 파일을 올려주세요.", type=['csv'])

            # 사용자가 CSV 파일을 올렸다면 아래 코드를 실행합니다.
            if csv_file is not None:
                # pandas 도구를 이용해 업로드된 파일을 표 형태로 읽어옵니다.
                df = pd.read_csv(csv_file)
    
                # 데이터가 총 몇 줄인지 계산해서 화면에 출력합니다.
                st.write(f"이 데이터는 총 {len(df)}개의 행으로 이루어져 있습니다.")
    
                # 읽어온 데이터 표를 깔끔한 형태로 화면에 출력합니다.
                st.dataframe(df)
            '''
            st.code(practice3_code, language="python")


    with t3:
        with st.expander('나의 첫 데이터 대시보드 실습 내용', expanded=True):

            import streamlit as st
            import pandas as pd

            st.title("나의 첫 데이터 대시보드")

            st.header("1. 월별 방문자 수 추이")

            # 1월부터 5월까지의 방문자 수 데이터를 표로 만듭니다.
            visitor_data = pd.DataFrame({
                "방문자수": [150, 200, 180, 300, 250]
            })
            # 방문자 데이터를 선 차트로 그립니다.
            st.line_chart(visitor_data)

            st.header("2. 우리 동네 맛집 지도")
            # 맛집 2곳의 위치 데이터를 표로 만듭니다. (lat: 위도, lon: 경도)
            restaurant_data = pd.DataFrame({
                "lat": [37.4979, 37.5000],
                "lon": [127.0276, 127.0300]
            })
            # 맛집 데이터를 지도에 표시합니다.
            st.map(restaurant_data)

            # 성공적으로 화면을 그렸다는 알림창을 띄웁니다.
            st.success("대시보드 생성이 완료되었습니다!")

            chart_code = '''
            import streamlit as st
            import pandas as pd

            st.title("나의 첫 데이터 대시보드")

            st.header("1. 월별 방문자 수 추이")

            # 1월부터 5월까지의 방문자 수 데이터를 표로 만듭니다.
            visitor_data = pd.DataFrame({
                "방문자수": [150, 200, 180, 300, 250]
            })
            # 방문자 데이터를 선 차트로 그립니다.
            st.line_chart(visitor_data)

            st.header("2. 우리 동네 맛집 지도")
            # 맛집 2곳의 위치 데이터를 표로 만듭니다. (lat: 위도, lon: 경도)
            restaurant_data = pd.DataFrame({
                "lat": [37.4979, 37.5000],
                "lon": [127.0276, 127.0300]
            })
            # 맛집 데이터를 지도에 표시합니다.
            st.map(restaurant_data)

            # 성공적으로 화면을 그렸다는 알림창을 띄웁니다.
            st.success("대시보드 생성이 완료되었습니다!")
            '''
            st.code(chart_code, language="python")


    with t4:
        with st.expander('종합 미디어 대시보드 실습 내용', expanded=True):

            # 필요한 도구를 불러옵니다.
            import streamlit as st

            # 앱의 로고를 설정합니다. (좌측 상단 표시)
            st.logo("https://cdn-icons-png.flaticon.com/512/4200/4200129.png")

            # 메인 화면 제목과 안내선을 긋습니다.
            st.title("종합 미디어 대시보드")

            # 이미지 출력
            st.header("오늘의 사진")
            st.image(
                "https://images.unsplash.com/photo-1788987259255-b45d400dd40f?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHx0b3BpYy1mZWVkfDIyfGJrMGhQYXF1VmVFfHxlbnwwfHx8fHw%3D", 
                caption="The Bay Bridge in San Francisco", 
                use_container_width=True
            )

            st.divider()

            # 4. 비디오 및 오디오 출력
            st.header("멀티미디어 감상")
            st.write("아래 재생 버튼을 눌러 영상과 음악을 감상해보세요.")

            # 비디오 띄우기
            st.video("https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4")

            # 오디오 띄우기
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

            # 실행 성공 메시지를 띄웁니다.
            st.success("미디어 갤러리가 성공적으로 완성되었습니다!")

            media_code = '''
            # 필요한 도구를 불러옵니다.
            import streamlit as st

            # 앱의 로고를 설정합니다. (좌측 상단 표시)
            st.logo("https://cdn-icons-png.flaticon.com/512/4200/4200129.png")

            # 메인 화면 제목과 안내선을 긋습니다.
            st.title("종합 미디어 대시보드")

            # 이미지 출력
            st.header("오늘의 사진")
            st.image(
                "https://images.unsplash.com/photo-1788987259255-b45d400dd40f?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHx0b3BpYy1mZWVkfDIyfGJrMGhQYXF1VmVFfHxlbnwwfHx8fHw%3D", 
                caption="The Bay Bridge in San Francisco", 
                use_container_width=True
            )

            st.divider()

            # 4. 비디오 및 오디오 출력
            st.header("멀티미디어 감상")
            st.write("아래 재생 버튼을 눌러 영상과 음악을 감상해보세요.")

            # 비디오 띄우기
            st.video("https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4")

            # 오디오 띄우기
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

            # 실행 성공 메시지를 띄웁니다.
            st.success("미디어 갤러리가 성공적으로 완성되었습니다!")
            '''
            st.code(media_code, language="python")


    with t5:
        with st.expander('오늘의 추천 메뉴 실습 내용', expanded=True):

            import streamlit as st

            # 메인 화면의 넓이를 넓게(wide) 쓰도록 기본 설정을 잡습니다.

            # 사이드바(왼쪽 메뉴) 영역을 구성합니다.

            # 메인 화면 영역을 구성합니다.
            st.title("오늘의 추천 메뉴")
            st.divider()

            # 화면을 두 칸으로 나눕니다.
            col_left, col_right = st.columns(2)

            # 첫 번째 칸(왼쪽)에 투명 상자를 만들어 메뉴를 넣습니다.
            with col_left:
                box1 = st.container(border=True)
                with box1:
                    st.subheader("불고기 백반")
                    st.write("달콤하고 짭짤한 불고기와 정갈한 반찬")
                    st.button("주문하기", key="btn1") # 버튼이 여러 개일 땐 key로 구분합니다.

            # 두 번째 칸(오른쪽)에 투명 상자를 만들어 메뉴를 넣습니다.
            with col_right:
                box2 = st.container(border=True)
                with box2:
                    st.subheader("얼큰 짬뽕")
                    st.write("해물이 듬뿍 들어간 시원한 짬뽕 국물")
                    st.button("주문하기", key="btn2")

            container_code = '''
            import streamlit as st

            # 메인 화면의 넓이를 넓게(wide) 쓰도록 기본 설정을 잡습니다.

            # 사이드바(왼쪽 메뉴) 영역을 구성합니다.

            # 메인 화면 영역을 구성합니다.
            st.title("오늘의 추천 메뉴")
            st.divider()

            # 화면을 두 칸으로 나눕니다.
            col_left, col_right = st.columns(2)

            # 첫 번째 칸(왼쪽)에 투명 상자를 만들어 메뉴를 넣습니다.
            with col_left:
                box1 = st.container(border=True)
                with box1:
                    st.subheader("불고기 백반")
                    st.write("달콤하고 짭짤한 불고기와 정갈한 반찬")
                    st.button("주문하기", key="btn1") # 버튼이 여러 개일 땐 key로 구분합니다.

            # 두 번째 칸(오른쪽)에 투명 상자를 만들어 메뉴를 넣습니다.
            with col_right:
                box2 = st.container(border=True)
                with box2:
                    st.subheader("얼큰 짬뽕")
                    st.write("해물이 듬뿍 들어간 시원한 짬뽕 국물")
                    st.button("주문하기", key="btn2")
            '''
            st.code(container_code, language="python")


    with t6:
        with st.expander('캠퍼스 동아리 안내 실습 내용', expanded=True):

            import streamlit as st

            # 앱의 메인 제목을 출력합니다.
            st.title("캠퍼스 동아리 안내")

            # 크게 두 가지 탭으로 화면을 겹쳐서 나눕니다.
            tab_art, tab_sport = st.tabs(["공연/예술", "운동/스포츠"])

            # 첫 번째 탭(공연/예술) 영역을 꾸며봅니다.
            with tab_art:
                st.subheader("공연/예술 동아리 목록")
    
                # 지난 시간에 배운 화면 2칸 분할 기능입니다.
                col1, col2 = st.columns(2)
    
                # 왼쪽 칸(col1)에 내용을 넣습니다.
                with col1:
                    st.info("밴드 동아리 '사운드'")
                    # 세부 모집 요강은 익스팬더로 접어둡니다.
                    with st.expander("모집 요강 펼쳐보기"):
                        st.write("- 모집 분야: 보컬, 기타, 드럼")
                        st.write("- 연습 시간: 매주 목요일 저녁")
                        st.button("지원하기", key="band_btn")
            
                # 오른쪽 칸(col2)에 내용을 넣습니다.
                with col2:
                    st.success("연극 동아리 '막'")
                    # 공간 절약을 위해 여기도 익스팬더를 씁니다.
                    with st.expander("모집 요강 펼쳐보기"):
                        st.write("- 모집 분야: 배우, 연출, 조명")
                        st.write("- 연습 시간: 매주 수요일 저녁")
                        st.button("지원하기", key="act_btn")

            # 두 번째 탭(운동/스포츠) 영역을 꾸며봅니다.
            with tab_sport:
                st.subheader("스포츠 동아리 목록")
                st.write("농구, 축구, 테니스 등 다양한 스포츠 동아리가 있습니다.")
                # 간단한 안내 사항을 익스팬더에 넣어둡니다.
                with st.expander("가입 신청 방법"):
                    st.write("학생회관 3층 동아리 연합회 사무실에 직접 방문하여 서류를 제출하세요.")

            expander_code = '''
            import streamlit as st

            # 앱의 메인 제목을 출력합니다.
            st.title("캠퍼스 동아리 안내")

            # 크게 두 가지 탭으로 화면을 겹쳐서 나눕니다.
            tab_art, tab_sport = st.tabs(["공연/예술", "운동/스포츠"])

            # 첫 번째 탭(공연/예술) 영역을 꾸며봅니다.
            with tab_art:
                st.subheader("공연/예술 동아리 목록")
    
                # 지난 시간에 배운 화면 2칸 분할 기능입니다.
                col1, col2 = st.columns(2)
    
                # 왼쪽 칸(col1)에 내용을 넣습니다.
                with col1:
                    st.info("밴드 동아리 '사운드'")
                    # 세부 모집 요강은 익스팬더로 접어둡니다.
                    with st.expander("모집 요강 펼쳐보기"):
                        st.write("- 모집 분야: 보컬, 기타, 드럼")
                        st.write("- 연습 시간: 매주 목요일 저녁")
                        st.button("지원하기", key="band_btn")
            
                # 오른쪽 칸(col2)에 내용을 넣습니다.
                with col2:
                    st.success("연극 동아리 '막'")
                    # 공간 절약을 위해 여기도 익스팬더를 씁니다.
                    with st.expander("모집 요강 펼쳐보기"):
                        st.write("- 모집 분야: 배우, 연출, 조명")
                        st.write("- 연습 시간: 매주 수요일 저녁")
                        st.button("지원하기", key="act_btn")

            # 두 번째 탭(운동/스포츠) 영역을 꾸며봅니다.
            with tab_sport:
                st.subheader("스포츠 동아리 목록")
                st.write("농구, 축구, 테니스 등 다양한 스포츠 동아리가 있습니다.")
                # 간단한 안내 사항을 익스팬더에 넣어둡니다.
                with st.expander("가입 신청 방법"):
                    st.write("학생회관 3층 동아리 연합회 사무실에 직접 방문하여 서류를 제출하세요.")
            '''
            st.code(expander_code, language="python")


    with t7:
        with st.expander('중앙 도서관 서비스 안내 실습 내용', expanded=True):

            st.divider()

            import streamlit as st

            # 다이얼로그(팝업창) 전용 함수 만들기
            @st.dialog("도서관 이용 만족도 설문")
            def survey_dialog():
                st.write("더 나은 도서관을 위해 의견을 남겨주세요.")
    
                # 팝업창 안에서 폼(Form)을 열어 입력을 하나로 묶습니다.
                with st.form(key="survey_form"):
                    # 라디오 버튼으로 만족도를 선택하게 합니다.
                    score = st.radio("전반적인 만족도는 어떠신가요?", ["매우 만족", "보통", "불만족"])
                    # 긴 텍스트를 입력받는 칸을 만듭니다.
                    feedback = st.text_area("개선할 점을 자유롭게 적어주세요.")
        
                    # 폼 제출 버튼을 만듭니다.
                    submit = st.form_submit_button("설문 제출하기")
        
                # 제출 버튼이 눌렸다면,
                if submit:
                    # 감사 메시지를 띄우고
                    st.success("소중한 의견 감사합니다!")
                    # 2초 정도 메시지를 보여줄 시간을 주기 위해 잠시 멈추는 기능(추가 활용)이 들어갈 수 있지만,
                    # 여기서는 곧바로 창을 닫고 새로고침 하도록 합니다.
                    st.rerun()

            # 메인 화면 구성하기
            st.title("중앙 도서관 서비스 안내")
            st.write("환영합니다. 원하는 메뉴를 선택해주세요.")

            # 팝오버를 활용해 화면 한구석에 작은 필터/설정 창을 만듭니다.
            with st.popover("⚙️ 화면 설정"):
                st.toggle("다크 모드 적용")
                st.toggle("알림 켜기")

            # 거리를 살짝 띄워줍니다.
            st.divider()

            # 메인 화면에서 설문조사 버튼을 만듭니다.
            st.info("현재 도서관 이용 만족도 설문조사가 진행 중입니다.")
            if st.button("설문조사 참여하기"):
                # 버튼을 누르면 위에서 만든 팝업창 함수를 실행합니다.
                survey_dialog()

            pop_code = '''
            import streamlit as st

            # 다이얼로그(팝업창) 전용 함수 만들기
            @st.dialog("도서관 이용 만족도 설문")
            def survey_dialog():
                st.write("더 나은 도서관을 위해 의견을 남겨주세요.")
    
                # 팝업창 안에서 폼(Form)을 열어 입력을 하나로 묶습니다.
                with st.form(key="survey_form"):
                    # 라디오 버튼으로 만족도를 선택하게 합니다.
                    score = st.radio("전반적인 만족도는 어떠신가요?", ["매우 만족", "보통", "불만족"])
                    # 긴 텍스트를 입력받는 칸을 만듭니다.
                    feedback = st.text_area("개선할 점을 자유롭게 적어주세요.")
        
                    # 폼 제출 버튼을 만듭니다.
                    submit = st.form_submit_button("설문 제출하기")
        
                # 제출 버튼이 눌렸다면,
                if submit:
                    # 감사 메시지를 띄우고
                    st.success("소중한 의견 감사합니다!")
                    # 2초 정도 메시지를 보여줄 시간을 주기 위해 잠시 멈추는 기능(추가 활용)이 들어갈 수 있지만,
                    # 여기서는 곧바로 창을 닫고 새로고침 하도록 합니다.
                    st.rerun()

            # 메인 화면 구성하기
            st.title("중앙 도서관 서비스 안내")
            st.write("환영합니다. 원하는 메뉴를 선택해주세요.")

            # 팝오버를 활용해 화면 한구석에 작은 필터/설정 창을 만듭니다.
            with st.popover("⚙️ 화면 설정"):
                st.toggle("다크 모드 적용")
                st.toggle("알림 켜기")

            # 거리를 살짝 띄워줍니다.
            st.divider()

            # 메인 화면에서 설문조사 버튼을 만듭니다.
            st.info("현재 도서관 이용 만족도 설문조사가 진행 중입니다.")
            if st.button("설문조사 참여하기"):
                # 버튼을 누르면 위에서 만든 팝업창 함수를 실행합니다.
                survey_dialog()
            '''
            st.code(pop_code, language="python")


