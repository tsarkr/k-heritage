from konlpy.tag import Okt
import pandas as pd

# 파일 경로
file_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/cleaned_youtube_comments_with_stopwords.csv'

# 데이터 읽기
data = pd.read_csv(file_path)

# 텍스트 데이터
comments = data['cleaned_comment'].dropna().tolist()

# 형태소 분석기 설정
okt = Okt()

# 모든 댓글을 토큰화
tokens = []
for comment in comments:
    tokens.extend(okt.morphs(comment))  # 형태소 분석기로 단어 분리

# 고유 단어의 수 (Type)와 총 단어의 수 (Token) 계산
unique_tokens = set(tokens)  # 고유 단어
num_unique_tokens = len(unique_tokens)  # 고유 단어의 수
num_total_tokens = len(tokens)  # 총 단어의 수

# TTR 계산
ttr = num_unique_tokens / num_total_tokens

# 결과 출력
print(f"총 단어 수 (Token): {num_total_tokens}")
print(f"고유 단어 수 (Type): {num_unique_tokens}")
print(f"TTR (Type-Token Ratio): {ttr:.4f}")