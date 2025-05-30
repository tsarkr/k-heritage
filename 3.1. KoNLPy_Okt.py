import pandas as pd
from konlpy.tag import Okt
from collections import Counter

# 파일 경로
file_path = 'cleaned_youtube_comments_with_stopwords.csv'

# 데이터 읽기
data = pd.read_csv(file_path)

# 텍스트 데이터
comments = data['cleaned_comment'].dropna().tolist()

# 형태소 분석기 설정
okt = Okt()

# 명사, 동사, 형용사 추출
nouns = []
adjectives = []

for comment in comments:
    # 명사 추출
    nouns.extend(okt.nouns(comment))
    # 품사 태깅
    tagged_words = okt.pos(comment)
    # 형용사 추출
    adjectives.extend([word for word, tag in tagged_words if tag in ('Adjective')])

# 불용어 제거 (명사 및 동사/형용사 모두 적용)
stopwords = set(["수", "것", "들", "저", "있", "되", "해", "한", "되어다"])
nouns = [noun for noun in nouns if noun not in stopwords and len(noun) > 1]
adjectives = [word for word in adjectives if word not in stopwords and len(word) > 1]

# 명사 빈도 계산
noun_counts = Counter(nouns)

# 동사/형용사 빈도 계산
adjectives = Counter(adjectives)

# 상위 30개 키워드 추출
top_nouns = noun_counts.most_common(30)
adjectives = adjectives.most_common(30)

# 결과를 데이터프레임으로 저장
nouns_df = pd.DataFrame(top_nouns, columns=["Keyword", "Frequency"])
adjectives = pd.DataFrame(adjectives, columns=["Keyword", "Frequency"])

# 결과 출력
print("상위 명사 키워드:")
print(nouns_df)
print("\n상위 형용사 키워드:")
print(adjectives)

# 결과 저장
nouns_output_path = 'extracted_nouns_konlpy.csv'
adjectives_output_path = 'extracted_adjectives_konlpy.csv'

nouns_df.to_csv(nouns_output_path, index=False)
adjectives.to_csv(adjectives_output_path, index=False)

print(f"명사 키워드 추출 결과 저장 완료: {nouns_output_path}")
print(f"형용사 키워드 추출 결과 저장 완료: {adjectives_output_path}")
