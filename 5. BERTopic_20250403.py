import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from sklearn.cluster import KMeans

class KMeansWrapper:
    def __init__(self, n_clusters=10, random_state=None):
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)

    def fit(self, X, y=None):
        labels = self.kmeans.fit_predict(X)
        self.labels_ = labels
        return self

    def fit_predict(self, X):
        return self.kmeans.fit_predict(X)

def main():
    # 파일 경로
    file_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/cleaned_youtube_comments_with_stopwords.csv'
    
    # 데이터 읽기
    data = pd.read_csv(file_path)
    comments = data['cleaned_comment'].dropna().tolist()

    # (1) Ko-SBERT 모델 로드
    model_name = "klue/bert-base"
    print(f"Embedding 모델 로드 중: {model_name}")
    embedding_model = SentenceTransformer(model_name)

    # (2) UMAP & KMeans 파라미터 설정
    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric='cosine',
        random_state=42
    )
    kmeans_model = KMeansWrapper(n_clusters=10, random_state=42)

    # (3) BERTopic 모델 생성
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=kmeans_model,
        language="multilingual"
    )

    # (4) 토픽 모델링
    topics, probs = topic_model.fit_transform(comments)

    # (5) 토픽 정보 출력
    print("\n### 주요 토픽 ###\n")
    topic_info = topic_model.get_topic_info()
    for _, row in topic_info.head(10).iterrows():
        print(f"토픽 {row['Topic']}: {row['Name']}")

    # (6) 토픽 정보 저장
    topic_info_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/bertopic_topic_info.csv'
    topic_info.to_csv(topic_info_path, index=False)
    print(f"\n토픽 정보 저장 완료: {topic_info_path}")

    # (7) 댓글별 토픽 저장
    comments_with_topics = pd.DataFrame({
        "Comment": comments,
        "Topic": topics
    })
    comments_topics_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/comments_with_topics.csv'
    comments_with_topics.to_csv(comments_topics_path, index=False)
    print(f"\n댓글별 주요 토픽 저장 완료: {comments_topics_path}")

    # (8) 시각화 (상위 10개 토픽)
    try:
        top_10_topics = topic_info.head(10)['Topic'].tolist()
        custom_visualization = topic_model.visualize_topics(topics=top_10_topics)
        visualization_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/bertopic_visualization.html'
        custom_visualization.write_html(visualization_path)
        print(f"\n토픽 시각화 저장 완료: {visualization_path}")
    except Exception as e:
        print(f"\n시각화 중 오류 발생: {e}")


# ★ 중요 ★
# Python 스크립트로 실행 시, 아래와 같은 구조가 필요.
if __name__ == '__main__':
    main()