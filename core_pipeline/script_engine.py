"""
DrawStory AI - Script Engine
Module tự động phân tích ý tưởng người dùng và sinh kịch bản chi tiết theo phân cảnh (Storyboard).
Hỗ trợ Google Gemini 1.5 Flash và cơ chế Fallback thông minh.
"""

import os
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
import json
import re
from typing import List, Dict, Any
from pydantic import BaseModel

class SceneItem(BaseModel):
    scene_id: int
    narration: str
    image_prompt: str
    keywords: List[str] = []

class StoryboardResponse(BaseModel):
    title: str
    scenes: List[SceneItem]

STORY_PROMPT_TEMPLATE = """
Bạn là một ĐẠO DIỄN VÀ BẬC THẦY KỂ CHUYỆN ĐIỆN ẢNH (phong cách dẫn chuyện lôi cuốn nghẹt thở của Netflix, Kurzgesagt, National Geographic).
Nhiệm vụ: Chuyển thể chủ đề sau đây thành một KỊCH BẢN KỂ CHUYỆN VIDEO NGẮN ĐẦY CẢM XÚC, HỒI HỘP, CÓ CÂU CHUYỆN DẪN DẮT VÀ TUYỆT ĐỐI KHÔNG KHÔ KHAN NHƯ ĐỌC BÁO CÁO.

Chủ đề: "{topic}"
Số lượng phân cảnh yêu cầu: ĐÚNG CHÍNH XÁC {scenes_count} PHÂN CẢNH.
Ngôn ngữ lời thoại: {language}.

=======================================================
🎯 QUY TẮC SỐNG CÒN CHO PHÂN CẢNH 1 (LỜI THOẠI THUYẾT MINH TTS):
=======================================================
⚠️ ĐẶC BIỆT LƯU Ý: Người xem video KHÔNG ĐỌC TIÊU ĐỀ! Họ CHỈ NGHE LỜI THOẠI THUYẾT MINH (GIỌNG ĐỌC TTS) CỦA CẢNH 1!
Nếu bạn chỉ giấu tên chủ đề trong tiêu đề ngoài mà trong lời thoại lại nói ẩn dụ chung chung, người nghe sẽ hoàn toàn không biết video nói về cái gì!

1. 🎯 TRONG CÂU ĐẦU TIÊN CỦA LỜI THOẠI CẢNH 1, BẮT BUỘC PHẢI GỌI ĐÚNG TÊN CHỦ ĐỀ "{topic}":
   - ❌ CẤM TUYỆT ĐỐI ẩn dụ bóng gió, tả cảnh vu vơ như: "Một tia sáng kinh hoàng xé toạc bầu trời, một hòn đá khổng lồ lao xuống..." (Người nghe KHÔNG BIẾT là đang nói về khủng long, thiên thạch, hay phim viễn tưởng!).
   - ✅ BẮT BUỘC PHẢI NÓI RÕ CHỦ ĐỀ NGAY CÂU ĐẦU TIÊN:
     + Ví dụ nếu chủ đề là "Tại sao khủng long tuyệt chủng":
       "Tại sao loài khủng long – kẻ thống trị Trái Đất suốt 165 triệu năm – lại đột ngột tuyệt chủng không còn một dấu vết? 66 triệu năm trước, một thiên thạch rộng 10 km đã lao thẳng xuống địa cầu với tốc độ 70.000 km/h, chôn vùi chúa tể thời tiền sử dưới biển lửa. Thế nhưng, thảm kịch kinh hoàng ấy chỉ mới là khúc dạo đầu..."
     + Ví dụ nếu chủ đề là "Sâu bướm lột xác":
       "Để sâu bướm có thể lột xác thành một cánh bướm rực rỡ, nó buộc phải tự hủy diệt chính mình: bên trong chiếc kén, toàn bộ cơ thể nó tự tan chảy thành một bãi dịch lỏng trước khi tái sinh..."
2. ❌ TUYỆT ĐỐI KHÔNG mào đầu lan man: "Bạn có bao giờ tự hỏi...", "Liệu bạn có biết rằng...", "Hãy cùng khám phá..."
3. 🔗 CUỐI CẢNH 1 PHẢI CÓ CÂU DẪN DẮT (BRIDGE) sang Cảnh 2 để cuốn người xem theo dõi tiếp.

=======================================================
🎬 NGHỆ THUẬT KỂ CHUYỆN (STORYTELLING) & CẦU NỐI DẪN DẮT CUỐN HÚT:
=======================================================
1. 🎭 BIẾN MỌI CHỦ ĐỀ THÀNH MỘT "CÂU CHUYỆN CÓ LINH HỒN" (CHỐNG KHÔ KHAN):
   - Đừng liệt kê sự thật hay định nghĩa sách giáo khoa cứng nhắc. Hãy đưa người xem vào một HÀNH TRÌNH SINH TỬ, một cuộc đối đầu cam go, hoặc số phận của một thực thể đang chiến đấu vượt qua nghịch cảnh.
   - Sử dụng từ ngữ giàu cảm giác, hình tượng thị giác sống động và nhịp điệu dồn dập.

2. 🔗 BẮT BUỘC PHẢI CÓ "CÂU NỐI DẪN DẮT KỊCH TÍNH" GIỮA CÁC PHÂN CẢNH (NARRATIVE BRIDGES):
   - Các cảnh KHÔNG ĐƯỢC rời rạc. Cảnh trước phải gieo mầm tò mò cho cảnh sau.
   - Đầu hoặc cuối mỗi cảnh thân bài BẮT BUỘC có các câu dẫn dắt tự nhiên, ví dụ:
     + "Thế nhưng, cơn ác mộng thực sự lúc này mới bắt đầu lộ diện..."
     + "Khoảnh khắc tưởng chừng đã rơi vào tuyệt vọng, một biến cố không ai ngờ tới đã đảo ngược tất cả..."
     + "Và để đổi lấy cơ hội sống sót ấy, cái giá phải trả tàn khốc hơn bất kỳ ai tưởng tượng..."

3. 🌟 CẢNH CUỐI: ĐÚC KẾT DƯ BA ÁM ẢNH, GỢI MỞ BÀI HỌC CUỘC ĐỜI:
   - Khép lại câu chuyện bằng một góc nhìn triết lý sâu sắc, liên hệ giữa biến cố vừa diễn ra với thực tại cuộc sống.

4. 📏 ĐỘ DÀI LỜI THOẠI:
   - Mỗi cảnh dài từ 38 đến 52 từ (khoảng 2-3 câu ngắn gọn, súc tích, nhịp đọc truyền cảm).

5. 🎨 PROMPT ẢNH VẼ TAY KHUNG DỌC 9:16 (image_prompt):
   - Bắt buộc là prompt TIẾNG ANH khung DỌC 9:16.
   - Đầu prompt: "Vertical 9:16 portrait composition,"
   - Cuối prompt: ", vertical orientation, full vertical view, 9:16 aspect ratio --ar 9:16"
   - Tả rõ góc máy điện ảnh, ánh sáng kịch tính, phong cách tranh màu nước vẽ tay giàu cảm xúc, nền trắng sạch sẽ.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC: DUY NHẤT một chuỗi JSON thuần túy (KHÔNG kèm markdown ```json):
{{
  "title": "Tiêu đề video cực kỳ giật gân, cuốn hút người xem",
  "scenes": [
    {{
      "scene_id": 1,
      "narration": "Lời thoại gọi tên rõ chủ đề ngay từ câu đầu, kể chuyện kịch tính, kết thúc bằng một gợi mở nghẹt thở...",
      "image_prompt": "Vertical 9:16 portrait composition, dramatic cinematic watercolor illustration with intense lighting, storybook art style, clean white background, vertical orientation, full vertical view, 9:16 aspect ratio --ar 9:16",
      "keywords": ["từ_khóa_1", "từ_khóa_2", "từ_khóa_3"]
    }}
  ]
}}
"""

def enforce_vertical_9_16_prompt(prompt: str) -> str:
    """Đảm bảo prompt ảnh luôn luôn có định dạng khung dọc 9:16 và tham số --ar 9:16 chuẩn xác."""
    p = (prompt or "").strip()
    if not p:
        return "Vertical 9:16 portrait composition, vibrant watercolor and pencil sketch illustration, storybook art style, clean white background, vertical orientation, full vertical view, 9:16 aspect ratio --ar 9:16"
    
    # Loại bỏ các tag tỉ lệ hoặc đuôi trùng lặp
    p = re.sub(r"--ar\s+\d+:\d+", "", p, flags=re.IGNORECASE).strip()
    p = re.sub(r"(?:,\s*)?vertical orientation(?:,\s*full vertical view)?(?:,\s*9:16 aspect ratio)?", "", p, flags=re.IGNORECASE).strip()
    p = re.sub(r",\s*,+", ",", p).strip(", ")

    # Đảm bảo phần đầu có chỉ thị khung dọc 9:16
    has_vertical_prefix = p.lower().startswith("vertical 9:16") or "vertical 9:16 portrait" in p.lower()
    if not has_vertical_prefix:
        p = f"Vertical 9:16 portrait composition, {p}"

    p = f"{p.rstrip(', ')}, vertical orientation, full vertical view, 9:16 aspect ratio --ar 9:16"
    return p

def clean_scene_narration(text: str) -> str:
    """Loại bỏ triệt để các câu mở bài lan man rập khuôn nếu mô hình lỡ sinh ra, giữ nguyên các câu dẫn dắt kịch tính."""
    t = (text or "").strip()
    # Loại bỏ câu mở đầu rập khuôn, lan man
    cliche_starters = [
        r"^bạn có bao giờ tự hỏi\s*,?\s*",
        r"^liệu bạn có biết rằng\s*,?\s*",
        r"^bạn có từng thắc mắc\s*,?\s*",
        r"^hãy cùng khám phá\s*,?\s*",
        r"^hãy cùng tìm hiểu\s*,?\s*",
        r"^bạn có biết rằng\s*,?\s*",
        r"^bạn có từng nghĩ\s*,?\s*",
        r"^từ xa xưa\s*,?\s*",
        r"^trong thế giới ngày nay\s*,?\s*",
        r"^có một sự thật rằng\s*,?\s*",
        r"^khi nhắc đến\s*[^,]+,?\s*",
        r"^trong video hôm nay\s*,?\s*",
        r"^hôm nay chúng ta sẽ\s*[^,]+,?\s*",
        r"^chắc hẳn ai trong chúng ta cũng\s*[^,]+,?\s*",
    ]
    for pattern in cliche_starters:
        t = re.sub(pattern, "", t, flags=re.IGNORECASE).strip()
    
    if t:
        t = t[0].upper() + t[1:]

    # Dọn dẹp dấu câu đôi nếu có
    t = re.sub(r"\.\.+", ".", t).strip()
    return t

def ensure_topic_in_scene1(narration: str, topic: str) -> str:
    """
    Đảm bảo LỜI THOẠI CẢNH 1 (phần đọc TTS) PHẢI trực tiếp gọi tên hoặc đập trúng chủ đề chính.
    Tránh trường hợp Gemini chỉ để chủ đề ở tiêu đề ngoài mà giọng đọc TTS lại nói lan man, trừu tượng.
    """
    narr = (narration or "").strip()
    top = (topic or "").strip()
    if not narr or not top:
        return narr

    # Tách các từ khóa có nghĩa từ topic
    stop_words = {"tại", "sao", "của", "và", "là", "những", "các", "cho", "về", "có", "không", "được", "ra", "lại", "đến", "vì", "thì", "mà", "khi"}
    words = [w.strip() for w in re.split(r"[\s,\.\?\!\:\-]+", top.lower()) if w.strip() and w.strip() not in stop_words and len(w.strip()) > 1]
    
    narr_lower = narr.lower()
    # Kiểm tra xem có từ khóa chủ đề nào xuất hiện trong 25 từ đầu tiên của Scene 1 không
    first_few_words = " ".join(narr_lower.split()[:25])
    has_topic_keyword = any(w in first_few_words for w in words) if words else (top.lower() in first_few_words)

    if not has_topic_keyword:
        clean_top = top.strip("?.!")
        if clean_top.lower().startswith("tại sao"):
            narr = f"{clean_top}? {narr}"
        elif any(clean_top.lower().startswith(p) for p in ["bí ẩn", "bí mật", "nguồn gốc", "sự tích", "thảm kịch", "câu chuyện"]):
            narr = f"{clean_top} bắt đầu khi {narr[0].lower() + narr[1:] if len(narr) > 1 else narr}"
        else:
            narr = f"Câu chuyện về {clean_top.lower()} bắt đầu khi {narr[0].lower() + narr[1:] if len(narr) > 1 else narr}"

    return narr

def generate_storyboard_with_gemini(
    topic: str,
    scenes_count: int = 3,
    language: str = "vi",
    api_key: str = None
) -> StoryboardResponse:
    """Gọi API Gemini để sinh kịch bản."""
    actual_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not actual_key or not actual_key.strip():
        raise ValueError("Chưa cung cấp GEMINI_API_KEY!")

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=actual_key.strip())
    prompt = STORY_PROMPT_TEMPLATE.format(
        topic=topic,
        scenes_count=scenes_count,
        target_duration=scenes_count * 15,
        language="Tiếng Việt" if language == "vi" else "Tiếng Anh"
    )

    # Danh sách model ưu tiên (cập nhật các phiên bản mới nhất theo khuyến nghị Google Gemini API)
    model_candidates = [
        "gemini-3.6-flash",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
        "gemini-1.5-flash"
    ]

    # Cố gắng lấy danh sách model thực tế còn hoạt động từ API tài khoản
    try:
        listed = client.models.list()
        active_flash = []
        for m in listed:
            m_name = getattr(m, 'name', '') or ''
            clean_name = m_name.replace("models/", "")
            if "flash" in clean_name.lower() and "thinking" not in clean_name.lower():
                active_flash.append(clean_name)
        if active_flash:
            # Đưa model flash từ API lên ưu tiên hàng đầu
            model_candidates = list(dict.fromkeys(active_flash + model_candidates))
            print(f"[ScriptEngine] Đã phát hiện các model khả dụng: {active_flash[:3]}")
    except Exception as e_list:
        print(f"[ScriptEngine] Không thể lấy danh sách models động ({e_list}), dùng danh sách model mặc định.")

    # Cấu hình generation tối ưu cho văn phong sáng tạo, sâu sắc, không sáo rỗng
    gen_config = types.GenerateContentConfig(
        temperature=0.85,
        top_p=0.95,
        response_mime_type="application/json"
    )

    response = None
    last_error = None
    for model_name in model_candidates:
        try:
            print(f"[ScriptEngine] Đang gọi model '{model_name}' với kịch bản chiều sâu...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=gen_config
            )
            if response and response.text:
                print(f"[ScriptEngine] ✅ Thành công với model: {model_name}")
                break
        except Exception as err:
            last_error = err
            print(f"[ScriptEngine] Model '{model_name}' không khả dụng ({err}), đang thử model tiếp theo...")

    if not response or not response.text:
        raise ValueError(f"Không thể tạo kịch bản từ Gemini: {last_error}")
    
    text = response.text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    
    json_match = re.search(r"(\{.*\})", text, re.DOTALL)
    if json_match:
        text = json_match.group(1)

    data = json.loads(text)
    
    # Bắt buộc chuẩn hóa mọi image_prompt sang khung hình dọc 9:16 và làm sạch lời thoại
    if "scenes" in data and isinstance(data["scenes"], list):
        for idx, s in enumerate(data["scenes"]):
            if "narration" in s:
                s["narration"] = clean_scene_narration(s["narration"])
                if idx == 0:
                    s["narration"] = ensure_topic_in_scene1(s["narration"], topic)
            if "image_prompt" in s:
                s["image_prompt"] = enforce_vertical_9_16_prompt(s["image_prompt"])

    return StoryboardResponse(**data)

def generate_mock_storyboard(topic: str, scenes_count: int = 3) -> StoryboardResponse:
    """
    Sinh kịch bản dự phòng thông minh:
    Đảm bảo 100% không bao giờ bị lặp lại phân cảnh (kể cả khi chọn 6, 8 hay 10 cảnh).
    Mỗi cảnh đều mang một góc nhìn tiến trình riêng biệt và lời kết đúc kết sâu sắc.
    """
    lower = topic.lower()
    count = max(1, min(scenes_count, 12))

    # 1. Kịch bản chuyên đề Thiên Nhiên / Sinh Học / Sâu Bướm / Động Thực Vật
    if any(k in lower for k in ["sâu bướm", "bướm", "lột xác", "côn trùng", "sinh học", "thiên nhiên", "động vật", "loài hoa", "cây cối"]):
        hook = {
            "narration": "Bên trong chiếc kén tơ, con sâu bướm không hề mọc thêm cánh. Toàn bộ cơ thể nó tự tiết enzym phân hủy chính mình thành một bãi dịch lỏng súp nhớp nháp. Để tái sinh thành một cánh bướm rực rỡ, nó buộc phải tự hủy diệt hoàn toàn. Thế nhưng, bi kịch nghiệt ngã ấy thực chất chỉ là bước khởi đầu của một phép màu phi thường...",
            "prompt": "Vertical 9:16 portrait composition, dramatic cinematic watercolor illustration of a caterpillar forming a mystical glowing cocoon, macro view, rich vibrant colors, clean white background, vertical orientation, 9:16 aspect ratio --ar 9:16",
            "keywords": ["sâu bướm", "lột xác", "chuyển hóa"]
        }
        body_pool = [
            {
                "narration": "Hành trình bắt đầu từ những ngày tháng ấu trùng non nớt. Chú sâu phải ăn liên tục ngày đêm để tích lũy từng giọt năng lượng quý giá, chuẩn bị cho bước ngoặt sinh tử lớn nhất cuộc đời. Và khi thời khắc định mệnh gõ cửa, nó lặng lẽ tìm đến một cành cây kiên cố...",
                "prompt": "Vertical 9:16 portrait composition, detailed watercolor sketch of green caterpillar happily nibbling on fresh succulent leaves in sunlit garden, vibrant watercolor textures, clean background",
                "keywords": ["ấu trùng", "tích lũy", "sinh trưởng"]
            },
            {
                "narration": "Nó dốc cạn sức lực nhả ra những sợi tơ bền bỉ nhất để tự giam mình vào chiếc kén tăm tối. Đằng sau lớp vỏ tĩnh lặng ấy không phải là giấc ngủ yên bình, mà là một cuộc giải thể rùng mình: toàn bộ cơ bắp tan chảy thành dung dịch nguyên sinh, chỉ giữ lại các tế bào mầm cánh quý giá...",
                "prompt": "Vertical 9:16 portrait composition, mystical watercolor illustration of the inner transformation inside a translucent cocoon, magical glowing biological cells, ethereal colors",
                "keywords": ["kết kén", "phân hủy", "tái sinh"]
            },
            {
                "narration": "Từ đống tro tàn của thể xác cũ, một phép màu kiến tạo bắt đầu: từng mạch máu li ti, đôi mắt kép tinh anh và đôi cánh mỏng manh được dệt nên với sự chính xác tuyệt đối. Tưởng chừng như khó khăn đã qua đi, một thử thách sống còn thứ hai lập tức ập tới...",
                "prompt": "Vertical 9:16 portrait composition, artistic watercolor sketch showing delicate patterned butterfly wings forming inside soft glowing cocoon, rich artistic texture, white background",
                "keywords": ["tạo hình", "đôi cánh", "kỳ tích"]
            },
            {
                "narration": "Chiếc kén khô cứng trở thành một nhà tù nghẹt thở. Không một ai giúp đỡ, chú bướm non phải tự dùng toàn bộ sức lực đạp vỡ lớp vỏ để chui ra ngoài thế giới. Nếu có ai đó cắt giúp kén, đôi cánh sẽ mãi mãi bại liệt...",
                "prompt": "Vertical 9:16 portrait composition, dramatic watercolor illustration of a butterfly emerging from its broken chrysalis, determination and struggle, vivid colors, white background",
                "keywords": ["phá kén", "đấu tranh", "nỗ lực"]
            },
            {
                "narration": "Chính áp lực nghẹt thở khi tự mình chui qua khe hở hẹp đã ép dòng dịch thể chảy đều vào các mao mạch, làm đôi cánh căng tràn sức sống! Đứng dưới ánh nắng ban mai ấm áp, đôi cánh ướt sũng dần khô ráo, trở nên cứng cáp và tỏa sáng lộng lẫy...",
                "prompt": "Vertical 9:16 portrait composition, close-up watercolor sketch of butterfly carefully pumping fluid into expanding colorful patterned wings, brilliant colors, clean background",
                "keywords": ["áp lực", "mao mạch", "sức mạnh"]
            },
            {
                "narration": "Từng vệt phấn hoa lấp lánh như ngàn viên kim cương, sẵn sàng cho cú đập cánh đầu tiên xé toạc bầu trời. Khoảnh khắc ấy là sự đền đáp xứng đáng cho chuỗi ngày giằng xé trong bóng tối...",
                "prompt": "Vertical 9:16 portrait composition, breathtaking watercolor illustration of a magnificent butterfly resting on a blooming flower, sunbeams shining through colorful wings, masterpiece",
                "keywords": ["tỏa sáng", "hoàn mỹ", "rực rỡ"]
            }
        ]
        conclusion = {
            "narration": "Không có nỗi đau lột xác thì không bao giờ có được đôi cánh tự do bay lượn. Cuộc tái sinh của cánh bướm nhắc nhở chúng ta: mọi nghịch cảnh và áp lực trong cuộc sống hôm nay đều là sự chuẩn bị để bạn cất cánh rực rỡ vào ngày mai!",
            "prompt": "Vertical 9:16 portrait composition, inspiring watercolor illustration of a gorgeous butterfly soaring high into a vast blue sunlit sky with glowing clouds, freedom and triumph, white background",
            "keywords": ["cất cánh", "tự do", "bài học"]
        }

    # 2. Kịch bản chuyên đề Khủng Long / Thiên Văn / Khoa học tự nhiên
    elif any(k in lower for k in ["khủng long", "tuyệt chủng", "dinosaur", "vũ trụ", "thiên thạch", "trái đất"]):
        hook = {
            "narration": "66 triệu năm trước, giữa buổi trưa yên bình của kỷ Phấn Trắng, bầu trời bỗng rực sáng một quầng lửa chói lòa. Một thiên thạch rộng 10 km lao thẳng xuống với tốc độ 70.000 km/h, đâm sầm vào Trái Đất với sức công phá bằng 10 tỷ quả bom nguyên tử. Thế nhưng, cú va chạm long trời lở đất ấy chỉ mới là khúc dạo đầu của một cơn ác mộng tàn khốc hơn gấp bội...",
            "prompt": "Vertical 9:16 portrait composition, dramatic cinematic watercolor illustration of giant Tyrannosaurus Rex looking up at a blazing apocalyptic asteroid cutting through twilight sky, artistic sketch lines, vivid colors, clean white background, vertical orientation, 9:16 aspect ratio --ar 9:16",
            "keywords": ["khủng long", "thiên thạch", "tuyệt chủng"]
        }
        body_pool = [
            {
                "narration": "Ngay sau tiếng nổ xé toạc địa cầu, bức tường sóng thần cao hàng trăm mét nuốt chửng các vùng duyên hải. Một cơn mưa mảnh vỡ rực lửa trút xuống như thiêu đốt mặt đất, biến những cánh rừng bạt ngàn thành biển lửa ngút ngàn. Trong cơn hoảng loạn tột cùng, những kẻ săn mồi khổng lồ bắt đầu nhận ra mình hoàn toàn bất lực...",
                "prompt": "Vertical 9:16 portrait composition, Cinematic watercolor sketch of a massive blazing asteroid striking the earth with cataclysmic shockwaves and fiery explosion, dramatic colors, white background",
                "keywords": ["sóng thần", "mưa lửa", "hỗn loạn"]
            },
            {
                "narration": "Tưởng chừng ngọn lửa rực trời đã là tận cùng của sự hủy diệt, một thảm kịch âm thầm khác lại ập tới: hàng triệu tấn tro bụi bốc lên che khuất hoàn toàn ánh mặt trời suốt nhiều năm ròng. Trái Đất chìm vào một mùa đông hạt nhân lạnh giá. Không còn quang hợp, chuỗi thức ăn sụp đổ đẩy những gã khổng lồ vào nạn đói kinh hoàng...",
                "prompt": "Vertical 9:16 portrait composition, Haunting watercolor illustration of a frozen dark prehistoric landscape with thick smoke blotting out the sun, silhouette of dinosaur skeleton, watercolor art",
                "keywords": ["mùa đông hạt nhân", "tuyệt chủng", "nạn đói"]
            },
            {
                "narration": "Giữa thời khắc đen tối tưởng như sự sống trên hành tinh đã bị xóa sổ vĩnh viễn, một cuộc chiến sinh tồn thầm lặng lại diễn ra dưới lòng đất sâu. Những loài thú có vú nhỏ bé, vốn chỉ biết lẩn trốn trong bóng tối trước đây, nay lại tìm thấy hy vọng nhờ khả năng đào hang trú ẩn và ăn rễ cây khô...",
                "prompt": "Vertical 9:16 portrait composition, Vibrant watercolor sketch of tiny clever mammals sheltering safely inside deep earthen burrows while storms rage outside, rich colors, white background",
                "keywords": ["sinh tồn", "thích nghi", "đào hang"]
            },
            {
                "narration": "Sự nhỏ bé từng bị coi là yếu ớt giờ đây lại trở thành chiếc chìa khóa vàng mở ra cánh cửa sống còn. Khi những kẻ thống trị to lớn lần lượt gục ngã vì kiệt quệ, những sinh vật nhỏ bé kiên cường này đã kiên trì vượt qua đêm trường băng giá để đợi chờ một ngày mai...",
                "prompt": "Vertical 9:16 portrait composition, Artistic watercolor illustration of prehistoric fossil excavation site with glowing amber fossils of dinosaur bones, mysterious lighting, storybook art",
                "keywords": ["kiên trì", "nghịch cảnh", "chờ đợi"]
            },
            {
                "narration": "Và rồi, sau hàng triệu năm tro tàn lắng xuống, những tia nắng ấm áp đầu tiên đã chiếu rọi trở lại mặt đất. Những mầm xanh đầu tiên nhú lên từ tro tàn núi lửa, báo hiệu một kỷ nguyên tái sinh kỳ diệu...",
                "prompt": "Vertical 9:16 portrait composition, Vibrant watercolor art of prehistoric green sprouts growing out of volcanic soil, bright hopeful morning light, white background",
                "keywords": ["hồi sinh", "ánh sáng", "tiến hóa"]
            }
        ]
        conclusion = {
            "narration": "Thảm kịch tuyệt chủng của loài khủng long là một mất mát đau thương, nhưng cũng là chiếc nôi vĩ đại mở đường cho tổ tiên loài người trỗi dậy. Trong quy luật của vũ trụ, mọi sự sụp đổ khốc liệt nhất đều là sự dọn đường cho một sự tái sinh vĩ đại!",
            "prompt": "Vertical 9:16 portrait composition, Inspiring watercolor illustration of lush green Earth reborn under warm golden sunlight, peaceful wildlife flourishing in paradise, uplifting storybook art, white background",
            "keywords": ["tái sinh", "tiến hóa", "bài học"]
        }

    # 3. Kịch bản chuyên đề Phát triển bản thân / Động lực / Kỷ luật
    elif any(k in lower for k in ["kỷ luật", "động lực", "thói quen", "đọc sách", "thành công", "kiên trì", "th thời gian"]):
        hook = {
            "narration": f"Cảm hứng và động lực nhất thời chỉ là một cái bẫy dối lừa ngọt ngào. Bộ não con người vốn được lập trình để né tránh đau đớn và chọn sự an toàn. Thứ duy nhất tạo nên sự bứt phá cho {topic} là kỷ luật thép: ép bản thân hành động ngay cả khi chán chường nhất. Thế nhưng, cuộc chiến nội tâm này cam go hơn bất kỳ ai tưởng tượng...",
            "prompt": "Vertical 9:16 portrait composition, powerful watercolor illustration of a determined person stepping forward through a storm onto a glowing golden path, intense focus, storybook art, clean white background, vertical orientation, 9:16 aspect ratio --ar 9:16",
            "keywords": ["kỷ luật thép", "mục tiêu", "tư duy"]
        }
        body_pool = [
            {
                "narration": "Khi ngọn lửa hưng phấn ban đầu vụt tắt, bạn sẽ lập tức đối mặt với 'bức tường kháng cự' vô hình: sự lười biếng, nỗi sợ thất bại và tiếng nói thầm thì đòi bỏ cuộc. Khoảnh khắc bạn muốn buông xuôi nhất lại chính là ngã rẽ định mệnh quyết định số phận...",
                "prompt": "Vertical 9:16 portrait composition, Artistic watercolor sketch of a determined person studying under a warm desk lamp with ticking clock and glowing gears of progress, rich colors, clean art",
                "keywords": ["kháng cự", "thử thách", "ngã rẽ"]
            },
            {
                "narration": "Bí quyết của những bậc thầy không phải là chờ đợi cảm hứng, mà là tạo ra quán tính hành động. Bằng cách chia nhỏ mục tiêu và ép bản thân tập trung tuyệt đối trong 15 phút đầu tiên, bạn sẽ đánh bại sức ì của não bộ và kích hoạt dòng chảy hưng phấn nội tại...",
                "prompt": "Vertical 9:16 portrait composition, Vibrant watercolor sketch of organized stepping stones leading smoothly across a rushing crystal stream towards a sunlit castle, storybook style",
                "keywords": ["quán tính", "chia nhỏ", "tập trung"]
            },
            {
                "narration": "Và khi hành động nhỏ ấy được lặp đi lặp lại qua từng ngày, một phép màu vô hình bắt đầu vận hành: hiệu ứng lãi kép của thói quen. Từng giọt nước nhỏ tưởng như vô hại, nhưng khi tích tụ đủ lâu sẽ có sức mạnh xuyên thủng cả tảng đá cứng nhất...",
                "prompt": "Vertical 9:16 portrait composition, Vibrant watercolor illustration of a tiny green seedling bursting through stone pavement and transforming into a radiant giant blooming tree, white background",
                "keywords": ["lãi kép", "thói quen", "bứt phá"]
            },
            {
                "narration": "Sẽ có những lúc bạn vấp ngã và cảm thấy bản thân bất lực. Nhưng những người bản lĩnh hiểu rằng mỗi thất bại không phải là dấu chấm hết, mà là một bài kiểm tra để tôi luyện ý chí sắt đá trước khi bước vào đỉnh cao vinh quang...",
                "prompt": "Vertical 9:16 portrait composition, Inspiring watercolor sketch of an inventor smiling while studying blueprints among glowing lightbulbs, vibrant warm art, clean background",
                "keywords": ["ý chí sắt đá", "kiên cường", "tiến bộ"]
            },
            {
                "narration": "Học cách tự hào về từng bước tiến nhỏ mỗi ngày. Niềm vui từ sự tự chủ nội tâm sẽ là nguồn nhiên liệu bất tận đưa bạn vượt qua mọi giông bão của cuộc đời...",
                "prompt": "Vertical 9:16 portrait composition, Vibrant watercolor illustration of an individual proudly celebrating small wins at sunset on a scenic viewpoint, warm light, clean background",
                "keywords": ["tự chủ", "niềm vui", "nội lực"]
            }
        ]
        conclusion = {
            "narration": "Đừng chờ đợi cho đến khi bản thân cảm thấy hoàn hảo mới bắt đầu. Tương lai của bạn không được định hình bởi những lời hứa hẹn ngày mai, mà được khắc ghi bởi chính quyết định kiên trì vượt qua nghịch cảnh ngay trong giây phút này!",
            "prompt": "Vertical 9:16 portrait composition, Inspiring watercolor illustration of a triumphant runner reaching the summit of a sunlit mountain raising arms in victory, colorful twilight sky, storybook art",
            "keywords": ["hành động", "chiến thắng", "tương lai"]
        }

    # 4. Kịch bản chuyên đề Tổng quát: Khoa học, Khám phá, Đời sống
    else:
        hook = {
            "narration": f"Sự thật trần trụi về {topic} hoàn toàn trái ngược với những gì số đông lầm tưởng. Ẩn sâu bên dưới bề mặt phẳng lặng là một chuỗi biến cố kịch tính đến nghẹt thở, nơi một chi tiết nhỏ cũng đủ sức kích nổ toàn bộ cục diện. Thế nhưng, bí mật đen tối này lại bị chôn giấu suốt một thời gian dài...",
            "prompt": f"Vertical 9:16 portrait composition, Dramatic cinematic watercolor illustration revealing the intense truth of {topic}, striking focal point, rich vibrant textures, clean white background, vertical orientation, 9:16 aspect ratio --ar 9:16",
            "keywords": ["sự thật", "bản chất", "nghịch lý"]
        }
        body_pool = [
            {
                "narration": f"Câu chuyện bắt đầu khi những vết nứt đầu tiên xuất hiện. Một chuỗi áp lực âm thầm gia tăng mà mắt thường không thể phát hiện, cho đến khi chạm đến ngưỡng cân bằng mong manh. Và rồi, một bước ngoặt sinh tử bất ngờ giáng xuống...",
                "prompt": f"Vertical 9:16 portrait composition, Artistic watercolor sketch depicting the origins and extreme forces of {topic}, swirling colors, intricate details, clean white background",
                "keywords": ["áp lực", "vết nứt", "bước ngoặt"]
            },
            {
                "narration": f"Khoảnh khắc biến cố bùng nổ, mọi quy chuẩn thông thường lập tức sụp đổ. Các lực tác động va chạm dữ dội, tạo ra một phản ứng dây chuyền không thể đảo ngược, cuốn phăng mọi nỗ lực chống đỡ ban đầu...",
                "prompt": f"Vertical 9:16 portrait composition, Vibrant watercolor illustration showing puzzle pieces connecting into a brilliant illuminated masterpiece, radiant rich colors, white background",
                "keywords": ["va chạm", "hỗn loạn", "phản ứng"]
            },
            {
                "narration": f"Tưởng chừng như mọi thứ đã rơi vào ngõ cụt hoàn toàn, một phát hiện đột phá đã hé lộ bản chất thực sự của vấn đề. Hóa ra, chính yếu tố bị xem nhẹ nhất từ trước đến nay lại nắm giữ chiếc chìa khóa định đoạt kết cục...",
                "prompt": f"Vertical 9:16 portrait composition, Artistic watercolor illustration of ancient compass and glowing celestial maps revealing secret pathways, rich colorful details, white background",
                "keywords": ["phát hiện", "chìa khóa", "bản chất"]
            },
            {
                "narration": f"Từ đống hỗn loạn, các mắt xích bắt đầu tự sắp xếp lại theo một trật tự hoàn toàn mới, khốc liệt hơn nhưng cũng chuẩn xác hơn bao giờ hết, từng bước định hình lại toàn bộ thực tế...",
                "prompt": f"Vertical 9:16 portrait composition, Vibrant watercolor sketch of visionary thinkers observing luminous molecular models and glowing data streams, creative art, clean background",
                "keywords": ["trật tự mới", "định hình", "chuẩn xác"]
            },
            {
                "narration": f"Những vết tích để lại chính là bằng chứng sống động nhất, khẳng định rằng bất kỳ sự chuyển hóa vĩ đại nào cũng phải đánh đổi bằng những thử thách nghiệt ngã nhất...",
                "prompt": f"Vertical 9:16 portrait composition, Dramatic watercolor illustration of a crystalline drop creating radiant expanding ripples in a quiet mountain lake, rich colors, white background",
                "keywords": ["bằng chứng", "chuyển hóa", "thử thách"]
            }
        ]
        conclusion = {
            "narration": f"Nhìn lại toàn bộ hành trình của {topic}, ta nhận ra một chân lý sâu sắc: mọi biến cố tưởng như ngẫu nhiên đều là những nấc thang định mệnh dẫn lối cho sự tiến hóa. Hiểu được điều này, bạn sẽ tìm thấy sức mạnh vượt qua mọi nghịch cảnh!",
            "prompt": f"Vertical 9:16 portrait composition, Inspiring watercolor illustration of human mind expanding with glowing constellations and colorful ideas, uplifting storytelling art, clean white background",
            "keywords": ["bài học", "tương lai", "khai sáng"]
        }

    # Ghép kịch bản đảm bảo 100% KHÔNG BAO GIỜ TRÙNG LẶP:
    # - Cảnh 1: LUÔN LÀ HOOK
    # - Các cảnh giữa: LẤY TUẦN TỰ TỪ BODY_POOL HOẶC TỰ ĐỘNG TẠO BƯỚC MỚI KHÁC BIỆT
    # - Cảnh cuối: LUÔN LÀ CONCLUSION (Lời kết và bài học đúc kết)
    final_scenes = []
    if count == 1:
        final_scenes = [conclusion]
    elif count == 2:
        final_scenes = [hook, conclusion]
    else:
        final_scenes.append(hook)
        num_body = count - 2
        for b_idx in range(num_body):
            if b_idx < len(body_pool):
                chosen_body = body_pool[b_idx]
            else:
                # Nếu số cảnh vượt quá pool, sinh phân cảnh mở rộng độc nhất, tuyệt đối không lặp lại
                stage_idx = b_idx + 1
                chosen_body = {
                    "narration": f"Đi sâu hơn vào chặng thứ {stage_idx} của {topic}, những nhân tố mới tiếp tục xuất hiện và làm sáng tỏ bức tranh toàn cảnh, mang đến cho chúng ta những phát hiện vô cùng bất ngờ.",
                    "prompt": f"Vertical 9:16 portrait composition, Vibrant artistic watercolor illustration depicting stage {stage_idx} of {topic}, swirling bright colors, intriguing visual details, clean white background",
                    "keywords": [f"giai đoạn {stage_idx}", "khám phá mới", "phát hiện"]
                }
            final_scenes.append(chosen_body)
        final_scenes.append(conclusion)

    generated_scenes = []
    for i, item in enumerate(final_scenes):
        generated_scenes.append(
            SceneItem(
                scene_id=i + 1,
                narration=item["narration"],
                image_prompt=enforce_vertical_9_16_prompt(item["prompt"]),
                keywords=item["keywords"]
            )
        )

    return StoryboardResponse(
        title=f"Bí Ẩn Khám Phá: {topic}",
        scenes=generated_scenes
    )

def generate_storyboard(
    topic: str,
    scenes_count: int = 2,
    language: str = "vi",
    api_key: str = None
) -> StoryboardResponse:
    """Hàm chính tự động phát hiện API Key hoặc dùng mock storyboard."""
    actual_key = (api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    if actual_key and actual_key != "your_gemini_api_key_here":
        try:
            print(f"[ScriptEngine] Đang gọi Google Gemini cho chủ đề: '{topic}' ({scenes_count} cảnh)...")
            return generate_storyboard_with_gemini(topic, scenes_count, language, actual_key)
        except Exception as e:
            print(f"[ScriptEngine] Lỗi khi gọi Gemini ({e}). Chuyển sang kịch bản thông minh dự phòng.")
    
    print(f"[ScriptEngine] Sử dụng kịch bản dự phòng cho chủ đề: '{topic}'")
    return generate_mock_storyboard(topic, scenes_count)

if __name__ == "__main__":
    sb = generate_storyboard("Lòng kiên trì của Rùa và Thỏ", scenes_count=2)
    print("Kịch bản tạo được:")
    print(sb.model_dump_json(indent=2))
