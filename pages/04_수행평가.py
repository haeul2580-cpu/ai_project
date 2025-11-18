# Re-run a focused inspection to avoid previous KeyError.
import pandas as pd
file_path = "/mnt/data/충청북도_분기별날씨현황_20250630 (1).csv"
for enc in ("utf-8","cp949","euc-kr"):
    try:
        df = pd.read_csv(file_path, encoding=enc)
        enc_used = enc
        break
    except Exception as e:
        last_err = e
print("Used encoding:", enc_used)
print("Columns:", df.columns.tolist())
display_dataframe_to_user("원본 데이터 미리보기 (상위 50행)", df.head(50))

# Show unique values of '구분' if exists
if '구분' in df.columns:
    print("구분 unique values (상위 200):")
    uniq = df['구분'].astype(str).unique()[:200]
    print(uniq)
else:
    for c in df.columns:
        print(c, "unique count:", df[c].nunique())
