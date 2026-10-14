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
            "Nguồn gốc",
            "Khung cảnh làng Việt cổ, mái đình, bàn thờ truyền thống, "
            "con người Việt Nam trong trang phục kín đáo và đúng thời kỳ",
        ),
        (
            "Nghi lễ",
            "Cận cảnh lễ vật và đồ thờ Việt Nam được sắp đặt trang nghiêm, "
            "ánh nến ấm, chất liệu sơn mài tinh xảo",
        ),
        (
            "Ý nghĩa",
            "Gia đình Việt nhiều thế hệ quây quần, cảm xúc thành kính, "
            "không gian ấm áp, bố cục cân đối",
        ),
        (
            "Gìn giữ",
            "Nghệ nhân Việt Nam gìn giữ thư tịch và nghi lễ cổ truyền, "
            "kết hợp tinh tế giữa di sản và công nghệ hiện đại",
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
        topic = request.topic.strip().rstrip(".?!")
        return [
            f"Bạn có biết điều gì làm nên giá trị đặc biệt của {topic}?",
            f"{topic} gắn với đời sống tinh thần và ký ức văn hóa của người Việt.",
            "Mỗi chi tiết trong nghi lễ đều gửi gắm lòng thành kính, sự biết ơn và mong cầu bình an.",
            "Điều quan trọng là thực hành trang nghiêm, đúng hoàn cảnh và tránh những diễn giải mê tín quá mức.",
            "Ngày nay, công nghệ có thể hỗ trợ lưu giữ tư liệu và trình bày nghi lễ rõ ràng hơn mà vẫn tôn trọng truyền thống.",
            request.cta_text,
        ]

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
