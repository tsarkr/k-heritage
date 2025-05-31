import requests
import pandas as pd

# Google API 키
API_KEY = '*********************************'  # API 키는 실제 키로 교체하세요

# 댓글 데이터 파일 경로
file_path = 'youtube_comments.csv'

# 데이터 읽기
data = pd.read_csv(file_path)

# video_id 리스트 추출 (중복 제거)
video_ids = data['video_id'].drop_duplicates().tolist()

# 영상 제목 가져오기 함수
def get_video_titles(video_ids, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    titles = {}

    for video_id in video_ids:
        params = {
            "part": "snippet",  # 영상 제목과 설명을 포함한 정보
            "id": video_id,  # 요청할 video_id
            "key": api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "items" in data and data["items"]:
                title = data["items"][0]["snippet"]["title"]
                titles[video_id] = title
            else:
                titles[video_id] = "Unknown Title"
        else:
            titles[video_id] = "Error"
    return titles

# 영상 제목 가져오기
video_titles = get_video_titles(video_ids, API_KEY)

# video_id와 제목을 DataFrame으로 변환
video_metadata = pd.DataFrame(list(video_titles.items()), columns=['video_id', 'title'])

# 댓글 데이터와 병합
merged_data = pd.merge(data, video_metadata, on='video_id', how='left')

# 결과 저장
output_path = 'comments_with_titles.csv'
merged_data.to_csv(output_path, index=False)

print(f"결과 저장 완료: {output_path}")