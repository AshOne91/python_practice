
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import torch
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import sys
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_score, recall_score,confusion_matrix
from autogluon.tabular import TabularPredictor
from sklearn.metrics import confusion_matrix, roc_curve
from autogluon.tabular import TabularDataset, TabularPredictor

# 한글 폰트 설정 (Google Colab 또는 로컬에서 실행 시)
if sys.platform == "linux":
    import matplotlib.font_manager as fm
    import subprocess
    subprocess.run(["apt-get", "-qq", "-y", "install", "fonts-nanum"], check=True)
    font_files = fm.findSystemFonts(fontpaths=['/usr/share/fonts/truetype/nanum'])
    for f in font_files:
        fm.fontManager.addfont(f)
    plt.rc('font', family='NanumBarunGothic')
    plt.rcParams['axes.unicode_minus'] = False
else:
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="고객 이탈 분석 대시보드", layout="wide")
st.title("고객 이탈 분석 및 예측")

# 메뉴 선택
menu = st.sidebar.radio("메뉴를 선택하세요", ["개요", "데이터 전처리", "모델 학습", "모델 평가", "모델 추론" ,"마무리"])



# @st.cache_data
# def load_data():
#     df = pd.read_csv("bank.csv")
#     df1 = pd.read_csv("bb.csv")
#     scaler = joblib.load("scaler.pkl")
#     # 모델이 저장된 경로
#     model_path = 'Bank_model_0417'
#     # 모델 불러오기
#     model = TabularPredictor.load(model_path)
    
#     return df, df1, scaler, model
import plotly.express as px
@st.cache_data
def load_table():
    automl_model_scores = pd.read_csv('automl_model_scores_wide_format.csv')
    nomal_model_scores = pd.read_csv('nomal_model_scores_wide_format.csv')
    tuning_model_scores = pd.read_csv('tuning_model_scores_wide_format.csv')
    return automl_model_scores, nomal_model_scores, tuning_model_scores

automl_df, nomal_df, tuning_df = load_table()
nomal_df.columns.values[0] = 'Model'
tuning_df.columns.values[0] = 'Model'
automl_df.columns.values[0] = 'Model'

if menu == "개요":
    st.markdown("""
고객 이탈 데이터 시각화 및 AI 모델 고객 이탈 가능성 예측

## 🎯 프로젝트 목표  
- 은행 데이터를 바탕으로 고객 이탈을 예측하고, 이탈 요인을 시각적으로 분석  

## 🔍 프로젝트 배경  
![이탈 비율](https://i.ibb.co/HTJ6ZqvT/2025-04-17-141405.png)
![이탈 비율](https://i.ibb.co/Ps3rDN84/2025-04-17-141434.png)
- 주거래은행 이탈 비율이 높아지고 있음
    - 시중은행 이탈률: **10.1%**
    - 인터넷 전문은행 이탈률: **30.7%**
    - 연령이 낮을수록 이탈 비율이 높고 장기적으로 이탈 비율이 증가할 것으로 예상됨

![이탈 의향](https://i.ibb.co/YBf4NFp5/2025-04-17-141456.png)
- 과반이 넘는 소비자가 **거래 이탈 의향**을 가지고 있음
- 따라서 고객 이탙을 막기 위한 **이탈 예측 모델**이 필요함

![비대면 대출 갈아타기 서비스](https://img.asiatoday.co.kr/file/2024y/02m/02d/2024020201000169500007791.jpg)
- 특히 최근 낮은 금리를 지원하는 **비대면 대출 갈아타기 서비스**로 인해, 비대면 플랫폼으로의 이탈 비율이 높아지고 있음
- 때문에 은행 데이터를 기반으로 고객의 이탈을 예측하는 모델은 시의성 측면에서도 적합한 주제임

## 📑 데이터  
- 출처 : 깃허브 

### ✨ 변수 설명
| **항목**                 | **설명 (사용자 정의)**              |
|----------------------|-------------------------------|
| 이탈여부              | 고객이 이탈했는지 여부          |
| 부양가족수            | 고객이 부양하는 가족 수         |
| 교육수준              | 고객의 교육 수준               |
| 총거래관계수          | 고객과 은행 간 전체 거래 항목 수 |
| 12개월비활성개월수     | 최근 12개월 동안 비활성 기간(월) 수 |
| 12개월고객접촉횟수         | 최근 12개월 동안 고객 접촉 횟수  |
| 신용한도                  | 고객의 신용 한도               |
| 회전잔액                  | 회전(남은) 잔액               |
| 1~4분기총이용금액변화       | 1~4분기 동안의 총 이용금액 변화  |
| 총거래금액                | 총 거래 금액                   |
| 1~4분기거래횟수변화       | 분기별 거래 횟수의 변화         |
| 나이그룹                | 나이 범주형 그룹               |
| 수입                   | 고객의 수입 수준               |
| 결혼여부        | 고객의 결혼 여부     |
| 카드등급        | 고객의 카드 등급            |
| 성별               | 고객의 성별                      |


**🎉 주요 기능:**  
- 이탈 여부 분포 시각화  
- 변수별 이탈과의 관계 분석  
- 상관관계 히트맵 확인  
- 사용자 입력 기반 이탈 예측 시뮬레이션
""")

elif menu == "데이터 전처리":

    st.title("데이터 전처리")
    
    # 탭 생성
    탭1, 탭2, 탭3, 탭4 = st.tabs(["🔮 피처 엔지니어링", "🕶️ 이상치 탐색", "🔗 상관관계", "🎢 SMOTE"])
    
    with 탭1:
        st.subheader("🔮 피처 엔지니어링")
        st.markdown("""
## 범주형 데이터 처리
### 원-핫 인코딩
- 결혼 여부
- 카드 등급
- 성별

## 데이터 구간화

### 나이
| **나이**    | **나이 구간화**   |
|------------|--------|
| 0 - 30     | 0      |
| 30 - 40    | 1      |
| 40 - 50    | 2      |
| 50 - 60    | 3      |
| 60 - 100   | 4      |


### 카드 보유 기간
| **카드보유기간(개월)** | **카드보유년 (결과)** |
|-------------------|------------------|
| 48 이상           | 4                |
| 36 이상 48 미만   | 3                |
| 24 이상 36 미만   | 2                |
| 24 미만           | 1                |

### 수입 구간
| **수입범주**        | **수입 (결과)** |
|-----------------|------------|
| Less than $40K  | 1          |
| $40K - $60K     | 2          |
| $60K - $80K     | 3          |
| $80K - $120K    | 4          |
| $120K +         | 5          |
| Unknown         | 0          |


### 교육 수준
| **교육수준**        | **매핑된 값 (결과)** |
|-----------------|----------------|
| Unknown  (알려지지 않음)      | 0              |
| Uneducated (중졸 이하)    | 1              |
| High School (고졸)    | 2              |
| College  (대학 재학)      | 3              |
| Graduate  (대졸)     | 4              |
| Post-Graduate (석사 학위) | 5              |
| Doctorate  (박사 학위)    | 6              |
        """)
    
    with 탭2:
        pass
#         st.subheader("🕶️ 이상치 탐색")
#         st.markdown("""
# ### 이상치 처리 
# - RobustScaler 
#     - 중앙값을 기준으로 IQR 방식을 사용하여 스케일링
#     - 중앙값과 사분위수를 사용하므로 이상치에 민감하지 않음
# - 은행 데이터에서 금액 관련 변수는 분포의 편차가 크고 이상치의 영향이 커 RobustScaler를 적용하였다.
# 이상치로 판단되는 값을 제거하기에는 데이터 손실 우려가 있어, 보존한 상태에서 정규화 처리하였다. 
#         """)

#         # 버튼 클릭 여부 확인
#         show_outlier = st.button('전처리 이후 데이터 박스플롯 확인')

#         if not show_outlier:
#             # 수치형 컬럼 추출
#             num_col = df1.select_dtypes(include='number').columns
            
#             # 박스플롯 시각화
#             fig = plt.figure(figsize=(15, 10))
#             for idx, col in enumerate(num_col):
#                 ax = fig.add_subplot(4, 5, idx + 1)
#                 sns.boxplot(y=df1[col], ax=ax)
#                 ax.set_title(col)
#                 ax.set_ylabel('')
            
#             fig.suptitle("전처리 이전 수치형 변수 박스 플롯", fontsize=16)
#             plt.tight_layout()
#             st.pyplot(fig)
#         else:
#             # 수치형 컬럼 추출
#             num_col = df.select_dtypes(include='number').columns
            
#             # 박스플롯 시각화
#             fig = plt.figure(figsize=(15, 10))
#             for idx, col in enumerate(num_col):
#                 ax = fig.add_subplot(4, 5, idx + 1)
#                 sns.boxplot(y=df[col], ax=ax)
#                 ax.set_title(col)
#                 ax.set_ylabel('')
            
#             fig.suptitle("전처리 이후 수치형 변수 박스 플롯", fontsize=16)
#             plt.tight_layout()
#             st.pyplot(fig)
      
    with 탭3:
        pass
#         st.subheader("🔗 상관관계")
#         st.markdown("""
# - 데이터 간의 강한 상관관계를 띄는 변수가 존재함
# - 상관관계가 0.5이상인 변수들을 제거
#         """)
#         # 페이지 제목
#         st.title('상관 관계 히트맵')
        
#         # 버튼 클릭 여부 확인
#         show_df1 = st.button('전처리 이후 데이터 상관관계 확인')
        
#         if not show_df1:
#             # df 데이터에서 상관계수 계산
#             columns_to_select1 = ['평균사용가능금액', '평균이용률', '총거래횟수', '카드보유년',
#                                   '부양가족수', '신용한도', '회전잔액', '총거래금액', '수입',
#                                   '교육수준', '총거래관계수', '12개월비활성개월수', '12개월고객접촉횟수']
#             df_selected = df1[columns_to_select1]
            
#             corr = df_selected.corr()
        
#             fig, ax = plt.subplots(figsize=(10, 8))
#             sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
#             plt.title("DF 데이터 처리전  상관 관계 히트맵")
#             st.pyplot(fig)
        
#         else:
#             # df1 데이터에서 상관계수 계산
#             columns_to_select = ['부양가족수', '신용한도', '회전잔액', '총거래금액',
#                                  '수입', '교육수준', '총거래관계수', '12개월비활성개월수', '12개월고객접촉횟수']
#             df1_selected = df[columns_to_select]
            
#             corr = df1_selected.corr()
        
#             fig, ax = plt.subplots(figsize=(10, 8))
#             sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
#             plt.title("DF 데이터 처리 후 상관 관계 히트맵")
#             st.pyplot(fig)
    
    with 탭4:
        pass
#         st.subheader("🎢 클래스 불균형")
#         st.markdown("""
# ### 🎢 클래스 불균형 해소
# - 원본 데이터에서 이탈 여부는 약 8 : 2이다
# - 이런 클래스 불균형 상황에서는 분류 모델의 성능이 떨어질 수 있다
# - 이를 해소하기 위해 Train 데이터 셋에서 SMOTE을 이용한 오버 샘플링을 진행했다.
#         """)

#         # 버튼 클릭 여부 확인
#         show_smote = st.button('클래스 불균형 확인')
        
#         if not show_smote:
#             # df 데이터에서 상관계수 계산
              
#             # 이탈여부 시각화
#             fig = plt.figure(figsize=(6, 4))
#             sns.countplot(data=df, x="이탈여부")
#             plt.title("이탈 여부 분포")
#             plt.xlabel("이탈여부 (0: 유지, 1: 이탈)")
#             plt.ylabel("고객 수")
#             plt.grid(True, linestyle="--", alpha=0.3)
#             plt.show()
#             st.pyplot(fig)
        
#         else:
#             y_train_df = pd.DataFrame(y_train)
#             fig = plt.figure(figsize=(6, 4))
#             sns.countplot(data=y_train_df, x="이탈여부")
#             plt.title("이탈 여부 분포")
#             plt.xlabel("이탈여부 (0: 유지, 1: 이탈)")
#             plt.ylabel("고객 수")
#             plt.grid(True, linestyle="--", alpha=0.3)
#             plt.show()
#             st.pyplot(fig)

elif menu == "모델 학습":
    # 탭 생성
    # 그래프 탭 추가 (예: tab5)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📘 기본 모델 성능",
        "📙 튜닝 모델 성능",
        "📗 AutoML 모델 성능",
        "📊 기본 vs 튜닝 모델 비교",
        "📈 모델별 f1 score 비교"
    ])
    # f1_test만 추출
    f1_nomal = nomal_df["f1_test"]
    f1_tuning = tuning_df["f1_test"]
    f1_automl = automl_df["f1_test"]
    with tab1:
        st.subheader("📘 기본 모델 성능")
        st.dataframe(nomal_df, use_container_width=True)

        st.markdown("### 📊 기본 모델별 f1 score")
        
        fig1 = px.bar(nomal_df,
                      x="Model", y="f1_test",
                      text_auto=True,
                      title="기본 모델의 F1 Score")
        fig1.update_layout(xaxis_title="모델", yaxis_title="F1 Score", title_x=0.5)

        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        st.subheader("📙 튜닝 모델 성능")
        st.dataframe(tuning_df, use_container_width=True)

        st.markdown("### 📊 튜닝 모델별 f1 score")

        fig2 = px.bar(tuning_df,
                      x="Model", y="f1_test",
                      text_auto=True,
                      title="튜닝 모델의 F1 Score")
        fig2.update_layout(xaxis_title="모델", yaxis_title="F1 Score", title_x=0.5)

        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.subheader("📗 AutoML 모델 성능")
        st.dataframe(automl_df, use_container_width=True)

        st.markdown("### 📊 AutoML 주요 성능 지표")

        metrics_to_plot = ["f1_test", "accuracy_test", "precision_test", "recall_test", "roc_auc_test"]

        for metric in metrics_to_plot:
            fig = px.bar(automl_df,
                         x="Model", y=metric,
                         text_auto=True,
                         title=f"AutoML 모델의 {metric} 지표")
            fig.update_layout(xaxis_title="모델", yaxis_title=metric.upper(), title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("📈 기본 vs 튜닝 모델 성능 향상률 (%)")
    
        metrics = ["f1_cv", "accuracy_cv", "precision_cv", "roc_auc_cv", "recall_cv",
                   "f1_test", "accuracy_test", "precision_test", "roc_auc_test", "recall_test"]
        
        # 향상률 계산
        improvement_df = ((tuning_df[metrics] - nomal_df[metrics]) / nomal_df[metrics]) * 100
        improvement_df = improvement_df.round(2).astype(str) + '%'

        # 모델 컬럼 삽입
        improvement_df.insert(0, "Model", nomal_df["Model"])
        
        # 데이터 프레임 출력
        st.dataframe(improvement_df, use_container_width=True)

        st.markdown("### 📊 모델별 f1 score (튜닝 전 vs 튜닝 후)")

        # 시각화를 위한 데이터 준비
        f1_compare_df = pd.DataFrame({
            "Model": nomal_df["Model"],
            "튜닝 전 (f1_test)": nomal_df["f1_test"],
            "튜닝 후 (f1_test)":  tuning_df["f1_test"]
        })
        

        # melt 해서 long-form으로 변환
        f1_long_df = f1_compare_df.melt(id_vars="Model", 
                                        value_vars=["튜닝 전 (f1_test)", "튜닝 후 (f1_test)"],
                                        var_name="구분", value_name="F1 Score")

        # 시각화
        fig = px.bar(f1_long_df,
                     x="Model", y="F1 Score", color="구분",
                     barmode="group", text_auto=True,
                     title="모델별 F1 Score 비교 (튜닝 전 vs 튜닝 후)")
        fig.update_layout(xaxis_title="모델", yaxis_title="F1 Score", title_x=0.5)

        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.subheader("📗 튜닝 모델 vs AutoML 모델 F1 Score 비교")
        
        # 튜닝 모델 수에 맞게 AutoML f1 score 반복
        automl_f1_score = automl_df['f1_test'].values[0]  # 단일 값 추출
        repeated_automl_scores = [automl_f1_score] * len(tuning_df)  # 튜닝 모델 수만큼 반복
    
        # f1_test 지표를 기준으로 비교
        f1_comparison_df = pd.DataFrame({
            'Model': tuning_df['Model'],  # 모델 이름
            'Tuning F1 Score': tuning_df['f1_test'],  # 튜닝 모델 f1 score
            'AutoML F1 Score': repeated_automl_scores  # 반복된 AutoML f1 score
        })
        st.write(f1_comparison_df)
        
        # Plotly로 bar chart 그리기
        fig_f1_comparison = px.bar(f1_comparison_df,
                                   x='Model', y=['Tuning F1 Score', 'AutoML F1 Score'],
                                   barmode='group',  # 각 모델에 대해 두 막대 그래프 표시
                                   title='튜닝 모델 vs AutoML 모델 F1 Score 비교',
                                   text_auto=True)  # 수치 표시 추가
    
        fig_f1_comparison.update_traces(textposition='outside')
        
        fig_f1_comparison.update_layout(
            xaxis_title="모델", 
            yaxis_title="F1 Score", 
            title_x=0.5,
            xaxis_tickangle=-45
        )
        
        # 그래프 출력
        st.plotly_chart(fig_f1_comparison, use_container_width=True)
        
elif menu == "모델 평가":
    pass
#     tab1, tab2, tab3, tab4 = st.tabs(["confusion-matrix","ROC곡선","변수별 중요도","변수 별 이탈여부"])
    
#     with tab1:
#         st.subheader("confusion-matrix")
#         # 예측 수행
        
#         # 혼동 행렬 계산
#         cm = confusion_matrix(bank_test['target'], pred)
        
#         # Streamlit 시각화
#         fig, ax = plt.subplots(figsize=(8, 5))
#         sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
#                     xticklabels=['Pred 0', 'Pred 1'],
#                     yticklabels=['Actual 0', 'Actual 1'],
#                     ax=ax)
#         ax.set_xlabel('Predicted')
#         ax.set_ylabel('Actual')
#         ax.set_title('Confusion Matrix')
#         st.pyplot(fig)

#         st.markdown("### 📊 Score Summary")
#         st.markdown(f"""
# ### **Accuracy** : `{accuracy_score(bank_test['target'], pred):.4f}` 
# ### **F1 Score** : `{f1_score(bank_test['target'], pred):.4f}`       
# ### **Recall Score** : `{recall_score(bank_test['target'], pred):.4f}`   
# ### **Precision Score** : `{precision_score(bank_test['target'], pred):.4f}`
#         """)
        
#     with tab2:
#         st.subheader("ROC곡선")

#         # ROC 곡선 계산
#         fpr, tpr, thresholds = roc_curve(bank_test['target'], proba[1])
        
#         # 그래프 그리기
#         fig, ax = plt.subplots(figsize=(8, 6))
#         ax.plot(fpr, tpr, color='red', lw=2, label='ROC 곡선')
#         ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='무작위 예측')
#         ax.set_xlabel('False Positive Rate')
#         ax.set_ylabel('True Positive Rate')
#         ax.set_title('Receiver Operating Characteristic (ROC)')
#         ax.legend()
        
#         # Streamlit에 출력
#         st.pyplot(fig)

#         st.markdown(f"### ROC AUC Score: `{roc_auc_score(bank_test['target'], pred):.4f}`")

#    with tab3:
        # st.subheader("변수별 중요도")
        
        # # feature_importance() 호출 시, X_test만 전달
        # feature_importance = model.feature_importance(bank_test)
        # print("Feature importance for LightGBMLarge model:")
        # print(feature_importance)
        
        # # 변수 이름과 중요도를 정렬하여 시각화
        # importance_df = feature_importance.sort_values(by="importance", ascending=False).head(10)
        
        # # 변수 중요도 시각화
        # fig, ax = plt.subplots(figsize=(10, 6))
        # ax.barh(importance_df.index, importance_df['importance'], color='skyblue')
        # ax.set_xlabel('Feature Importance')
        # ax.set_ylabel('Feature')
        # ax.set_title('Feature Importance for LightGBMLarge Model')
        # ax.invert_yaxis()  # 중요도가 높은 순으로 표시
        
        # # Streamlit에 그래프 출력
        # st.pyplot(fig)

#    with tab4:
        # df2['이탈여부'] = df2['이탈여부'].replace({0: '유지', 1: '이탈'})
        # feature = st.selectbox("분석할 변수 선택", ['나이', '결혼여부', '총거래금', '회전잔액'])
        
        # fig2, ax2 = plt.subplots()
        
        # if feature == '나이':
        #     df2['recovered_feature'] = df2['나이그룹'].astype(str)
        
        # elif any(feature in col for col in df2.columns if feature != '나이'):
        #     features = [col for col in df2.columns if feature in col]
        
        #     if len(features) > 1:
        #         # 원핫 인코딩된 범주형 처리
        #         df2['recovered_feature'] = df2[features].idxmax(axis=1).str.replace(f'{feature}_', '')
        #     else:
        #         # 단일 컬럼 범주형
        #         df2['recovered_feature'] = df2[features[0]]
        
        #     # 문자열로 변환 (정렬 목적)
        #     df2['recovered_feature'] = df2['recovered_feature'].astype(str)
        
        # # 범주형: barplot
        # if feature == '나이' or len(features) > 1:
        #     grouped = df2.groupby(['recovered_feature', '이탈여부']).size().reset_index(name='count')
        #     sns.barplot(data=grouped, x='recovered_feature', y='count', hue='이탈여부', ax=ax2)
        #     ax2.set_title(f'{feature} 별 이탈여부 분포 (범주형)')
        
        # # 연속형: histplot
        # else:
        #     sns.histplot(data=df2, x=features[0], hue='이탈여부', bins=30, alpha=0.6, ax=ax2)
        #     ax2.set_title(f'{feature} 별 이탈여부 분포 (연속형)')
        
        # st.pyplot(fig2)


elif menu == "모델 추론":
    pass
    
elif menu == "마무리":
    st.markdown("""
## 🏢 은행 입장에서의 이점

- 이탈 위험이 높은 고객을 미리 파악해 타겟 맞춤형 프로모션을 제공할 수 있음
- 맞춤형 금융상품 추천으로 고객 충성도를 높이고 이탈을 방지할 수 있음

## 🙇‍♀️ 소비자 입장에서의 이점

- 본인의 은행 이용 패턴에 맞는 혜택을 제공받을 수 있음
- 개선된 고객 경험을 얻을 수 있음
""")
