import random
from pytrends.request import TrendReq

# --- Paraphrasing (optional, for English only) ---
try:
    from transformers import pipeline
    paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")
    paraphrasing_enabled = True
except Exception:
    paraphrasing_enabled = False
    paraphraser = None


# --- Fetch trending SEO keywords ---
pytrends = TrendReq(hl='en-US', tz=330)
kw_list = ["ethnic wear", "kurti", "palazzo", "women fashion", "designer gown"]
try:
    pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='IN', gprop='')
    trending = pytrends.related_queries()
except Exception:
    trending = {}

seo_keywords = set()
for kw in kw_list:
    if kw in trending and 'top' in trending[kw] and trending[kw]['top'] is not None:
        try:
            top_df = trending[kw]['top']
            for row in top_df.to_dict('records'):
                if 'query' in row:
                    cleaned = row['query'].replace(" ", "").replace("-", "")
                    seo_keywords.add(cleaned)
        except Exception:
            pass

if not seo_keywords:
    seo_keywords = set(["Ethnic Wear", "Trendy Kurti", "Designer Palazzo", "Wedding Gown", "Women Fashion"])

seo_keywords = list(seo_keywords)

# --- Review Elements ---
products = ["Kurti", "Tunic", "Co-ord Set", "Pant Pair", "Palazzo Pair", "Aliya Pair", "Crop Top", "Gown"]
product_postfix = {
    "Kurti": {"gu": "lidhi", "hi": "li"},
    "Tunic": {"gu": "lidhu", "hi": "liya"},
    "Co-ord Set": {"gu": "lidho", "hi": "liya"},
    "Pant Pair": {"gu": "lidhi", "hi": "li"},
    "Palazzo Pair": {"gu": "lidhi", "hi": "li"},
    "Aliya Pair": {"gu": "lidhi", "hi": "li"},
    "Crop Top": {"gu": "lidhu", "hi": "liya"},
    "Gown": {"gu": "lidhu", "hi": "liya"}
}

emotions_en = ["super comfy", "stylish", "affordable", "perfect fitting", "trendy", "beautiful", "unique design", "soft fabric", "amazing quality"]
emotions_hi = ["bahut comfortable", "stylish", "affordable", "fitting mast", "trendy", "bahut sundar", "unique design", "soft fabric", "quality zabardast"]
emotions_gu = ["khub comfort che", "stylish", "sasta", "fit ekdam perfect", "trendy", "sundar", "unique design", "soft fabric", "quality mast che"]

areas = ["Surat", "Laxman Nagar", "Varachha"]
emojis = ["🌸", "😍", "👌", "✨", "💃", "🛍️", "😊", "👍", "❤️"]

starters_hi = ["", "Yaar,", "Bhai,", "Dil se bolu toh,", "Seriously,", "Kya mast collection hai,", "Wah bhai wah,", "Bilkul sahi jagah,", "Mast laga mujhe,"]
enders_hi = ["", "Fir aaungi pakka!", "Sabko recommend karungi.", "Mummy ko bhi pasand aayi.", "Aajkal sab yahin se le rahe hain.", "Thanks HK Factory Outlet!", "Next time friends ke sath aungi.", "Love it!", "Full paisa vasool."]
mid_phrases_hi = ["staff full helpful tha", "collection ek number tha", "fitting ekdum mast thi", "price bhi ekdum hu sahi he", "shop ka vibe alag hai", "service fast he", "colors mast he", "quality bhi zabardast hai", "sab kuch latest colection me hai"]

starters_gu = ["", "Maja avi gay,", "Boss, ekdam mast,", "Dil thi bolu chu,", "Yaar, su collection che,", "Full satisfied,", "Ek number,", "Sachu kav to,"]
enders_gu = ["", "Pachi pan aavish.", "Badha friends ne recommend karish.", "Mummy ne khub gamyu.", "Next time family sathe aavish.", "Thanks HK Factory Outlet!", "Full paisa vasool.", "Love it!", "Ekdam unique che."]
mid_phrases_gu = ["staff khub helpful che", "collection ek number che", "fitting mast che", "price to bov j reasonable che", "shop ni vibe kyk alag j che", "service to bov j fast che", "colors mast che", "quality pan best che", "badhu latest collection che"]

starters_en = ["", "Wow,", "Honestly,", "To be frank,", "No words,", "Guys,", "Trust me,", "Hey,", "Loved it!", "Just wow!"]
enders_en = ["", "Will buy again.", "Such a great find.", "My mom loved it too.", "Best experience ever.", "Highly recommended.", "Great for daily wear.", "Perfect for gifting.", "My friends asked where I got it.", "Must try!"]
mid_phrases_en = ["the staff was so helpful", "loved the colors", "fabric feels premium", "fit is just right", "price is reasonable", "collection is huge", "location is easy to find", "ambience is nice", "service is quick"]

# ------------------
# Generation Function
# ------------------
def generate_review(lang, product, area, emoji, keyword):
    starter, ender, mid, emotion = "", "", "", ""
    postfix = product_postfix[product][lang] if lang in ["hi", "gu"] else ""
    
    # Randomly choose the shop name
    shop_name = random.choice(["HK Factory Outlet"])
    
    if lang == "en":
        starter = random.choice(starters_en)
        ender = random.choice(enders_en)
        mid = random.choice(mid_phrases_en)
        emotion = random.choice(emotions_en)
        review = f"{starter} I bought a {product} from {shop_name} in {area}, {mid}, it's {emotion} and perfect for {keyword}. {emoji} {ender}"
    elif lang == "hi":
        starter = random.choice(starters_hi)
        ender = random.choice(enders_hi)
        mid = random.choice(mid_phrases_hi)
        emotion = random.choice(emotions_hi)
        review = f"{starter} {area} se {product} {postfix} from {shop_name}, {mid}, {emotion} aur perfect he {keyword} ke liye. {emoji} {ender}"
    elif lang == "gu":
        starter = random.choice(starters_gu)
        ender = random.choice(enders_gu)
        mid = random.choice(mid_phrases_gu)
        emotion = random.choice(emotions_gu)
        review = f"{starter} {area} mathi {product} {postfix} from {shop_name}, {mid}, {emotion} ane {keyword} mate ekdam perfect. {emoji} {ender}"
    
    return review.strip()

# ------------------
# Main Loop
# ------------------
reviews_set = set()
N = 500  # Number of reviews to generate

while len(reviews_set) < N:
    lang = random.choice(["hi", "gu", "en"])
    product = random.choice(products)
    area = random.choice(areas)
    emoji = random.choice(emojis) if random.random() > 0.2 else ""
    keyword = random.choice(seo_keywords)
    review = generate_review(lang, product, area, emoji, keyword)

    if lang == "en" and paraphrasing_enabled and random.random() > 0.5:
        try:
            review = paraphraser(review, max_length=60, num_return_sequences=1)[0]['generated_text']
        except Exception:
            pass

    reviews_set.add(review)

# ------------------
# Output
# ------------------
with open("reviews.js", "w", encoding="utf-8") as f:
    f.write("const reviews = [\n")
    for r in sorted(reviews_set):
        escaped_review = r.replace('"', '\\"')
        f.write(f'"{escaped_review}",\n')
    f.write("];")

print(f"✅ Generated {len(reviews_set)} reviews and saved to reviews.js")
