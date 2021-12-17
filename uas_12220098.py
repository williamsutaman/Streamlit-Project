'''
Nama: Williams Utaman
NIM: 12220098
UAS Pemrograman Komputer
Membuat aplikasi GUI berbasis Streamlit yang menggambarkan informasi seputar data produksi minyak mentah dari berbagai negara di seluruh dunia.


CATATAN PENGGUNA: UNTUK USERNAME DAN PASSWORD SECARA LEBIH JELAS, HARAP BUKA DOKUMEN README.TXT
CATATAN PENGGUNA: UNTUK USERNAME DAN PASSWORD SECARA LEBIH JELAS, HARAP BUKA DOKUMEN README.TXT
CATATAN PENGGUNA: UNTUK USERNAME DAN PASSWORD SECARA LEBIH JELAS, HARAP BUKA DOKUMEN README.TXT
CATATAN PENGGUNA: UNTUK USERNAME DAN PASSWORD SECARA LEBIH JELAS, HARAP BUKA DOKUMEN README.TXT
CATATAN PENGGUNA: UNTUK USERNAME DAN PASSWORD SECARA LEBIH JELAS, HARAP BUKA DOKUMEN README.TXT


PART A 
Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N, dimana nilai
N dapat dipilih oleh user secara interaktif. Nama negara N dituliskan secara lengkap bukan kode
negaranya.

PART B 
Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar pada tahun T, dimana
nilai B dan T dapat dipilih oleh user secara interaktif.

PART C
Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar secara kumulatif
keseluruhan tahun, dimana nilai B dapat dipilih oleh user secara interaktif.

PART D
Informasi yang menyebutkan: (1) nama lengkap negara, kode negara, region, dan sub-region
dengan jumlah produksi terbesar pada tahun T dan keseluruhan tahun. (2) nama lengkap negara,
kode negara, region, dan sub-region dengan jumlah produksi terkecil (tidak sama dengan nol)
pada tahun T dan keseluruhan tahun. (3) nama lengkap negara, kode negara, region, dan
sub-region dengan jumlah produksi sama dengan nol pada tahun T dan keseluruhan tahun.

'''

#Kumpulan library yang perlu dipanggil bagi perancangan dan pengoperasian program
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth
from os import remove
from numpy.lib.function_base import append
from matplotlib import cm
from sklearn.linear_model import LinearRegression
from typing import List

#KOMPONEN KELENGKAPAN TAMPILAN AWAL PADA STREAMLIT

#Penentuan ukuran halaman pada Streamlit
st.set_page_config(layout="wide")
#Pembuatan wallpaper pada halaman Streamlit
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://images.pexels.com/photos/87236/pexels-photo-87236.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")
    }
   .sidebar .sidebar-content {
        background: url("https://images.pexels.com/photos/87236/pexels-photo-87236.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")
    }
    </style>
    """,
    unsafe_allow_html=True
)
#Konsep User Authentication sederhana dengan metode bawaan Streamlit dari library "streamlit_authenticator"
st.subheader("PUSAT INFORMASI PRODUKSI MINYAK BUMI DUNIA")
names = ['Williams', 'Williams', 'Habibur', 'Habibur', 'Nur Ahmadi', 'Nur Ahmadi']
usernames = ['Williams', 'williams', 'Habibur', 'habibur', 'Nur', 'nur']
passwords = ['Kelas02', 'Kelas02', 'Kelas02', 'Kelas02', 'Kelas01', 'Kelas01']
hashed_passwords = stauth.hasher(passwords).generate()
authenticator = stauth.authenticate(names, usernames, hashed_passwords, 'some_cookie_name','some_signature_key', cookie_expiry_days=0)
name, authentication_status = authenticator.login('Login','main')
if authentication_status:
    st.write(f'Selamat datang _{name}_!')
    #Penulisan judul dan identitas awal pada halaman Streamlit
    st.markdown("<h1 style='text-align: center; color: red;'>REKAPITULASI PRODUKSI MINYAK BUMI DUNIA</h1>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: right; color: white;'>Williams Utaman</h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: right; color: white;'>12220098</h1>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: right; color: white;'>All rights reserved</h6>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: right; color: white;'>Copyright 2021</h6>", unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")

    #BAGIAN KENDALI UNTUK KEDUA SUMBER FILE DATA EKSTERNAL

    #Fungsi untuk mengonversi data pada file csv menjadi list
    def csvConverter():
        df = pd.read_csv('produksi_minyak_mentah.csv')
        list = [[row[col] for col in df.columns] for row in df.to_dict('records')]
        return list

    #Fungsi untuk mengekstrak kode negara dalam bentuk list
    def extractor(extractcode_lst):
        lst = csvConverter()
        code_lst = []
        for i in range(len(lst)):
            if lst[i][0] == extractcode_lst:
                code_lst.append(lst[i])
        return code_lst

    #Fungsi untuk mengekstrak nama negara dari file source json dan menghubungkan ke kode negara
    def country_basic():
        Code_lst = csvConverter()
        CountryCode_lst = []
        Country_Code = Code_lst[0][0]
        Country_lst = []
        for i in Code_lst:
            if i[0] != Country_Code:
                CountryCode_lst.append(Country_Code)
                Country_Code = i[0]
        with open("kode_negara_lengkap.json") as f:
            data = json.load(f)
        for i in range(len(CountryCode_lst)):
            for Country in data:
                if CountryCode_lst[i] == Country["alpha-3"]:
                    Country_lst.append(
                        [Country["alpha-3"], Country["name"]])
                    break
        return Country_lst

    #Fungsi untuk membuat list nama negara
    def countrybasic_lst():
        lst = []
        countrybasic_lst = country_basic()
        for i in countrybasic_lst:
            lst.append(i)
        return lst

    #Pembentukan list nama negara yang siap dipakai dalam program
    CountryNames = []
    for i in countrybasic_lst():
        CountryNames.append(i[1])
    datframe = pd.DataFrame(CountryNames, columns = ['Nama Negara'])

    #Fungsi untuk menyinkronkan nama negara terhadap kode negara
    def country_code_relate(countryname):
        lst = country_basic()
        for i in lst:
            if i[1] == countryname:
                return i[0]

    #MEKANISME PEMENUHAN PERMINTAAN SOAL BAGIAN A

    #Fungsi untuk merancang grafik yang menampilkan hubungan tahun produksi dan jumlah produksi pada suatu negara
    def CountryProductionChart(complete_country):
        year_lst = extractor(country_code_relate(complete_country))
        X = []
        for i in range(len(year_lst)):
            X.append(year_lst[i][1])
        Y = []
        for i in range(len(year_lst)):
            Y.append(year_lst[i][2])
        regression = LinearRegression()
        regression.fit(np.array(X).reshape(-1,1),np.array(Y))
        m = regression.coef_[0]
        c = regression.intercept_
        trendline_equation = [m*x+c for x in X]
        if c >= 0:
            equation = 'y = {m:.2f}x + {c:.2f}'.format(m=m,c=c)
        else:
            equation = 'y = {m:.2f}x {c:.2f}'.format(m=m,c=c)

        plt.clf()

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown(f"<h4 style='text-align: left; color: white;'>Grafik Jumlah Produksi Minyak terhadap Tahun Produksi pada Negara {complete_country}</h4>", unsafe_allow_html=True)
        option = st.selectbox('',['Grafik Garis (Line Chart)','Grafik XY (Scatter Chart)'])
        if option == 'Grafik Garis (Line Chart)': 
            plt.plot(X,Y,label='Pergerakan Jumlah Produksi', color = "blue")
            plt.plot(X,trendline_equation,label='Trendline\n{}'.format(equation), color = "red")
            plt.xlabel('Tahun Produksi')
            plt.ylabel('Jumlah Produksi')
            plt.legend()
            st.pyplot(plt)
        else:
            dic['trendline'] = trendline_equation
            scat_chart = px.scatter(pd.DataFrame(dic),x='tahun',y='produksi',trendline='lowess',trendline_options=dict(frac=0.1))
            st.plotly_chart(scat_chart)

    #MEKANISME PEMENUHAN PERMINTAAN SOAL BAGIAN B

    #Fungsi untuk membentuk data tahun produksi ke dalam suatu list
    def YearExtractor(Input_Year):
        lst = csvConverter()
        YearLst = []
        for i in lst:
            if i[1] == Input_Year:
                YearLst.append(i)
        return YearLst

    #Fungsi untuk menghitung jumlah produksi per negara dengan hasil akhir sebagai list
    def rank_counter(Input_Country, Input_Year):
        lst = csvConverter()
        allcountry_lst = country_basic()
        Code_lst = YearExtractor(Input_Year)
        valuelst = [lst[i][2] for i in range(len(lst))]
        prod_lst = []
        for j in Code_lst:
            prod_lst.append(j[2])
        count = 0
        country_rank = []
        while (count < Input_Country):
            Maximum = max(prod_lst)
            for i in allcountry_lst:
                if lst[valuelst.index(Maximum)][0] == i[0]:
                    country_rank.append([i[1], Maximum])
                    count += 1
                    break
            prod_lst.remove(Maximum)
        return country_rank

    #Fungsi untuk membentuk "sekian" besar negara menurut jumlah produksi ke dalam list secara berurutan
    def final_rankcounter(Input_Country, Input_Year):
        lst = rank_counter(Input_Country, Input_Year)
        countryrank_fixed = []
        for i in lst:
            countryrank_fixed.append(i[1])
        return countryrank_fixed

    #Fungsi untuk membentuk list "sekian" besar negara menurut jumlah produksi dengan sinkronisasi terhadap nama negara
    def countryrank_names(Input_Country, Input_Year):
        lst = rank_counter(Input_Country, Input_Year)
        namesrank_lst = []
        for i in lst:
            namesrank_lst.append(i[0])
        return namesrank_lst

    #Fungsi untuk merancang grafik yang menampilkan "sekian" besar negara secara berurutan dengan acuan terhadap hasil produksi
    def PeriodicProdChart(Input_Country, Input_Year):
        X = countryrank_names(Input_Country, Input_Year)
        Y = final_rankcounter(Input_Country, Input_Year)

        plt.clf()

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown(f"<h4 style='text-align: left; color: white;'>Grafik {Input_Country} Besar Negara dengan Jumlah Produksi Periodik Minyak Terbanyak</h4>", unsafe_allow_html=True)
        option2 = st.selectbox(' ',['Grafik Batang (Bar Chart)','Grafik Lingkaran (Pie Chart)'])
        if option2 == 'Grafik Batang (Bar Chart)': 
            plt.style.use("seaborn")
            plt.bar(X, Y, width=0.5, bottom=None, align="center", color="gold", edgecolor="black", data=None, zorder=5)
            plt.grid(True, color="red", linewidth="1", linestyle="-.", zorder=0)
            for i in range(len(Y)):
                plt.annotate(f'{Y[i]}\n', xy=(X[i], Y[i]), ha="center", va="center", size="xx-small")
            plt.legend(labels=["Negara dengan Produksi Periodik Minyak Tertinggi"], loc="best")
            plt.xlabel("Negara")
            plt.xticks(rotation=30, size="xx-small")
            plt.ylabel(f"Jumlah Produksi Tahun {Input_Year}")
            st.pyplot(plt)
        else:
            labels = X
            sizes = Y
            piechart, ax1 = plt.subplots()
            explode = None
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
            ax1.axis('equal')  
            st.pyplot(piechart)

    #MEKANISME PEMENUHAN PERMINTAAN SOAL BAGIAN C

    #Fungsi untuk menghitung jumlah produksi kumulatif per negara
    def cumulative_counter(Input_Country):
        lst = csvConverter()
        allcountry_lst = country_basic()
        extractcode_lst = lst[0][0]
        cumulative_lst = []
        Var1 = []
        Var2 = []
        rank_lst = []
        count = 0
        index = 0
        sum = 0
        for target_lst in lst:
            if index != len(lst) - 1:
                if extractcode_lst == target_lst[0]:
                    sum += target_lst[2]
                else:
                    sum = round(sum, 3)
                    cumulative_lst.append([extractcode_lst, sum])
                    Var1.append(sum)
                    Var2.append(sum)
                    extractcode_lst = target_lst[0]
                    sum = 0
                    sum += target_lst[2]
            else:
                sum += target_lst[2]
                sum = round(sum, 3)
                cumulative_lst.append([extractcode_lst, sum])
                Var1.append(sum)
                Var2.append(sum)
            index += 1
        while (count < Input_Country):
            Maximum = max(Var1)
            for i in allcountry_lst:
                if cumulative_lst[Var2.index(Maximum)][0] == i[0]:
                    rank_lst.append([i[1], Maximum])
                    count += 1
                    break
            Var1.remove(Maximum)
        return rank_lst

    #Fungsi untuk mengidentifikasi urutan dari list jumlah produksi kumulatif per negara yang telah terbentuk
    def cumulative_fixed(Input_Country):
        lst = cumulative_counter(Input_Country)
        cumfixed_lst = []
        for i in lst:
            cumfixed_lst.append(i[1])
        return cumfixed_lst

    #Fungsi untuk menyinkronkan list urutan "sekian besar" dan data produksi kumulatif per negara terhadap nama negara tersebut masing-masing
    def CountryCum_relate(Input_Country):
        lst = cumulative_counter(Input_Country)
        finalrelate_lst = []
        for i in lst:
            finalrelate_lst.append(i[0])
        return finalrelate_lst

    #Fungsi untuk merancang grafik yang menampilkan "sekian" besar negara secara berurutan dengan acuan terhadap hasil produksi kumulatif
    def CumProdChart(Input_Country):
        X = CountryCum_relate(Input_Country)
        Y = cumulative_fixed(Input_Country)

        plt.clf()

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown(f"<h4 style='text-align: left; color: white;'>Grafik {Input_Country} Besar Negara dengan Jumlah Produksi Kumulatif Minyak Terbanyak</h4>", unsafe_allow_html=True)
        option3 = st.selectbox('   ',['Diagram Batang (Bar Chart)', 'Diagram Lingkaran (Pie Chart)'])
        if option3 == 'Diagram Batang (Bar Chart)': 
            plt.style.use("seaborn")
            plt.bar(X, Y, width=0.5, bottom=None, align="center", color="gold", edgecolor="black", data=None, zorder=5)
            plt.grid(True, color="red", linewidth="1", linestyle="-.", zorder=0)
            for i in range(len(Y)):
                plt.annotate(f'{Y[i]}\n', xy=(X[i], Y[i]), ha="center", va="center", size="xx-small")
            plt.legend(labels=["Negara dengan Produksi Kumulatif Minyak Tertinggi"], loc="best")
            plt.xlabel("Negara")
            plt.xticks(rotation=30, size="x-small")
            plt.ylabel("Jumlah Produksi Kumulatif")
            st.pyplot(plt)
        else:
            labels = X
            sizes = Y
            explode = None
            piechart2, ax2 = plt.subplots()
            ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
            ax2.axis('equal')
            st.pyplot(piechart2) 

    #MEKANISME PEMENUHAN PERMINTAAN SOAL BAGIAN D

    #Fungsi untuk menghitung produksi minyak yang paling sedikik (sedikit != 0)     
    def minimum_counter(Input_Year):
        lst = csvConverter()
        allcountry_lst = country_basic()
        Code_lst = YearExtractor(Input_Year)
        valuelst = [lst[i][2] for i in range(len(lst))]
        prod_lst = []
        for j in Code_lst:
            prod_lst.append(j[2])
        smallest_lst = []
        Min_value = min(prod_lst)
        while Min_value == 0:
            prod_lst.remove(Min_value)
            Min_value = min(prod_lst)
        for i in allcountry_lst:
            if lst[valuelst.index(Min_value)][0] == i[0]:
                smallest_lst.append([i[1], Min_value])
                break
        prod_lst.remove(Min_value)
        return smallest_lst

    #Fungsi untuk menghitung produksi minyak yang sama dengan nol
    def zero_counter(Input_Year):
        zerolst = []
        zerofixed_lst = []
        lst = csvConverter()
        for i in lst:
            if i[2] == 0 and i[1] == Input_Year:
                zerolst.append([i[0], i[2]])
        for j in zerolst:
            for i in country_basic():
                if i[0] == j[0]:
                    zerofixed_lst.append([i[1], j[1]])
        return zerofixed_lst

    #Fungsi berupa akumulasi syntax terkait summary produksi minyak paling banyak, sedikit, dan nol pada tahun tertentu
    def specific_year(Input_Year, Input_Option):
        Targets = []
        lst = []
        if Input_Option == "The_Most":
            lst.extend(rank_counter(1, Input_Year))
        elif Input_Option == "The_Least":
            lst.extend(minimum_counter(Input_Year))
        elif Input_Option == "Zero":
            lst.extend(zero_counter(Input_Year))
        with open("kode_negara_lengkap.json") as f:
            data = json.load(f)
        for i in range(len(lst)):
            for Country in data:
                if Country["name"] == lst[i][0]:
                    if Input_Option != "Zero":
                        Targets.extend([Country["name"], Country["alpha-3"],
                                          Country["region"], Country["sub-region"]])
                        break
                    else:
                        Targets.append([Country["name"], Country["alpha-3"],
                                          Country["region"], Country["sub-region"]])
        return Targets

    #Fungsi berupa akumulasi untuk menghitung produksi minyak paling banyak, sedikit, dan nol dengan mengacu kepada fungsi kumulatif sebelumnya
    def complete_counter(Input_Option):
        lst = csvConverter()
        allcountry_lst = country_basic()
        extractcode_lst = lst[0][0]
        cumulative_lst = []
        Var1 = []
        Var2 = []
        ModeComp = []
        sum = 0
        index = 0
        for target_lst in lst:
            if index != len(lst) - 1:
                if extractcode_lst == target_lst[0]:
                    sum += target_lst[2]
                else:
                    sum = round(sum, 3)
                    cumulative_lst.append([extractcode_lst, sum])
                    Var1.append(sum)
                    Var2.append(sum)
                    extractcode_lst = target_lst[0]
                    sum = 0
                    sum += target_lst[2]
            else:
                sum += target_lst[2]
                sum = round(sum, 3)
                cumulative_lst.append([extractcode_lst, sum])
                Var1.append(sum)
                Var2.append(sum)
            index += 1
        if (Input_Option == "The_Most"):
            ModeComp = cumulative_counter(1)
        elif (Input_Option == "The_Least"):
            Min_value = min(Var1)
            while Min_value == 0:
                Var1.remove(Min_value)
                Min_value = min(Var1)
            for i in allcountry_lst:
                if cumulative_lst[Var2.index(Min_value)][0] == i[0]:
                    ModeComp.append([i[1], Min_value])
                    break
                else:
                    while Min_value == 0:
                        Var1.remove(Min_value)
                        Min_value = min(Var1)
        elif (Input_Option == "Zero"):
            zeroprod_lst = []
            for i in cumulative_lst:
                if i[1] == 0:
                    zeroprod_lst.append(i)
            for i in zeroprod_lst:
                for j in allcountry_lst:
                    if i[0] == j[0]:
                        ModeComp.append([j[1], 0])
                        break
        return ModeComp

    #Fungsi untuk menindaklanjuti fungsi complete_counter untuk memberikan summary kepada user
    def complete_summary(Input_Option):
        Targets_compsump = []
        lst = complete_counter(Input_Option)
        with open("kode_negara_lengkap.json") as f:
            data = json.load(f)
        for i in range(len(lst)):
            for Country in data:
                if Country["name"] == lst[i][0]:
                    if Input_Option != "Zero":
                        Targets_compsump.extend([Country["name"], Country["alpha-3"],
                                          Country["region"], Country["sub-region"]])
                        break
                    else:
                        Targets_compsump.append([Country["name"], Country["alpha-3"],
                                          Country["region"], Country["sub-region"]])
        return Targets_compsump


    #KOMPONEN PEMBUATAN MAIN CONTENT PADA STREAMLIT
            
    #Input berupa permintaan masukkan pilihan oleh user
    country = st.sidebar.selectbox('Apa negara yang ingin Anda analisis? ',CountryNames)
    rank = st.sidebar.number_input("Berapa besar (jumlah) negara yang ingin Anda analisis?", min_value=1, max_value=137, value=4)
    year = st.sidebar.number_input("Kapan tahun produksi yang ingin Anda analisis?", min_value=1971, max_value=2015)

    #Pembuatan tampilan frame data umum produksi minyak per tahun sesuai negara yang dipilih
    year_lst = extractor(country_code_relate(country))
    X = []
    for i in range(len(year_lst)):
        X.append(year_lst[i][1])
    Y = []
    for i in range(len(year_lst)):
        Y.append(year_lst[i][2])
    dic = {'tahun':X,'produksi':Y}
    st.markdown(f"<h4 style='text-align: left; color: white;'>Data Umum Produksi Minyak Negara {country}</h4>", unsafe_allow_html=True)
    st.write(pd.DataFrame(dic))
    
    #Pemanggilan fungsi untuk menampilkan grafik jumlah produksi minyak terhadap tahun produksi sesuai negara yang dipilih
    csvConverter()
    country_code_relate(country)
    country_basic()
    countrybasic_lst()
    extractor(country_code_relate(country))
    CountryProductionChart(country)

    #Pemanggilan fungsi untuk menampilkan grafik "sekian" besar negara dengan jumlah produksi periodik minyak terbanyak
    YearExtractor(year)
    rank_counter(rank, year)
    final_rankcounter(rank, year)
    countryrank_names(rank, year)
    PeriodicProdChart(rank, year)

    #Pemanggilan fungsi untuk menampilkan grafik "sekian" besar negara dengan jumlah produksi kumulatif minyak terbanyak
    cumulative_counter(rank)
    cumulative_fixed(rank)
    CountryCum_relate(rank)
    CumProdChart(rank)

    #Pemanggilan fungsi untuk menampilkan summary dari berbagai kriteria analisis terkait jumlah dan tahun produksi
    minimum_counter(year)
    zero_counter(year)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown(f"<h4 style='text-align: left; color: white;'>Simpulan Informasi Produksi Minyak Bumi Dunia pada Tahun {year}</h4>", unsafe_allow_html=True)
    option4 = st.selectbox('    ',['Negara dengan Jumlah Produksi Minyak Tertinggi', 'Negara dengan Jumlah Produksi Minyak Terendah', 'Negara yang Tidak Memproduksi Minyak'])
    if option4 == 'Negara dengan Jumlah Produksi Minyak Tertinggi':
        mostlst = specific_year(year, 'The_Most')
        df_most = pd.DataFrame([mostlst], columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region'])
        st.write(df_most)
    elif option4 == 'Negara dengan Jumlah Produksi Minyak Terendah':
        leastlst = specific_year(year, 'The_Least')
        df_least = pd.DataFrame([leastlst], columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region'])
        st.write(df_least)
    elif option4 == 'Negara yang Tidak Memproduksi Minyak':
        zerolst = specific_year(year, 'Zero')
        df_zero = pd.DataFrame(zerolst)
        df_zero.columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region']
        st.write(df_zero)
    st.markdown(f"<h4 style='text-align: left; color: white;'>Simpulan Informasi Produksi Minyak Bumi Dunia pada Keseluruhan Tahun</h4>", unsafe_allow_html=True)
    option5 = st.selectbox('     ',['Negara dengan Jumlah Produksi Minyak Tertinggi', 'Negara dengan Jumlah Produksi Minyak Terendah', 'Negara yang Tidak Memproduksi Minyak'])    
    if option5 == 'Negara dengan Jumlah Produksi Minyak Tertinggi':
        complete_counter('The_Most')
        mostlst2 = complete_summary('The_Most')
        df_most2 = pd.DataFrame([mostlst2], columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region'])
        st.write(df_most2)
    elif option5 == 'Negara dengan Jumlah Produksi Minyak Terendah':
        complete_counter('The_Least')
        leastlst2 = complete_summary('The_Least')
        df_least2 = pd.DataFrame([leastlst2], columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region'])
        st.write(df_least2)
    elif option5 == 'Negara yang Tidak Memproduksi Minyak':
        complete_counter('Zero')
        zerolst2 = complete_summary('Zero')
        df_zero2 = pd.DataFrame(zerolst2)
        df_zero2.columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region']
        st.write(df_zero2)

elif st.session_state['authentication_status'] == False:
    st.error('Username atau Password yang Anda Masukkan Salah!')
