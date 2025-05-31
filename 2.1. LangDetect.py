from langdetect import detect
import pandas as pd

# 댓글 데이터 불러오기
input_path = "comments_with_titles.csv"  # 댓글 데이터 파일 경로
output_path = "filtered_comments.csv"  # 결과 파일 경로

# 데이터프레임 로드
data = pd.read_csv(input_path)

# '댓글' 컬럼의 이름을 적절히 수정하세요.
comment_column = 'comment'

def filter_language(comment):
    try:
        lang = detect(comment)  # 댓글 언어 식별
        if lang in ['ko', 'en']:  # 한국어('ko')와 영어('en')만 허용
            return True
        else:
            return False
    except:
        return False  # 오류 발생 시 삭제

# 한국어와 영어 댓글 필터링
data['Is_Korean_Or_English'] = data[comment_column].apply(filter_language)
filtered_data = data[data['Is_Korean_Or_English']]  # True인 행만 유지

# 결과 저장
filtered_data.drop(columns=['Is_Korean_Or_English'], inplace=True)  # 임시 컬럼 삭제
filtered_data.to_csv(output_path, index=False)

print(f"필터링 완료: {output_path}")