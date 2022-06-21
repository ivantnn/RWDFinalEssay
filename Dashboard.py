#Pandas
import pandas as pd
#Plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import math as m
#Streamlit
import streamlit as st


#https://www.webfx.com/tools/emoji-cheat-sheet/

#---------TITLE OF PAGE
st.set_page_config(page_title = 'Radiological Waste Management', page_icon=":warning:",layout="wide")

#---------ZERO-th SECTION: INTRO
st.title(':thought_balloon:Introduction')
st.write('Radioactive waste finds itself pretty often amidst the discussion of the viability of the Nuclear Power as a reliable and long-term energy source against climate change: Sometimes called the Achilles Heel of the energy source, sometimes argued as an advantage of nuclear in face of the fossil fuels.')
st.write('There are several subcategories of Radioactive Waste, one of them being the High-Level Waste (HLW), which can have its origin traced back to Spent Fuel.')
st.write('Due to its grand hazard to human health and its long-dated radiotoxicity, one possible way to keep HLW away from contaminating nature is by trapping it into Glass Matrices.')
st.write('Since lots of countries adopted strategies to maintain radioactive residues in repositories, even with the glass matrix, it is paramount the conduction of analysis on how will these glass matrices stand the passage of the decades and isolate the radionuclides.')

#---------FIRST SECTION: INPUT
st.title(':arrow_down_small: Input Data')
st.header('> Initial Conditions & Nuclear Data: ')

#Importing the pandas DataFrames
df1 = pd.read_csv('initial_cond.csv',index_col=0)
df1 = df1.join(pd.read_csv('decay_cte_data.csv',index_col=0),how='outer')

#Making a selection box to sort the DataFrame
opt = st.selectbox(
     'How would you like to sort the input data?',
     ('Mass Order', 'Moles Order', 'Decay Cte Order'))

#Function to sort the DataFrame
def input_filter(opt,df1):
    if opt=='Mass Order':
        df1_mod = df1.sort_index()
    elif opt =='Moles Order':
        df1_mod = df1.sort_values(by='Moles')
    else:
        df1_mod = df1.sort_values(by='Cte')
    return df1_mod

df1_mod = input_filter(opt,df1)


#Plot with Plotly
fig = make_subplots(1,1,specs=[[{"secondary_y": True}]]) #TElling Plotly that are 2 graphs

# First Graph is a bar graphic for the Moles
fig.add_trace(go.Bar(x=df1_mod.index, y=df1_mod['Moles'],
                     name='Moles',
                     marker_color = 'white',
                     opacity=0.4,
                     marker_line_color='rgb(8,48,107)',
                     marker_line_width=2),secondary_y=False)

# Second graph is a line graph, showing the Decay Constants
fig.add_trace(go.Scatter(
                        x=df1_mod.index, y=df1_mod['Cte'],
                        line=dict(color='red'),
                        name='Decay Cte'),
                        secondary_y=True)

# Adding More information on the y-axis
#This one is about the Decay Constant
fig.update_yaxes(
    title_text="<b>Decay Constant</b>",
    type="log", secondary_y=True)
#This one is about the Moles
fig.update_yaxes(
    title_text="<b>Moles</b>",
    secondary_y=False)

fig.update_xaxes(title_text = "<b>Compounds</b>",tickangle=45)

st.plotly_chart(fig, use_container_width=True)
st.write('Source: IAEA Nuclear Data Decay Service (NuDat 3) -> [Link](https://www.nndc.bnl.gov/nudat3/)')

st.header('Decay chain')
st.latex(r'''
     \begin{CD}
        {}^{245}Cm @>\alpha>> {}^{241}Pu
        @>\beta^{{}-{}} >> {}^{241}Am
        @>\alpha>> {}^{237}Np
        @>\alpha>> {}^{233}Pa
        @>\beta^{{}-{}} >> {}^{233}U
        @>\alpha >> {}^{229}Th
        @>\alpha >> {}^{225}Ra
        @>\beta^{{}-{}} >> {}^{225}Ac
        @>\alpha >> {}^{221}Fr
        @>\alpha >> {}^{217}At
        @>\alpha >> {}^{213}Bi
        @> 0.02\beta^{{}-{}} >> {}^{213}Po
        @>\alpha >> {}^{209}Pb
        @>\beta^{{}-{}} >> {}^{209}Bi
        @>\alpha >> {}^{205}Tl \\
        @. @. @. @. @. @. @. @. @. @. @.  @V 0.98 \alpha VV @. @A \beta^{{}-{}} AA \\
        @. @. @. @. @. @. @. @. @. @. @. {}^{209}Tl @= {}^{209}Tl @= {}^{209}Tl \\
    \end{CD}
     ''')


#-----SECOND SECTION: RESULTS
st.markdown('---')
st.title(':arrow_up_small: Results')
st.header('> Parameters selection: ')
#st.plotly_chart(heatmap)
l_col,m_col,r_col = st.columns(3)

with l_col:
    st.subheader('Select a value of the start of Containment Failure (Start of Leaching - $t_c$)')

    tc_sel = st.radio(
     "Select a time:",
     ('1000 years', '2000 years', '3000 years', '5000 years'))

with m_col:
    st.subheader('Select a value of End of Containment (Leaching Completed - $t_l$)')

    tl_sel = st.radio(
     "Select a time:",
     ('1 Million years', '2 Million years', '5 Million years','10 Million years'))

with r_col:
    st.subheader('Moles in Log? ')
    Y_scale = st.radio("Put Y in Log:",
     ('No, Thanks','Yes, please'))

#Putting the plots

def Filter(tc,tl):
    if tc == '1000 years':
        if tl =='1 Million years':
            df_ans = pd.read_csv('Answer_tc1k_tl1M.csv',index_col=0)
        elif tl == '2 Million years':
            df_ans = pd.read_csv('Answer_tc1k_tl2M.csv',index_col=0)
        elif tl =='5 Million years':
            df_ans = pd.read_csv('Answer_tc1k_tl5M.csv',index_col=0)
        elif tl == '10 Million years':
            df_ans = pd.read_csv('Answer_tc1k_tl10M.csv',index_col=0)

    elif tc == '2000 years':
        if tl =='1 Million years':
            df_ans = pd.read_csv('Answer_tc2k_tl1M.csv',index_col=0)
        elif tl == '2 Million years':
            df_ans = pd.read_csv('Answer_tc2k_tl2M.csv',index_col=0)
        elif tl =='5 Million years':
            df_ans = pd.read_csv('Answer_tc2k_tl5M.csv',index_col=0)
        elif tl == '10 Million years':
            df_ans = pd.read_csv('Answer_tc2k_tl10M.csv',index_col=0)

    elif tc == '3000 years':
        if tl =='1 Million years':
            df_ans = pd.read_csv('Answer_tc3k_tl1M.csv',index_col=0)
        elif tl == '2 Million years':
            df_ans = pd.read_csv('Answer_tc3k_tl2M.csv',index_col=0)
        elif tl =='5 Million years':
            df_ans = pd.read_csv('Answer_tc3k_tl5M.csv',index_col=0)
        elif tl == '10 Million years':
            df_ans = pd.read_csv('Answer_tc3k_tl10M.csv',index_col=0)

    elif tc == '5000 years':
        if tl =='1 Million years':
            df_ans = pd.read_csv('Answer_tc5k_tl1M.csv',index_col=0)
        elif tl == '2 Million years':
            df_ans = pd.read_csv('Answer_tc5k_tl2M.csv',index_col=0)
        elif tl =='5 Million years':
            df_ans = pd.read_csv('Answer_tc5k_tl5M.csv',index_col=0)
        elif tl == '10 Million years':
            df_ans = pd.read_csv('Answer_tc5k_tl10M.csv',index_col=0)

    return df_ans

df_ans = Filter(tc_sel, tl_sel)
n = len(df_ans.columns)
df_ans.index = df_ans.index

fig2 = make_subplots(1,1)
fig3 = make_subplots(1,1)

    # First Graph is a bar graphic for the Moles
fig2 = px.line(df_ans.iloc[:,0:int(n/2)], log_x = True, title = 'Concentration Glass Matrix')
fig3 = px.line(df_ans.iloc[:,int(n/2):], log_x = True, title = 'Concentration Outside of Matrix')

if Y_scale == 'No, Thanks':
    fig2.update_yaxes(title_text="<b>Moles</b>")
    fig3.update_yaxes(title_text="<b>Moles</b>")
else:
    fig2.update_yaxes(title_text="<b>Moles</b>", type="log")
    fig3.update_yaxes(title_text="<b>Moles</b>", type="log")

fig2.update_xaxes(
    title_text="<b>Times (Years) </b>",
    type="log")

st.plotly_chart(fig2, use_container_width=True)

fig3.update_xaxes(
    title_text="<b>Times (Years) </b>",
    type="log")

st.plotly_chart(fig3, use_container_width=True)

st.markdown('##')

st.markdown('---')

st.title(':bulb:Theory')
st.subheader(":floppy_disk: Data")
with st.expander("+ See more"):
     st.write("""
         Nuclear Data and Decay chain information were both adquired from the IAEA's [NuDat 3](https://www.nndc.bnl.gov/nudat3/) system. The Values utilised being:
     """)
     st.latex(r'''
        \begin{matrix}
        Nuclide & Decays & Half-Life\\
        {}^{245}Cm & \alpha & 8423 yrs\\
        {}^{241}Pu & \beta^{{}-{}} & 14.32 yrs\\
        {}^{241}Am & \alpha & 432 yrs\\
        {}^{237}Np & \alpha & 210000 yrs\\
        {}^{233}Pa & \beta^{{}-{}} & 647 hrs\\
        {}^{233}U & \alpha & 159 yrs\\
        {}^{229}Th & \alpha & 7932 yrs\\
        {}^{225}Ra & \beta^{{}-{}} & 357 yrs\\
        {}^{225}Ac & \alpha & 237 yrs\\
        {}^{221}Fr & \alpha & 4.7 min\\
        {}^{217}At & \alpha & 32 min\\
        {}^{213}Bi & \alpha (0.98)+\beta^{{}-{}} (0.02) & 45 min\\
        {}^{213}Po & \alpha & 3.7 \mu s\\
        {}^{209}Tl & \beta^{{}-{}} & 2.1 min\\
        {}^{209}Pb & \beta^{{}-{}} & 3.2 hrs\\
        {}^{209}Bi & \alpha & 2.01E19 yrs\\
        {}^{205} Tl & \_ & STABLE\\
        \end{matrix}
     ''')
     st.write("""
         The constants are obtained from the relation with the following decay constant:
     """)
     st.latex(r'''
        \begin{equation}
        \lambda = \frac{ln{2}}{t_{1/2}}
        \end{equation}
     ''')
     st.write("""
         For the solubilities, [a study conducted by Chalmers University - Sweden -  on the solubility of different radionuclides](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiw2LaI06X4AhVI1hoKHQ3LDU4QFnoECAYQAQ&url=https%3A%2F%2Finis.iaea.org%2Fcollection%2FNCLCollectionStore%2F_Public%2F16%2F022%2F16022266.pdf&usg=AOvVaw3mlq7-SGGbcLyaQfCfSYog) and publicated on IAEA portal can show that the solubility is around 1E-10 Mol/L
     """)

st.subheader(":wrench: Model")
with st.expander("+ See more"):
     st.write("""
         The storage is compromised of two different regions: The first one is the inside of the Glass Matrix, which is continuously leached and corroded. At time $t_c$, the time on which some of the matrix begins to leached and stops at $t_l$, when all the matrix is finally destroyed. For this reason, there are two different equation sets for the Glass Matrix: Before $t_c$ (Only decay of the radionuclides )and after (Decay and Leach from the matrix).
     """)
     st.latex(r'''
              \begin{equation}
              \frac{d u(t)}{d t} = {
                \begin{matrix}    A \cdot u(t) & \forall (t<t_c)\\
                                  A \cdot u(t) -\frac{3u(t)}{t_l-t} & \forall (t_c<t<t_l)
                \end{matrix}}
              \end{equation}
         ''')
     st.write("""
         Where u(t) is the number of radionuclides and A is the matrix of the the decay chains. It follows the following logic:
     """)
     st.latex(r'''
        A =
        \begin{matrix}
            {}^{245}Cm \\
            {}^{241}Pu \\
            \vdots \\
            {}^{209}Pb \\
            \vdots \\
            {}^{205}Tl \\
        \end{matrix}



        \begin{bmatrix}
            - \lambda_{{}^{245}Cm} & 0                   & \dots & 0                    &0                      &0                    &\dots  &0 &0\\
            \lambda_{{}^{245}Cm} & -\lambda_{{}^{241}Pu} & \dots & 0                    &0                      &0                    &\dots  &0 &0\\
            \vdots               & \vdots                &\ddots &\vdots                &\vdots                 &\vdots               &\ddots &\vdots &\vdots \\
            0                    & 0                     &\dots  &\lambda_{{}^{213}Po}  &\lambda_{{}^{209}Tl}   &-\lambda_{{}^{209}Pb} &\dots  &0 &0\\
            \vdots               & \vdots                &\ddots &\vdots                &\vdots                 &\vdots               &\ddots &\vdots &\vdots \\
            0                    & 0                     &\dots  &0                     &0                      &0                    &\dots  &\lambda_{{}^{209}Bi} &0\\
        \end{bmatrix}
     ''')
     st.write("""
         The other region is still inside the containment, but outside of the Glass Matrix. In this region, the radionuclides are still decaying, but are being constantly washed away by the infiltration of water in the containment. The set of equations are:
     """)
     st.latex(r'''
     \begin{equation}
        \frac{dU(t)}{dt} = \begin{matrix}
            0 & \forall t<t_c \\
            A \cdot U(T) + \frac{3 U(t)}{t_l - t} - Q(t) \cdot C_{s,n} & \forall t_c<t<t_l \\
        \end{matrix}
     \end{equation}
     ''')
     st.write("""
         Here the U is the number of radionuclides in the storage and outside the Glass Matrix. Q(t) is the infiltration rate of the water in the storage. C is the solubility of the radionuclides in the water.
     """)

st.subheader(":pencil: Algorithm")
with st.expander("+ See more"):
     st.write("""
         For a numeric integration, the derivative is treated with the Taylor's expansion:
     """)
     st.latex(r'''
         \begin{equation}
         x = x_0 + \frac{dx}{dt} \cdot \delta t
         \end{equation}
     ''')
     st.write("""
         With that, the system of ODEs can be solved for each time step as:
     """)
     st.latex(r'''
         \begin{equation}
         u(t+\delta t) = u(t) + \frac{du(t)}{dt} \cdot \delta t
         \end{equation}
     ''')
     st.write("The method used was the simple Euler method with a forward discretization. As for the timestep, since lots of radionuclides have centuries and milennias as half-lifes, the adoption of the calculated times as in a linear logspace was adopted")

st.subheader(":triangular_flag_on_post: References")
with st.expander("+ See more"):
     st.write("""
         > IAEA NuDat Database, available at: https://www.nndc.bnl.gov/nudat3/

         > Allard, Bert. ACTINIDE SOLUTION EQUILIBRIA AND SOLUBILITIES IN GEOLOGIC SYSTEMS. Chalmers University, Sweden. Published in 10/04/1983. Available at: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiw2LaI06X4AhVI1hoKHQ3LDU4QFnoECAYQAQ&url=https%3A%2F%2Finis.iaea.org%2Fcollection%2FNCLCollectionStore%2F_Public%2F16%2F022%2F16022266.pdf&usg=AOvVaw3mlq7-SGGbcLyaQfCfSYog

         > Class Material from Prof. Hidalgo on Radioactive Waste Management [UPM 2022]
     """)

st.write('Made by Ivan Tonon for $Radioactive$ $Waste$ $Management$ course final assessment.')
st.write('Professors: Arturo Hidalgo, Eduardo Gallego and Francisco Javier Elorza')


hide_st_style="""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html = True)
