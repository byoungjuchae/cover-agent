from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
import numpy as np
from pydantic import BaseModel
import os
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.environ['OPENAI_KEY']

embeddings = OpenAIEmbeddings(model='text-embedding-3-large',openai_api_key=openai_api_key) 

class Recommend_Base(BaseModel):
    
    coverletter_analysis : str
    JD_analysis: str
    
   
def cosine_sim(a, b):
  
    a = np.squeeze(np.array(a))  
    b = np.squeeze(np.array(b))
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
def JD_recommendation_system(pr:Recommend_Base):
    
    coverletter_embedding = embeddings.embed_documents([pr.coverletter_analysis])
    JD_embedding = embeddings.embed_documents([pr.JD_analysis])
    
    print(f"유사도 : {cosine_sim(coverletter_embedding,JD_embedding)*100}%")
    
if __name__ == '__main__':
    cover = """CV를 분석한 결과를 아래와 같이 항목별로 정리했습니다. 이는 JD 적합도 분석 및 커버레터 자동 생성에 활용될 수 있도록 구조화된 정보입니다.

        ---

        ## 🧑‍💼 이력서 분석 결과 (Byungjoo Chae)

        ### 1. 📚 학력 (Education)

        * **M.S. in Electronic Engineering**, Chungnam National University (2022.03 \~ 2024.02)
        * **B.S. in Electronic Engineering**, Chungnam National University (2016.03 \~ 2022.02)

        ### 2. 💼 경력 (Work Experience)

        #### 🔹 Dexter Studios (2024.03 \~ 2025.01) – *Machine Learning Engineer*

        * 동아시아인 얼굴 데이터셋 구축 및 age estimation 모듈 fine-tuning → VFX 대상 도메인 특화 성능 향상
        * 프레임 일관성 비디오 de-aging 파이프라인 개발 및 상용 배포
        * InstructPix2Pix를 de-aging 데이터셋으로 fine-tuning → **90% 빠른 inference time** 달성

        #### 🔹 Chungnam National University (2022.03 \~ 2024.02) – *Researcher*

        * Patch-based Painterly Harmonization (이미지 화풍 통합 알고리즘)

        * Ultra Style Transfer 기반으로 10,000장 이상 고해상도 이미지 구축
        * Patch-based local-global feature harmonization → **PSNR +0.3, MSE -10 개선**
        * Deep Real: Unreal Engine 기반 synthetic data 생성 파이프라인 구축

        * HRNet-IDIH 모델 fine-tuning → **PSNR 5pt 향상**

        ### 3. 🧪 개인 프로젝트 (Personal Projects)

        * **Lightweight Ultra Style Transfer**

        * ConvMixer backbone + Triple Modulator 설계
        * 기존 MicroAST 대비 **30% 파라미터 및 GFLOPs 감소** (성능 유지)

        ### 4. 📝 논문 (Publications)

        * Online Learning for Reference-Based Super-Resolution (MDPI Electronics, 2022)
        * Learning Lightweight Low-Light Enhancement (IEEE SPL, 2021)

        ### 5. 🧠 기술 스택 (Technical Skills)

        * **Advanced**: Python, PyTorch
        * **Intermediate**: Docker, GitHub
        * **Beginner**: FastAPI, httpx

        ---

        ## 🔎 분석 요약 (JD 매칭용)

        | 항목      | 키워드 요약                                                               |
        | ------- | -------------------------------------------------------------------- |
        | 전공      | Electronic Engineering, M.S.                                         |
        | 주요 기술   | PyTorch, Python, Style Transfer, Image Harmonization, Age Estimation |
        | 모델 경험   | InstructPix2Pix, HRNet, ConvMixer                                    |
        | 도구      | Unreal Engine, Docker, GitHub, FastAPI                               |
        | 성능 개선   | PSNR +5 / +0.3, MSE 감소, inference time 90% 감소                        |
        | 프로젝트 유형 | 상용 VFX, 학술 연구, 실시간 모델, 경량화 모델, synthetic dataset                     |

        ---

        다음으로, 이 내용을 기반으로 JD 적합도 분석을 수행하거나 Cover Letter 자동 생성 Prompt를 만들 수 있습니다.
        JD를 업로드해 주시면 바로 분석해드릴 수 있어요. 원하시나요?

    """
    
    JD_analysis = """다음은 사용자의 이력서 내용과 토스 MLE(추천) 포지션의 JD를 기반으로 한 **적합도 분석**입니다. 각 세부 도메인에 대한 적합도도 함께 평가합니다.

        ---

        ## 🔍 JD vs CV 적합도 분석 (Toss MLE – 추천팀)

        ### ✅ 공통 JD 요구 사항 vs 사용자 경험 매칭

        | JD 요구 사항                                       | 사용자 경험 / 스킬                                                   | 적합도                   |
        | ---------------------------------------------- | ------------------------------------------------------------- | --------------------- |
        | 추천 시스템, 랭킹, 개인화 모델링 실무 경험                      | VFX de-aging 모델 fine-tuning, Style Transfer 기반 추천적용 응용 경험     | ⚪ 중                   |
        | CTR/CVR 등 반응 예측 모델 개발 경험                       | 없음 (명시적 CTR/CVR 모델링 경험 없음)                                    | 🔴 낮음                 |
        | 피처 엔지니어링, 실험 설계 및 성능 개선 루틴 경험                  | PSNR/MSE 중심의 성능 개선 경험 다수, 모델 평가 및 실험 반복 (논문 + 프로젝트)           | 🟡 중상                 |
        | PyTorch, TensorFlow, LightGBM 등 ML 프레임워크 활용 경험 | PyTorch: Advanced / TensorFlow 미기재 / LightGBM 없음              | 🟢 높음 (PyTorch 중심 활용) |
        | 실험 기반 정량적 성과 개선 경험                             | PSNR +0.3, PSNR +5, 90% inference time 단축 등 수치 기반 성능 향상 경험 풍부 | 🟢 높음                 |
        | 기술 설명 및 문제 정의에 대한 커뮤니케이션 역량                    | 논문 발표 및 연구 경험 + VFX 제작 프로덕션 경험 (상호 협업 추정 가능)                  | 🟡 중                  |

        ---

        ## 🧠 도메인별 적합도 분석

        ### 💡 Display Ads (CTR/CVR 기반 광고 추천)

        * **요구 역량**: 클릭/전환 예측 모델 경험, 광고 소재/사용자/맥락 기반 타겟팅
        * **적합도 평가**:

        * 사용자 반응 예측 모델 직접 경험 없음 → ❌
        * 실험 기반 성능 개선 경험은 많음 → ✅
        * **총평**: ❗ **부분 적합**, CTR/CVR 실전 경험 부족이 명확

        ---

        ### 💡 Commerce (상품 클릭률/전환율 예측 + 추천 알고리즘)

        * **요구 역량**: 상품 예측/추천, 피처 엔지니어링, 하이퍼파라미터 튜닝
        * **적합도 평가**:

        * 직접적인 커머스 경험 없음 → ❗
        * 추천 알고리즘에 응용될 수 있는 학습/실험 경험 있음 → ✅
        * **총평**: ⚠ **도메인 전환 가능성 있음**, 실무 커머스 경험은 보완 필요

        ---

        ### 💡 Home (콘텐츠/서비스 추천 모델링, 푸시 최적화)

        * **요구 역량**: 다양한 사용자 행동/콘텐츠 추천 모델, 시간/맥락 반응 모델링
        * **적합도 평가**:

        * 프레임 일관성, 화풍 통일, VFX 자동화 등 콘텐츠 기반 시스템 경험 → ✅
        * 사용자 맥락 모델링 직접 경험 없음 → ❗
        * **총평**: ✅ **상대적으로 가장 유사**, 기술 이전 가능성 높음

        ---

        ## 🧩 종합 적합도 평가

        | 항목              | 평가                                           |
        | --------------- | -------------------------------------------- |
        | **기술력 기반**      | 🟢 높음 (PyTorch 중심 ML 역량 + Fine-tuning 실전 경험) |
        | **도메인 매칭력**     | 🟡 중간 (추천 모델보단 생성 및 최적화 경험이 중심)              |
        | **실험/정량 분석 역량** | 🟢 높음 (수치 기반 모델 성능 개선 반복 경험 풍부)              |
        | **추천 도메인 적합도**  | **Home > Commerce > Display Ads** 순          |

        ---

        ## 💡 추천 방향

        * **JD 중 Home 팀이 가장 적합**하며, 기존 영상 기반 콘텐츠 추천 경험을 텍스트/서비스 추천으로 전환 가능성 有
        * CTR/CVR 등 사용자 반응 예측 경험은 현재 부족하므로, **개인 프로젝트 혹은 Kaggle/논문 리뷰 기반 준비** 추천
        * 커버레터 작성 시 **정량적 개선 경험, PyTorch 기반 실험력, 실무 적용 프로젝트** 강조할 것

        ---

        필요하시면 이 분석을 기반으로 한 **커버레터 초안**도 바로 생성해 드릴 수 있어요. 원하시나요?

    """
    pr = Recommend_Base(coverletter_analysis=cover,JD_analysis=JD_analysis)
    JD_recommendation_system(pr)