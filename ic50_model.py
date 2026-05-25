import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. 엑셀 데이터 불러오기
df = pd.read_excel('ic50_data.xlsx')
print("=== 입력된 IC50 Raw Data ===")
print(df)

# 2. 4PL(4-Parameter Logistic) 방정식 정의
# a: Top (최대 생존율, 100 근처)
# d: Bottom (최소 생존율, 0 근처)
# c: IC50 (생존율이 절반이 되는 농도 ★우리가 찾을 값!)
# b: Hill slope (곡선의 기울기)
def four_pl(x, a, d, c, b):
    return d + (a - d) / (1 + (x /c)**b)

# 3. 계산을 위한 데이터 준비
# 약물 농도(X축)와 세포 생존률(Y축) 데이터를 파이썬 수학 모듈이 계산하기 좋게 꺼냅니다.
x_data = df['Concentration_nM'].values
y_data = df['Viability_percent'].values

# 4. 곡선 피팅 (Curve Fitting) 및 IC50 계산
# 초기 추정치 설정: [Top, Bottom, IC50, Hill slope] 대략적인 시작값을 파이썬에게 알려줍니다.
initial_guess = [100, 0, 10, 1]

# curve_fit 함수가 수만 번의 계산을 통해 실제 데 이터와 가장 오차가 적은 최적의 4PL 파라미터를 찾아냅니다!
popt, pcov = curve_fit(four_pl, x_data, y_data, p0=initial_guess)

#찾아낸 최적의 값들 중 세 번째(인덱스 2) 값이 바로 IC50 입니다.
ic50_value = popt[2]
print(f"\n[분석 완료] 산출된 IC50 값은 : {ic50_value:.2f} nM 입니다!")

# 5. 고해상도 시각화 (S자 곡선 그리기)
plt.figure(figsize=(8, 6))

# 1) 실제 실험 데이터는 '빨간색 동그라미 점'으로 찍기
plt.scatter(x_data, y_data, color='red', s=50, label='Raw Data (RPT_alpha)', zorder=5)

# 2) 파이썬이 계산한 4PL 수학 모델은 '파란색 부드러운 곡선'으로 그리기
# 부드러운 선을 그리기 위해 X축(농도)을 100개로 촘촘하게 쪼갭니다. (로그 스케일 기준)
x_curve = np.logspace(np.log10(min(x_data)), np.log10(max(x_data)), 100)
y_curve = four_pl(x_curve, *popt) #촘촘한 X값들에 대해 최적화된 방식으로 Y값을 계산
plt.plot(x_curve, y_curve, color='blue', linewidth=2, label=f'4L Fit (IC50 = {ic50_value:.2f} nM ')

# 6. 그래프 디테일 꾸미기
plt.xscale('log') #약물 농도는 10배씩 커지므로 X축을 '로그 스케일'로 설정
plt.title('In vitro Cell Viability (4PL Model)', fontsize=16, fontweight='bold')
plt.xlabel('Concentration(nM) - Log Scale', fontsize=12)
plt.ylabel('Cell Viability (%)', fontsize=12)
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.3) # 희미한 격자무늬 추가
plt.tight_layout()

# 7. 결과 이미지 저장 및 띄우기
plt.savefig('ic50_result.png', dpi=300)
plt.show()
