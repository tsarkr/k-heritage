import re
import pandas as pd

# 불용어 리스트 정의
stopwords = set(["저", "수", "들", "이", "있다니", "너무", "하다", "로", "을", "에", "는", "을", "가", "도", "의", "있", "니다", "신청"])

def clean_text(text):
    """
    텍스트 정제 함수:
    1. HTML 태그 제거
    2. 특수문자 및 허용되지 않는 문자 제거
    3. 공백 통합
    4. 불용어 제거
    """
    if not isinstance(text, str):  # 문자열이 아닐 경우 빈 문자열 반환
        return ""
    
    # 1. HTML 태그 제거
    text = re.sub(r'<[^>]*>', '', text)
    
    # 2. 특수문자 및 허용되지 않는 문자 제거
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', text)  # 특수문자 제거
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)  # Excel에서 허용되지 않는 제어 문자 제거
    
    # 3. 공백 통합
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 4. 불용어 제거
    words = text.split()
    words = [word for word in words if word not in stopwords]
    text = ' '.join(words)
    
    return text

# 데이터 불러오기
file_path = '/Users/gyungmin/VS_PRJ/DH/k-heritage/youtube_comments.csv'
data = pd.read_csv(file_path)

# 텍스트 정제 적용
data['cleaned_comment'] = data['comment'].apply(clean_text)

# 정제된 데이터 저장 (CSV 및 Excel 파일)
csv_path = 'cleaned_youtube_comments_with_stopwords.csv'

# 저장
data.to_csv(csv_path, index=False)

# CSV 저장 완료 출력
print(f"CSV 저장 완료: {csv_path}")
