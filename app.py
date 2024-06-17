import streamlit as st
import pandas as pd
import rstr
import time
from streamlit_echarts import st_echarts

# Regular Expression Matching Functions
def isMatchDP(s, p):
    dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
    dp[0][0] = True
    
    for i in range(1, len(p) + 1):
        if p[i - 1] == '*':
            dp[0][i] = dp[0][i - 2]
    
    for i in range(1, len(s) + 1):
        for j in range(1, len(p) + 1):
            if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                ignore_star = dp[i][j - 2]
                match_star = dp[i - 1][j] and (s[i - 1] == p[j - 2] or p[j - 2] == '.')
                dp[i][j] = ignore_star or match_star
    
    return dp[len(s)][len(p)]

def isMatchBacktracking(s, p):
    def backtrack(i, j):
        if j == len(p):
            return i == len(s)
        next_char_is_star = (j + 1 < len(p) and p[j + 1] == '*')
        if next_char_is_star:
            if backtrack(i, j + 2):
                return True
            while i < len(s) and (s[i] == p[j] or p[j] == '.'):
                i += 1
                if backtrack(i, j + 2):
                    return True
        else:
            if i < len(s) and (s[i] == p[j] or p[j] == '.'):
                return backtrack(i + 1, j + 1)
        return False
    
    return backtrack(0, 0)

# Streamlit App
st.set_page_config(page_title="Tugas Besar Strategi Algoritma", page_icon=":rocket:")

st.title(':blue[Regular Expression Matching] :sparkles:')

st.markdown("""
### :books: Tugas Besar Strategi Algoritma
- **Valentino Hartanto** - 1301223020
- **Gede Bagus Krishnanditya Merta** - 1301223088 
- **Raka Aditya Waluya** - 1301220192

### :page_facing_up: Deskripsi
Tugas besar ini bertujuan untuk menganalisis dan membandingkan strategi algoritma antara backtracking dan dynamic programming dalam konteks regular expression (regex) matching. Regex matching adalah proses penting dalam pengolahan teks yang dapat digunakan untuk berbagai aplikasi seperti pencarian pola, validasi input, dan transformasi data.
""")

pattern = st.text_input("Masukkan pattern regular expression:", placeholder="Contoh: a*b.c")

if pattern:
    listAlp = []
    for char in pattern:
        if '.' == char or '*' == char:
            continue
        if char not in listAlp:
            listAlp.append(char)    
    result = ''.join(listAlp)

    listLength = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240]
    listString = []

    for panjang in listLength:
        listString.append(rstr.rstr(result, panjang))
    st.success(f'Berhasil melakukan generate string dengan panjang sebagai berikut: {listLength}')

if st.button('Mulai', key='start_button'):
    timeDP = []
    timeBT = []

    with st.spinner('Menghitung waktu eksekusi...'):
        for string in listString:
            startTime = time.time()
            temp = isMatchDP(string, pattern)
            totaltime = time.time() - startTime
            timeDP.append(totaltime)

        for string in listString:
            startTime = time.time()
            temp = isMatchBacktracking(string, pattern)
            totaltime = time.time() - startTime
            timeBT.append(totaltime)

    st.subheader("📊 Perbandingan Waktu Eksekusi Algoritma")

    data = {
        "List Length": listLength,
        "Dynamic Programming": timeDP,
        "Backtracking": timeBT
    }
    df = pd.DataFrame(data).transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    st.table(df)
    
    option = {
        "backgroundColor": "#2E2E2E",
        "xAxis": {
            "type": "category",
            "data": listLength,
        },
        "animation": {
            "duration": 1500,
            "easing": "quinticInOut",
            "delay": 0,
            "opacity": {
                "duration": 1000,
                "easing": "linear",
                "from": 0.3,
                "to": 0.5,
            },
        },
        "legend": {
            "data": ["Dynamic Programming", "Backtracking"],
            "textStyle": {"color": "#FFFFFF"},  
            "selected": {
                "Dynamic Programming": True,
                "Backtracking": True,
            },
            "delay": 300,
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Dynamic Programming",
                "data": timeDP,
                "type": "line",
                "label": {
                    "show": False,
                    "position": "top",
                },
                "animation": {
                    "duration": 1000,
                    "easing": "elasticOut",
                    "fadeIn": "true",
                },
                "itemStyle": {"color": "#FF6347"},
                "emphasis": {
                    "focus": 'series'
                },
            },
            {
                "name": "Backtracking",
                "data": timeBT,
                "type": "line",
                "label": {
                    "show": False,
                    "position": "top",
                },
                "animation": {
                    "duration": 1000,
                    "easing": "elasticOut",
                },
                "itemStyle": {"color": "#4682B4"},
                "emphasis": {
                    "focus": 'series'
                },
            },
        ],
    }

    st_echarts(options=option, height="400px")
