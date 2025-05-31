import csv
import time
from googleapiclient.discovery import build

# ===== 사용자 설정 =====
API_KEY = "*************************"             # 자신의 YouTube Data API 키 입력
CHANNEL_ID = "UCRO-l6Fli7rtpY2O9Y5NIzw"                # 국가유산채널(또는 분석할 채널)의 채널 ID
OUTPUT_CSV = "youtube_playlist.csv"      # 저장할 CSV 파일 이름
# ========================

def get_youtube_service(api_key):
    """YouTube Data API 클라이언트 생성"""
    return build('youtube', 'v3', developerKey=api_key)

def fetch_playlists(youtube, channel_id):
    """
    해당 채널의 재생목록 정보를 모두 가져와 리스트로 반환.
    (재생목록 제목, 재생목록 ID 등)
    """
    playlists = []
    page_token = None

    while True:
        response = youtube.playlists().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=page_token
        ).execute()

        for item in response.get('items', []):
            playlist_id = item['id']
            playlist_title = item['snippet']['title']
            playlists.append((playlist_id, playlist_title))

        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return playlists

def fetch_playlist_items(youtube, playlist_id):
    """
    특정 재생목록(playlist_id)에 있는 모든 영상(playlistItem) 정보를 가져옴.
    (영상 ID, 영상 제목 등)
    """
    items = []
    page_token = None

    while True:
        response = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token
        ).execute()

        for item in response.get('items', []):
            snippet = item['snippet']
            video_id = snippet['resourceId']['videoId']
            video_title = snippet['title']
            items.append((video_id, video_title))

        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return items

def fetch_video_details(youtube, video_id):
    """
    영상의 세부 정보를 조회하여,
    - 등록 일자(publishedAt)
    - 댓글 수(commentCount)를 반환
    """
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    items = response.get('items', [])
    if not items:
        return None, None  # 해당 영상 정보가 없을 경우

    video_snippet = items[0].get('snippet', {})
    video_statistics = items[0].get('statistics', {})

    published_date = video_snippet.get('publishedAt', None)
    comment_count = video_statistics.get('commentCount', 0)

    return published_date, comment_count

def main():
    youtube = get_youtube_service(API_KEY)

    # 1. 채널 내 모든 재생목록 정보를 가져옴
    playlists = fetch_playlists(youtube, CHANNEL_ID)

    # 2. CSV 파일 열기
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # CSV 헤더
        writer.writerow(["재생목록", "영상제목", "등록 일자", "댓글 수"])

        # 3. 각 재생목록을 순회하며 재생목록 아이템(영상) 정보 수집
        for playlist_id, playlist_title in playlists:
            playlist_items = fetch_playlist_items(youtube, playlist_id)

            for video_id, video_title in playlist_items:
                # 4. 영상 세부 정보를 조회
                published_date, comment_count = fetch_video_details(youtube, video_id)

                # 5. CSV에 한 줄씩 기록
                writer.writerow([
                    playlist_title,
                    video_title,
                    published_date,
                    comment_count
                ])

                # API 호출 제한이나 네트워크 안정성을 위해 필요 시 딜레이 추가 가능
                time.sleep(0.1)

    print(f"CSV 파일 생성 완료: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()