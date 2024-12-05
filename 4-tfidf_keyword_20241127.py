import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# 데이터 파일 경로
file_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/cleaned_youtube_comments_with_stopwords.csv'

# 데이터 읽기
data = pd.read_csv(file_path)

# 텍스트 데이터
documents = data['cleaned_comment'].dropna().tolist()

# TF-IDF 벡터라이저 설정
tfidf_vectorizer = TfidfVectorizer(
    max_features=50,  # 상위 20개 키워드 추출
    stop_words='english',  # 영어 불용어 제거 (한국어 불용어는 이미 정제됨)
    max_df=0.85,  # 너무 자주 등장하는 단어 무시
    min_df=0.01  # 너무 드물게 등장하는 단어 무시
)

# TF-IDF 행렬 생성
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

# 키워드 추출
keywords = tfidf_vectorizer.get_feature_names_out()
tfidf_scores = tfidf_matrix.sum(axis=0).A1  # TF-IDF 점수 합계 계산

# 키워드와 TF-IDF 점수를 데이터프레임으로 저장
keyword_scores = pd.DataFrame({'Keyword': keywords, 'Score': tfidf_scores})
keyword_scores = keyword_scores.sort_values(by='Score', ascending=False)

# 결과 출력
print("상위 키워드:")
print(keyword_scores)

# 결과 저장
output_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/extracted_keywords.csv'
keyword_scores.to_csv(output_path, index=False)
print(f"키워드 추출 결과 저장 완료: {output_path}")