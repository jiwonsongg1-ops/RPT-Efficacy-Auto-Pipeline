import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 불러오기: 엑셀 파일을 파이썬 표(DataFrame)로 변환
file_name = 'tumor_data.xlsx'
df = pd.read_excel(file_name)

# 파이썬이 데이터를 잘 읽었는지 하단에 출력해서 확인
print("=== 입력된 Raw Data 미리보기 ===")
print(df.head())

# 2. 고해상도 그래프 그리기 세팅
plt.figure(figsize=(8,6)) # 그래프 크기 설정

# 3. 핵심 알고리즘: 그룹별 평균과 오차막대(Error bar) 자동 계산 및 시각화
sns.lineplot(
    data=df,
    x='Day',
    y='Tumor_Volume_mm3',
    hue='Group',   # 그룹별로 색상을 다르게 칠함
    marker='o',    # 데이터 포인트에 동그라미 마커 표시
    err_style='bars',  # 오차막대 표시
    errorbar='sd'      # 표준편차(Standard Deviation) 기준으로 오차 계산
)

#4. 그래프 디테일 꾸미기
plt.title('In vivo Tumor Growth over Time', fontsize=16, fontweight='bold')
plt.xlabel('Days Post Treatment', fontsize=12)
plt.ylabel('Tumor Volume (mm³)', fontsize=12)
plt.legend(title='Treatment Group')
plt.tight_layout()

#5. 완성된 그래프를 고해상도 이미지(300dpi)로 자동 저장하고 화면에 띄우기
plt.savefig('tumor_growth_result.png', dpi=300)
plt.show()