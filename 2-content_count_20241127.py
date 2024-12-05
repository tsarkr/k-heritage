import pandas as pd

# 파일 경로 설정
file_path = 'youtube_comments.csv'

try:
    # 데이터 읽어오기
    data = pd.read_csv(file_path)
    
    # 콘텐츠별 댓글 수 계산
    content_comment_counts = data.groupby('video_id')['comment'].count().reset_index()
    content_comment_counts.columns = ['video_id', 'comment_count']
    
    # 전체 콘텐츠 수 계산
    total_content_count = content_comment_counts['video_id'].nunique()
    
    # 전체 댓글 수 계산
    total_comment_count = content_comment_counts['comment_count'].sum()
    
    # 결과 출력
    print(f"전체 콘텐츠 수: {total_content_count}")
    print(f"전체 댓글 수: {total_comment_count}")
    print("\n콘텐츠별 댓글 수:")
    print(content_comment_counts)
    
    # 결과를 CSV 파일로 저장
    output_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/content_comment_counts.csv'
    content_comment_counts.to_csv(output_path, index=False)
    print(f"\n콘텐츠별 댓글 수를 저장한 파일 경로: {output_path}")
    
except FileNotFoundError:
    print(f"지정된 파일 경로를 찾을 수 없습니다: {file_path}")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
