# training-pipeline
[![Airflow](https://img.shields.io/badge/Airflow-2.x-blue?logo=apache-airflow)](https://airflow.apache.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.x-lightgrey?logo=mlflow)](https://mlflow.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://www.docker.com/)

이 레포지토리는 Airflow, MLflow, PostgreSQL을 활용한 실용적인 MLOps 파이프라인 예제를 담고 있습니다. 각 프로젝트에서 필요한 모델을 훈련하고, 데이터 전처리부터 학습, 로깅까지의 과정을 Airflow DAG를 통해 자동화합니다. 모든 구성 요소는 Docker로 컨테이너화되어 재현 가능하게 연결되어 있으며, 경량화된 MLOps 템플릿으로 활용할 수 있습니다.

---

## 실행 방법

```bash
# 1. 레포지토리 클론
git clone https://github.com/Habonit/training-pipeline.git

# 2. 프로젝트 디렉토리로 이동
cd training-pipeline

# 3. 환경변수 설정
# openai API 키 포함한 .env-api → .env 복사
cp .env-api .env

# airflow, mlflow, postgres 전용 env 파일 복사
cp airflow/.env.example airflow/.env
cp mlflow/.env.example mlflow/.env
cp postgres/.env.example postgres/.env

# 4. 도커 컴포즈 실행
docker compose up -d --build
```