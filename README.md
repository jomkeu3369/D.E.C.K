# AI 기반 실시간 선박 표면 검사 시스템
2025 k-조선 해커톤 참가를 위한 "D.E.C.K(Deep-learning Enhanced K-shipbuilding)" 팀의 AI 모델 레포지토리입니다.
- **참가한 공모전**: https://linkareer.com/activity/267766

## 프로젝트 개요
조선 산업의 선박 검사 과정에서 발생하는 고위험, 고비용, 비효율 문제를 해결하기 위해 개발된 인공지능 기반 실시간 표면 검사 및 진단 시스템입니다. 
CCTV, 드론, 스마트기기 등 다양한 카메라 장비로부터 영상을 입력받아 선체의 녹, 따개비, 오염물 등 각종 결함을 자동으로 탐지하고 분석하여, 최종적으로는 데이터에 근거한 해결 방안과 예상 견적까지 제시하는 통합 솔루션을 목표로 합니다.

## 주요 기능

* **실시간 결함 탐지:** 초경량 AI 모델(YOLOv8-nano-seg)을 사용하여 실시간 영상 스트림에서 선체 표면의 결함(녹, 따개비, 오염물 등)을 신속하게 탐지합니다.
* **정밀 분석 및 진단 (구현 예정):** 탐지된 결함 영역을 Image RAG 기술과 LLM을 활용하여 과거 데이터와 비교 분석하고, 결함의 종류, 심각도, 추정 원인 등을 상세히 진단합니다.
* **자동 보고서 생성 (구현 예정):** 분석 결과를 바탕으로 즉시 활용 가능한 상세 보고서 및 해결 방안(수리 가이드)을 자동으로 생성합니다.
* **확장 가능한 아키텍처:** LangGraph 기반의 워크플로우 엔진을 사용하여, 향후 다양한 AI 모델과 분석 단계를 유연하게 추가하고 관리할 수 있습니다.
* **보안 강화 (계획):** 최종적으로 모든 AI 분석 과정을 외부와 차단된 로컬 서버(On-premise) 환경에서 구동하여 데이터 보안을 확보할 계획입니다.

## 아키텍처 개요
본 시스템은 **두 개의 AI가 협력하는 2단계 방식**으로 설계되었습니다.

1.  **1단계: 신속 스캔 (YOLOv8-nano-seg)**
    * 실시간 영상 프레임에서 결함 의심 영역을 빠르게 탐지.
2.  **2단계: 정밀 분석 (Image RAG + LLM)**
    * 탐지된 영역만 잘라내어 과거 데이터베이스와 비교 분석 후, 상세 보고서 생성.

전체 워크플로우는 **LangGraph**를 통해 자동화되며, **FastAPI** 기반의 API 서버를 통해 외부 시스템과 연동됩니다. 시스템은 **Docker**로 컨테이너화되어 **AWS EC2 T2.micro**와 같은 저사양 환경에서도 효율적으로 운영될 수 있도록 최적화되었습니다.

## 기술 스택

* **Backend:** Python, FastAPI
* **AI Models:** YOLOv8 (Ultralytics)
* **Workflow Orchestration:** LangGraph (계획)
* **Data Analysis:** Image RAG, LLM (계획)
* **Dependency Management:** Poetry
* **Containerization:** Docker, Docker Compose
* **CI/CD:** GitHub Actions
  
## 시작하기

### 사전 요구 사항

* Python 3.12
* Poetry (의존성 관리 도구)
* Docker & Docker Compose (컨테이너 실행 환경)

### 설치 및 실행 (로컬)

1.  **저장소 클론:**
    ```bash
    git clone [https://github.com/jomkeu3369/shipbuild.git](https://github.com/jomkeu3369/shipbuild.git)
    cd shipbuild
    ```

2.  **Poetry 설치:**
    ```bash
    pip install poetry
    ```

3.  **의존성 설치:**
    ```bash
    poetry install --no-root
    ```

4.  **YOLO 모델 다운로드:**
    * 학습된 `best.pt` 모델 파일을 프로젝트 내 적절한 위치(예: `app/api/`)에 배치해야 합니다.
    * `app/api/router.py` 파일 상단의 `MODEL_PATH` 변수를 실제 모델 파일 경로로 수정하세요.

5.  **서버 실행 (Uvicorn):**
    ```bash
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    이제 `http://localhost:8000/docs` 로 접속하여 API 문서를 확인할 수 있습니다.

### 설치 및 실행 (Docker)

1.  **저장소 클론:** (위와 동일)
2.  **YOLO 모델 배치:** (위와 동일)
3.  **Docker 이미지 빌드 및 실행:**
    ```bash
    docker-compose up --build
    ```
    이제 `http://localhost:8080/docs` 로 접속하여 API 문서를 확인할 수 있습니다. (Dockerfile에서 포트가 8080으로 설정됨)

## 사용법

### 이미지 분석 API

* **Endpoint:** `POST /analyze/yolo`
* **Request:**
    * `file`: 분석할 이미지 파일을 `multipart/form-data` 형식으로 전송합니다.
* **Response:**
    * 성공 시: 분석 결과(결함 영역이 표시된) 이미지 파일을 반환합니다 (`image/jpeg`).
    * 실패 시: 에러 메시지를 JSON 형식으로 반환합니다.

* **예시 (curl 사용):**
    ```bash
    curl -X POST "http://localhost:8080/analyze/yolo" \
         -H "accept: image/jpeg" \
         -H "Content-Type: multipart/form-data" \
         -F "file=@/path/to/your/image.jpg;type=image/jpeg" \
         --output result_image.jpg
    ```
    
## 작동 예시
- 현재 학습 데이터셋: 110개
<img width="708" height="396" alt="KakaoTalk_20251016_004745213" src="https://github.com/user-attachments/assets/df352b94-d8c8-49a0-b123-2eb286243be9" />
