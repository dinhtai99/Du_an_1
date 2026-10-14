from app.schemas.pipeline import (
    PipelineSceneInput,
    PipelineSceneState,
    PipelineStartRequest,
)


class ScriptPlanner:
    """Create an editable first draft without loading a local LLM."""

    _beats = (
        (
            "Mở đầu",
            "Không gian văn hóa Việt Nam trang nghiêm, ánh sáng bình minh, "
            "chi tiết thủ công truyền thống, góc máy điện ảnh",
        ),
        (
            "Bối cảnh",
            "Khung cảnh làng Việt cổ, mái đình, bàn thờ truyền thống, "
            "con người Việt Nam trong trang phục kín đáo và đúng thời kỳ",
        ),
        (
            "Nguồn gốc",
            "Tư liệu cổ Việt Nam, gia phả và thư tịch trên bàn gỗ, "
            "ánh sáng tự nhiên, không gian nghiên cứu truyền thống",
        ),
        (
            "Không gian",
            "Ngôi nhà Việt cổ với sân gạch, mái ngói và gian thờ trang nghiêm, "
            "bố cục dọc sâu, ánh sáng sớm",
        ),
        (
            "Chuẩn bị",
            "Cận cảnh lễ vật và đồ thờ Việt Nam được sắp đặt trang nghiêm, "
            "ánh nến ấm, chất liệu sơn mài tinh xảo",
        ),
        (
            "Thực hành",
            "Đôi tay người Việt chuẩn bị nghi lễ cẩn trọng, động tác tự nhiên, "
            "chi tiết chân thực, không khí tĩnh lặng",
        ),
        (
            "Lòng thành",
            "Gia đình Việt nhiều thế hệ quây quần, cảm xúc thành kính, "
            "không gian ấm áp, bố cục cân đối",
        ),
        (
            "Đạo lý",
            "Khoảnh khắc con cháu lắng nghe người cao tuổi kể chuyện truyền thống, "
            "cảm xúc gần gũi và tôn kính",
        ),
        (
            "Cộng đồng",
            "Sinh hoạt văn hóa trong làng Việt, nhiều thế hệ cùng tham gia, "
            "không khí đoàn kết và trang trọng",
        ),
        (
            "Biểu tượng",
            "Cận cảnh biểu tượng văn hóa và hoa văn Việt Nam, chất liệu thủ công, "
            "ánh sáng điện ảnh, chiều sâu rõ nét",
        ),
        (
            "Chiêm nghiệm",
            "Nhân vật Việt Nam trầm tư trong không gian di sản, ánh sáng dịu, "
            "bố cục tối giản và giàu cảm xúc",
        ),
        (
            "Trao truyền",
            "Nghệ nhân Việt Nam gìn giữ thư tịch và nghi lễ cổ truyền, "
            "hướng dẫn thế hệ trẻ bằng thao tác chân thực",
        ),
        (
            "Gìn giữ",
            "Tủ lưu trữ thư tịch và hiện vật văn hóa Việt được bảo quản cẩn thận, "
            "không gian bảo tồn chuyên nghiệp",
        ),
        (
            "Hiện đại",
            "Người Việt sử dụng công nghệ để lưu trữ tư liệu truyền thống, "
            "màn hình hiện đại hài hòa với không gian văn hóa",
        ),
        (
            "Tiếp nối",
            "Di sản Việt Nam hiện diện trong đời sống hôm nay, gia đình trẻ "
            "trân trọng truyền thống, ánh sáng tươi sáng",
        ),
        (
            "Kết thúc",
            "Hình ảnh biểu tượng văn hóa Việt Nam trang trọng, khoảng trống "
            "bố cục phù hợp cho lời kết, ánh sáng vàng ấm",
        ),
    )

    def create_scenes(self, request: PipelineStartRequest) -> list[PipelineSceneState]:
        if request.scenes:
            return [
                self._from_input(index, scene, request)
                for index, scene in enumerate(request.scenes, start=1)
            ]

        narrations = self._narrations(request)
        scenes: list[PipelineSceneState] = []
        for index in range(request.scene_count):
            label, description = self._beats[
                round(index * (len(self._beats) - 1) / max(request.scene_count - 1, 1))
            ]
            narration = narrations[
                round(index * (len(narrations) - 1) / max(request.scene_count - 1, 1))
            ]
            scenes.append(
                PipelineSceneState(
                    order=index + 1,
                    narration=narration,
                    image_prompt=self._prompt(request, label, description),
                )
            )
        return scenes

    def _from_input(
        self,
        index: int,
        scene: PipelineSceneInput,
        request: PipelineStartRequest,
    ) -> PipelineSceneState:
        prompt = scene.image_prompt or self._prompt(
            request,
            f"Cảnh {index}",
            scene.narration,
        )
        return PipelineSceneState(
            order=index,
            narration=scene.narration,
            image_prompt=prompt,
            image_path=scene.image_path,
        )

    def _narrations(self, request: PipelineStartRequest) -> list[str]:
        topic = self._shorten(request.topic.strip().rstrip(".?!"), 6)
        return [
            f"Khám phá {topic}.",
            "Đây là một nét văn hóa lâu đời của người Việt.",
            "Nghi thức bắt nguồn từ nếp sống gia đình truyền thống.",
            "Mỗi vùng miền lưu giữ một cách thực hành riêng.",
            "Không gian nghi lễ luôn cần sự trang nghiêm.",
            "Lễ vật được chuẩn bị gọn gàng và thành kính.",
            "Từng chi tiết đều mang một ý nghĩa văn hóa.",
            "Điều quý nhất nằm ở lòng biết ơn.",
            "Nghi lễ nhắc con cháu nhớ về cội nguồn.",
            "Đó cũng là lúc gia đình cùng nhau sum họp.",
            "Người lớn trao lại kinh nghiệm cho thế hệ trẻ.",
            "Ký ức cộng đồng nhờ vậy được tiếp nối.",
            "Phong tục cần được hiểu đúng bối cảnh.",
            "Sự thành tâm quan trọng hơn hình thức cầu kỳ.",
            "Thực hành đúng giúp tránh những diễn giải mê tín.",
            "Tư liệu cổ cần được gìn giữ cẩn thận.",
            "Nghệ nhân góp phần bảo tồn tri thức dân gian.",
            "Công nghệ giúp lưu trữ và tra cứu thuận tiện.",
            "Truyền thống vẫn có thể đồng hành cùng hiện đại.",
            "Giá trị xưa tiếp tục sống trong đời sống hôm nay.",
            "Mỗi thế hệ đều có trách nhiệm gìn giữ di sản.",
            "Hiểu đúng giúp văn hóa được trao truyền bền vững.",
            f"{topic} là một phần ký ức Việt.",
            self._shorten(request.cta_text, 11),
        ]

    @staticmethod
    def _shorten(text: str, max_words: int) -> str:
        words = text.split()
        if len(words) <= max_words:
            return text
        return " ".join(words[:max_words]).rstrip(",.;:!?") + "…"

    def _prompt(
        self,
        request: PipelineStartRequest,
        label: str,
        description: str,
    ) -> str:
        context = f" Cultural context: {request.extra_context}." if request.extra_context else ""
        return (
            f"Create a vertical 9:16 cinematic still for a Vietnamese cultural short video. "
            f"Topic: {request.topic}. Scene: {label}. {description}. "
            f"Visual style: {request.visual_style}. Respect authentic Vietnamese architecture, "
            f"ritual objects, clothing and symbolism. Warm natural light, rich detail, realistic "
            f"hands and faces, centered subject, no captions, no letters, no watermark, no logo, "
            f"no Western religious symbols, no modern vehicles.{context}"
        )
