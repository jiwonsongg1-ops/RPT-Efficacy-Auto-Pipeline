# 🧪 RPT Efficacy Data Automation Pipeline
> **"Precision in Tech, Warmth in Service"**
> 생명과학 연구의 깊이에 IT 데이터 제어 기술의 정밀함을 더하여, 방대한 약효 평가 데이터를 오차 없이 분석하는 자동화 시스템입니다.

## 📌 Project Overview
전임상 연구(In vitro/In vivo) 과정에서 도출되는 방대한 약효 평가 데이터를 수동으로 처리하며 발생하는 휴먼 에러를 방지하고, 데이터 분석의 정확도와 속도를 극대화하기 위해 파이썬(Python) 기반의 데이터 자동화 파이프라인을 구축했습니다.

## 🚀 Key Features
1. **In vivo 종양 부피 시각화 자동화 (`tumor_plot.py`)**
   - 날짜 및 그룹별 종양 부피(Tumor Volume) 데이터를 인식하여 평균 및 표준편차 오차막대(Error bar)가 포함된 고해상도 그래프를 즉시 시각화합니다.
2. **In vitro IC50 4PL 수학적 모델링 (`ic50_model.py`)**
   - 약물 농도에 따른 세포 생존율 데이터를 바탕으로 `SciPy`를 활용해 4-Parameter Logistic(4PL) 방정식에 피팅합니다.
   - S자 곡선 시각화 및 최적의 IC50 값을 수학적으로 역산출합니다.
3. **Master Pipeline 통합 및 요약 (`master_pipeline.py`)**
   - 특정 폴더(`Raw_Data`) 내의 데이터 성격을 자동으로 분류하고 분석을 수행한 뒤, 최종 그래프 이미지와 IC50 요약 엑셀 파일을 일괄 생성합니다.

## 🛠 Tech Stack
- **Language:** Python
- **Data Analysis:** Pandas, NumPy, SciPy (Curve-fitting)
- **Visualization:** Matplotlib, Seaborn

## 💡 Expected Impact
이러한 깐깐한 데이터 트래킹 논리와 제어 시스템 구축 경험은 RPT(방사성의약품) 연구 과정에서 동위원소의 반감기와 선량 계산 등 유기적 변수를 추적하고 데이터 무결성을 보장하는 업무에 즉시 활용될 수 있습니다.
