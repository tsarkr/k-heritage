import pandas as pd
from bertopic import BERTopic

# 파일 경로
file_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/cleaned_youtube_comments_with_stopwords.csv'

# 데이터 읽기
data = pd.read_csv(file_path)

# 텍스트 데이터 준비
comments = data['cleaned_comment'].dropna().tolist()

# BERTopic 모델 생성
topic_model = BERTopic(language="multilingual")  # 다국어 지원

# 토픽 모델링 수행
topics, probs = topic_model.fit_transform(comments)

# 토픽 정보 출력
print("\n### 주요 토픽 ###\n")
topic_info = topic_model.get_topic_info()
for idx, row in topic_info.head(10).iterrows():
    topic_id = row['Topic']
    topic_name = row['Name']
    print(f"토픽 {topic_id}: {topic_name}")

# 결과 저장 (토픽 정보 및 각 댓글의 토픽)
topic_info.to_csv('/Users/gyungmin/VS_PRJ/DH/k-heritage/bertopic_topic_info.csv', index=False)
print("\n토픽 정보 저장 완료: /Users/gyungmin/VS_PRJ/DH/k-heritage/bertopic_topic_info.csv")

# 각 댓글의 주요 토픽 저장
comments_with_topics = pd.DataFrame({
    "Comment": comments,
    "Topic": topics
})
comments_with_topics.to_csv('/Users/gyungmin/VS_PRJ/DH/k-heritage/comments_with_topics.csv', index=False)
print("\n댓글별 주요 토픽 저장 완료: /Users/gyungmin/VS_PRJ/DH/k-heritage/comments_with_topics.csv")

# 토픽 시각화 (HTML 파일 저장)
visualization_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/bertopic_visualization.html'
topic_model.visualize_topics().write_html(visualization_path)
print(f"\n토픽 시각화 저장 완료: {visualization_path}")