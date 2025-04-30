import os
# Placeholder for model-based image keyword extraction (CLIP/BLIP)
def model_based_extraction(img_path):
    """
    Placeholder function for CLIP/BLIP based image keyword extraction.
    Should return a list of keyword strings.
    """
    # TODO: implement actual model-based extraction logic
    return ["키워드1","키워드2","키워드3","키워드4","키워드5",
            "키워드6","키워드7","키워드8","키워드9","키워드10",
            "키워드11","키워드12"]

CUSTOM_WHITELIST = {
    "TS001.01.04": [
        "스탠드선반","스탠드랙","스탠드쉘프","플로어선반","바닥선반",
        "바닥수납선반","벽걸이선반","벽선반","월랙","월쉘프",
        "월마운트선반","붙박이선반","접착선반","무타공선반",
        "흡착선반","스티커선반","셀프부착선반"
    ],
    # … 다른 노드 키워드 추가 …
}

STOPWORDS = [
    "무료","특가","1+1","세일","할인","신상품","인기","베스트",
    "추천","한정","자체제작","공구","나사","볼트","배송비"
]

def dedup(keywords):
    seen = set()
    unique = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique.append(kw)
    return unique

def extract_keywords(img_path):
    kw = model_based_extraction(img_path)
    kw = [w for w in kw if w not in STOPWORDS]
    caption = " ".join(kw)
    for node, terms in CUSTOM_WHITELIST.items():
        if any(term in caption for term in terms):
            kw.insert(0, terms[0])
    return dedup(kw)[:20]
