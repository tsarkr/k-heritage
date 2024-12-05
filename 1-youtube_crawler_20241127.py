import googleapiclient.discovery
import pandas as pd
import time

# YouTube Data API 키 설정
API_KEY = 'YOUTUBE_API'  # API 키는 실제 키로 교체하세요
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

def execute_request(request, retries=5, delay=1):
    """API 요청 실행, 재시도 로직 포함."""
    for i in range(retries):
        try:
            return request.execute()
        except googleapiclient.errors.HttpError as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise

def get_all_video_ids(channel_id):
    """채널의 모든 동영상 ID 가져오기."""
    video_ids = []
    response = execute_request(youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ))
    
    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    nextPageToken = None
    
    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )
        response = execute_request(request)
        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
        
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
        time.sleep(1)
    
    print(f"총 {len(video_ids)}개의 동영상 ID를 가져왔습니다.")
    return video_ids

def get_comments(video_id):
    """특정 동영상의 댓글 가져오기."""
    comments = []
    nextPageToken = None
    
    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            pageToken=nextPageToken
        )
        
        try:
            response = execute_request(request)
        except googleapiclient.errors.HttpError as e:
            print(f"Error with video ID {video_id}: {e}")
            break
    
        for item in response.get('items', []):
            # 댓글 정보 추출
            comment_snippet = item['snippet']['topLevelComment']['snippet']
            comment_data = {
                "video_id": video_id,
                "comment": comment_snippet['textDisplay'],
                "author": comment_snippet.get('authorDisplayName', "Unknown"),
                "published_at": comment_snippet.get('publishedAt', "Unknown"),
                "like_count": comment_snippet.get('likeCount', 0),
            }
            comments.append(comment_data)
    
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
        time.sleep(1)
    
    return comments

def collect_channel_comments(channel_id):
    """채널의 모든 동영상 댓글 수집."""
    video_ids = get_all_video_ids(channel_id)
    all_comments = []
    
    for idx, video_id in enumerate(video_ids, 1):
        print(f"Processing video {idx}/{len(video_ids)}: {video_id}")
        try:
            comments = get_comments(video_id)
            all_comments.extend(comments)
        except Exception as e:
            print(f"Skipping video ID {video_id} due to error: {e}")
    
    return all_comments

# 채널 ID 입력
channel_id = "UCRO-l6Fli7rtpY2O9Y5NIzw"
comments_data = collect_channel_comments(channel_id)

# 결과를 데이터프레임으로 변환하여 CSV로 저장
df = pd.DataFrame(comments_data)
df.to_csv("/Users/gyungmin/VS_PRJ/DH/k-heritage/youtube_comments.csv", index=False)
df.to_excel("/Users/gyungmin/VS_PRJ/DH/k-heritage/youtube_comments.xlsx", index=False)
print(f"댓글 수집 완료! 총 {len(comments_data)}개의 댓글을 가져왔습니다.")
