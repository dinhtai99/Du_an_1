import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from app.core.config import settings

# Built-in authoritative knowledge base for Vietnamese Traditional Sớ & Rituals
DEFAULT_CULTURAL_KNOWLEDGE = {
    "so_tao_quan": """
KIẾN THỨC VĂN HÓA VỀ SỚ TÁO QUÂN (23 THÁNG CHẠP):
- Ý nghĩa: Ngày 23 tháng Chạp âm lịch là ngày Táo Quân (Thần Bếp) cưỡi cá chép về trời tấu báo việc tốt xấu trong một năm của gia đình lên Ngọc Hoàng Thượng Đế.
- Tục dâng sớ: Gia chủ dâng sớ Táo Quân (Thần Bếp tấu sớ) ghi rõ bản quán, gia chủ tính danh, cầu xin xá tội giải hạn, kính báo lòng thành, cầu mong một năm mới mưa thuận gió hòa, gia đạo an yên.
- Lễ vật truyền thống: Cá chép (sống hoặc giấy), mâm cỗ mặn hoặc chay, mũ áo Táo Quân (hai mũ nam có cánh chuồn, một mũ nữ không cánh chuồn), hương hoa trà quả, vàng mã, tờ sớ viết chữ Nho hoặc Quốc ngữ trang trọng.
- Lưu ý văn hóa: Phải kính cẩn, không mê tín dị đoan thái quá, giữ gìn nét đẹp văn hóa thờ cúng tổ tiên và thần linh bản gia.
""",
    "so_cau_an": """
KIẾN THỨC VĂN HÓA VỀ SỚ CẦU AN (ĐẦU NĂM / DỊP LỄ):
- Ý nghĩa: Cầu mong chư Phật, Bồ Tát, Thần linh phù hộ cho gia đạo bình an, tai qua nạn khỏi, thân tâm an lạc, công việc hanh thông.
- Thể thức sớ: Mở đầu bằng chữ "Phục dĩ" (kính nghĩ rằng), nêu rõ "Nam mô Bản Sư Thích Ca Mâu Ni Phật", "Tam bảo chứng minh", tiếp đến bản tự/bản gia chỉ quán, ngày tháng, tên tuổi các thành viên trong gia đình.
- Nghi lễ: Thường tổ chức tại gia đình, chùa hoặc đền miếu vào dịp rằm tháng Giêng (Thượng Nguyên), rằm tháng Bảy (Trung Nguyên), rằm tháng Mười (Hạ Nguyên).
""",
    "so_cau_sieu": """
KIẾN THỨC VĂN HÓA VỀ SỚ CẦU SIÊU (BÁCH NHẬT, GIỖ, VU LAN):
- Ý nghĩa: Hướng tâm về cửu huyền thất tổ, tiên linh nội ngoại, các vong linh đã khuất, nương nhờ oai lực Tam Bảo sớm vãng sinh Cực Lạc.
- Thể thức: Lời văn bi thiết, trang nghiêm, nêu rõ tên tuổi hương linh, ngày mất, nơi an táng, tâm nguyện con cháu hồi hướng công đức.
""",
    "so_giao_thua": """
KIẾN THỨC VĂN HÓA VỀ SỚ GIAO THỪA (TRỪ TỊCH):
- Ý nghĩa: Thời khắc thiêng liêng chuyển giao năm cũ sang năm mới, nghênh đón vị Hành Khiển Thiên Binh mới cai quản nhân gian, tống tiễn Hành Khiển năm cũ.
- Lễ nghi: Có hai lễ sớ: Sớ Giao Thừa ngoài trời (nghênh quan Hành Khiển phán quan) và Sớ Giao Thừa trong nhà (thờ cúng Thần linh bản thổ và Gia tiên tiền tổ).
""",
    "may_in_so_phan_mem_so": """
QUẢNG BÁ SẢN PHẨM & CÔNG NGHỆ BẢO TỒN VĂN HÓA:
- Phần mềm viết sớ tự động: Hỗ trợ chuyển đổi nhanh Quốc ngữ sang chữ Hán Nôm chuẩn thể, chuẩn lòng sớ, chuẩn mẫu sớ cổ truyền các khoa lễ (Cầu An, Cầu Siêu, Táo Quân, Giao Thừa, Trạng Mã, Cúng Mụ...). Tiết kiệm thời gian, chính xác lòng dòng, không sai lệch điển tích.
- Máy in sớ chuyên dụng: In khổ giấy dài truyền thống (khổ vàng, khổ đỏ, giấy long phụng), mực bền màu không phai, in sắc nét chữ Hán Nôm và hoa văn rồng phượng cổ truyền.
- Lợi ích: Giữ gìn hồn cốt chữ cổ Việt Nam kết hợp công nghệ hiện đại phục vụ các thầy, chùa, đền và bà con tín chủ trang nghiêm đạo vị.
"""
}

class KnowledgeService:
    def __init__(self):
        self.knowledge_dir = settings.KNOWLEDGE_DIR
        self._bootstrap_knowledge()

    def _bootstrap_knowledge(self):
        """Write default cultural documents if knowledge dir is empty"""
        for doc_key, content in DEFAULT_CULTURAL_KNOWLEDGE.items():
            file_path = self.knowledge_dir / f"{doc_key}.txt"
            if not file_path.exists():
                file_path.write_text(content.strip(), encoding="utf-8")

    def get_cultural_context(self, topic: str, extra_context: Optional[str] = None) -> str:
        """
        Retrieve relevant cultural knowledge matching topic keywords.
        Ensures strict accuracy and provides guardrails against hallucinating Hán Nôm.
        """
        matched_docs = []
        topic_lower = topic.lower()

        # Check keyword matches
        if any(w in topic_lower for w in ["táo quân", "ong tao", "bếp", "chạp", "cá chép"]):
            matched_docs.append(DEFAULT_CULTURAL_KNOWLEDGE["so_tao_quan"])
        if any(w in topic_lower for w in ["cầu an", "đầu năm", "bình an", "thượng nguyên"]):
            matched_docs.append(DEFAULT_CULTURAL_KNOWLEDGE["so_cau_an"])
        if any(w in topic_lower for w in ["cầu siêu", "vu lan", "vong linh", "tổ tiên", "giỗ"]):
            matched_docs.append(DEFAULT_CULTURAL_KNOWLEDGE["so_cau_sieu"])
        if any(w in topic_lower for w in ["giao thừa", "trừ tịch", "hành khiển", "năm mới", "tết"]):
            matched_docs.append(DEFAULT_CULTURAL_KNOWLEDGE["so_giao_thua"])
        
        # Product promotion context always included
        matched_docs.append(DEFAULT_CULTURAL_KNOWLEDGE["may_in_so_phan_mem_so"])

        # Also scan custom user documents in storage/knowledge/
        for p in self.knowledge_dir.glob("*.txt"):
            try:
                text = p.read_text(encoding="utf-8")
                # Add if not already included and relates to query
                if p.stem not in DEFAULT_CULTURAL_KNOWLEDGE and any(word in text.lower() for word in topic_lower.split() if len(word) > 3):
                    matched_docs.append(f"\n--- TÀI LIỆU NGHIÊN CỨU: {p.name} ---\n{text[:1500]}")
            except Exception:
                pass

        combined_knowledge = "\n".join(matched_docs)
        if extra_context:
            combined_knowledge += f"\n--- THÔNG TIN DO NGƯỜI DÙNG CUNG CẤP THÊM ---\n{extra_context}\n"

        return combined_knowledge

    def add_document(self, filename: str, content: str) -> str:
        safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)
        target_path = self.knowledge_dir / safe_name
        target_path.write_text(content, encoding="utf-8")
        return str(target_path)

    def list_documents(self) -> List[Dict[str, str]]:
        docs = []
        for p in self.knowledge_dir.glob("*.*"):
            if p.suffix.lower() in [".txt", ".md", ".json"]:
                docs.append({
                    "filename": p.name,
                    "size_bytes": p.stat().st_size,
                    "path": str(p)
                })
        return docs

knowledge_service = KnowledgeService()
