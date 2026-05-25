import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

# --- 4PL 방정식 정의  ---
def four_pl(x, a, d, c, b):
    return d + (a - d) / (1 + (x / c)**b)

# --- 폴더 경로 설정 ---
input_folder = 'Raw_Data'
output_folder = 'Result'

# 폴더가 혹시 없다면 파이썬이 알아서 생성합니다.
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

print(f"[{input_folder}] 폴더에서 분석할 엑셀 파일들을 탐색합니다...\n" + "-"*40)

# 최종 IC50 요약 데이터를 모아둘 빈 리스트 (계획표 3단계용)
ic50_summary_list = []

# ======================================================================
# [계획표 1단계] 특정 폴더(Raw_Data)에 엑셀 파일을 넣으면 자동으로 인식하는 순회 로직
# ======================================================================
for file_name in os.listdir(input_folder):
    # 엑셀 파일(.xlsx)이 아니거나 임시 파일(~)이면 무시하고 넘어감
    if not file_name.endswith('.xlsx') or file_name.startswith('~'):
        continue

    file_path = os.path.join(input_folder, file_name)
    print(f"▶ 발견된 파일: {file_name}")

    # 데이터 불러오기
    df = pd.read_excel(file_path)

    # ==================================================================
    # [계획표 2단계] 인식된 파일 종류(이름)에 따라 분석 분기하는 조건문
    # ==================================================================

    # 1) 파일명에 'tumor'가 포함된 겨 ㅇ우 -> 종양 부피 시각화 파이프라인 가동
    if 'tumor' in file_name.lower():
        print("  -> [분석 1] 종양 부피 데이터로 인식하여 그래프를 생성합니다.")
        plt.figure(figsize=(8, 6))
        sns.lineplot(data=df, x='Day', y='Tumor_Volume_mm3', hue='Group',
                     marker='o', err_style='bars', errorbar='sd')

        plt.title('In vivo Tumor Growth over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Days Post Treatment', fontsize=12)
        plt.ylabel('Tumor Volume (mm³)', fontsize=12)
        plt.legend(title='Treatment Group')
        plt.tight_layout()

        # [계획표 3단계] 완성된 그래프를 Result 폴더에 저장 (화면에 띄우지 않고 자동 저장)
        save_plot_path = os.path.join(output_folder, f"plot_{file_name.replace('.xlsx', '.png')}")
        plt.savefig(save_plot_path, dpi=300)
        plt.close() # 다음 반복을 위해 도화지를 닫아줍니다.
        print(f"   -> [저장 완료] {save_plot_path}")

    # 2) 파일명에 'ic50'이 포함된 경우 -> IC50 4PL 모델링 파이프라인 가동
    elif 'ic50' in file_name.lower():
        print(" -> [분석 2] IC50 데이터로 인식하여 4PL 모델링을 시작합니다.")
        x_data = df['Concentration_nM'].values
        y_data = df['Viability_percent'].values

        initial_guess = [100, 0, 10, 1]
        popt, _ = curve_fit(four_pl, x_data, y_data, p0=initial_guess)
        calc_ic50 = popt[2]

        plt.figure(figsize=(8,6))
        plt.scatter(x_data, y_data, color='red', s=50, label='Raw Data', zorder=5)
        x_curve = np.logspace(np.log10(min(x_data)), np.log10(max(x_data)), 100)
        y_curve = four_pl(x_curve, *popt)
        plt.plot(x_curve, y_curve, color='blue', linewidth=2, label=f'4PL Fit (IC50 = {calc_ic50:.2f} nM)')

        plt.xscale('log')
        plt.title('In vitro Cell Viability (4PL Model)', fontsize=16, fontweight='bold')
        plt.xlabel('Concentration (nM) - Log Scale', fontsize=12)
        plt.ylabel('Cell Viability (%)', fontsize=12)
        plt.legend()
        plt.grid(True, which="both", ls="--", alpha=0.3)
        plt.tight_layout()

        # [계획표 3단계] 완성된 그래프를 Result 폴더에 저장
        save_plot_path = os.path.join(output_folder, f"plot_{file_name.replace('.xlsx', '.png')}")
        plt.savefig(save_plot_path, dpi=300)
        plt.close()
        print(f"  -> [저장 완료] {save_plot_path}")

        # [계획표 3단계] 요약 엑셀을 만들기 위해 계싼된 IC50 값을 리스트에 기록해 둡니다.
        ic50_summary_list.append({
            'Source_File': file_name,
            'Compound': df['Compound'].iloc[0] if 'Compount' in df.columns else 'Unknown',
            'Calculated_IC50_nM': round(calc_ic50, 2)
        })

    print("-" * 40)

    # ==================================================================
    # [계획표 3단계] IC50 결과가 정리된 새로운 엑셀 요약본 일괄 저장
    # ==================================================================
    if ic50_summary_list:
        print("IC50 분석 결과를 모아 요약 엑셀 파일을 생성합니다...")
        summary_df = pd.DataFrame(ic50_summary_list)
        summary_excel_path = os.path.join(output_folder, 'IC50_Final_Summary.xlsx')
        summary_df.to_excel(summary_excel_path, index=False)
        print(f"-> [저장 완료] 최종 요약본: {summary_excel_path}")

        print("\n 🎉모든 파이프라인 자동화 작업이 성공적으로 완료되었습니다!")