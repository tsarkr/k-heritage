import re
import pandas as pd
from konlpy.tag import Okt

# (1) Okt 형태소 분석기
okt = Okt()

# (2) 불용어 리스트 (추가 확장 가능)
stopwords = set([
    # 조사 & 접사류 (조사, 어미, 접미사 등은 아래 품사 제거 단계에서도 걸러짐)
    "은", "는", "이", "가", "을", "를", "에", "와", "과", 
    "에서", "에게", "에게는", "한테", "한테는", "께", 
    "의", "하다", "됩니다", "된다", "했다", "해요",
    
    # 반복 감탄사 / 의미 없음
    "진짜", "정말", "그냥", "너무", "완전", "약간", "그래서", "근데", "그러나",
    "입니다", "인데", "있네요", "있을까요", "없는", "없나요", "같아요", "있어요", "되어다",
    
    # 유튜브 상에서 자주 나타나는 '메타' 단어
    "채널", "구독", "좋아요", "댓글", "라이브", "스트리밍",
    "보고", "봤는데", "봤습니다", "봤어요",
    # '영상'도 제거할지 말지는 데이터 목표에 따라 결정
    "영상",
    
    # 프로젝트 도메인에 따라 의미 없는 단어
    "한국", "대한민국", "서울",
    # 위처럼 의미 없는 단어는 계속 추가...
    "좋다", "있다", "보다", "되다", "같다", "우리", "자다", "오다", "멋지다", "많다", "가다", "만들다", "이다", "들다", "싶다", "이렇다", "많이",
    "없다", "아니다", "않다", "생각"
])

def clean_text_with_okt(text, remove_num_eng=True, min_token_len=2):
    """
    텍스트 전처리 & 형태소 분석:
      1) HTML 태그 제거
      2) 특수문자 제거
      3) (옵션) 숫자/영문 토큰 제거
      4) 형태소 분석 (Okt)
      5) 조사/어미/접미사/감탄사 등 불필요 품사 제거
      6) 불용어 제거
      7) (옵션) 최소 토큰 길이 필터
      8) 최종 문자열로 변환
    """
    if not isinstance(text, str):
        return ""
    
    # 1) HTML 태그 제거
    text = re.sub(r'<[^>]*>', '', text)
    
    # 2) 특수문자, 제어문자 제거
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', text)
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    
    # 3) (옵션) 숫자/영문 토큰 제거
    #    \b[a-zA-Z0-9]+\b : 순수 영어/숫자만 있는 토큰
    #    원치 않으면 이 부분 주석 처리
    if remove_num_eng:
        text = re.sub(r'\b[a-zA-Z0-9]+\b', '', text)
    
    # 다중 공백 제거
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 4) 형태소 분석 (어간추출, 정규화)
    tokens = okt.pos(text, stem=True, norm=True)
    
    # 5) 조사, 어미, 접미사, 감탄사 등 불필요 품사 제거
    #    품사 태그:
    #      Josa(조사), Eomi(어미), Suffix(접미사),
    #      Punctuation(구두점), Conjunction(접속사),
    #      Exclamation(감탄사) 등등
    filtered = [
        word for word, pos in tokens 
        if pos not in ['Josa','Eomi','Suffix','Punctuation','Conjunction','Exclamation','Foreign']
        # Foreign(외국어)도 제거하고 싶으면 추가
    ]
    
    # 6) 불용어 제거
    #    (stopwords에 넣을지, 품사 제거로 해결할지 여부는 데이터에 맞게)
    filtered = [w for w in filtered if w not in stopwords]
    
    # 7) (옵션) 최소 토큰 길이 필터
    filtered = [w for w in filtered if len(w) >= min_token_len]
    
    # 8) 결과 문자열로 합침
    return ' '.join(filtered)

# (3) CSV 불러오기
file_path = 'filtered_comments.csv'
data = pd.read_csv(file_path)

# (4) 전처리 적용
data['cleaned_comment'] = data['comment'].apply(clean_text_with_okt)

# (5) 저장
csv_path = 'cleaned_youtube_comments_with_stopwords.csv'
data.to_csv(csv_path, index=False)

print(f"CSV 저장 완료: {csv_path}")