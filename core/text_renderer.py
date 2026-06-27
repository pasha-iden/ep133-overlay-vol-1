from data.text_script import TEXT_BLOCKS


class TextRenderer:
    def __init__(self, font):
        self.font = font

    def get_active_text(self, current_time):
        """
        Возвращает активный текстовый блок и прогресс печатания
        """
        for block in TEXT_BLOCKS:
            if block["start"] <= current_time <= block["end"]:
                text = block["text"]

                # Эффект печатания
                if block.get("typing_effect", False):
                    typing_duration = block.get("typing_duration", 1.0)
                    elapsed = current_time - block["start"]

                    if elapsed < typing_duration:
                        progress = elapsed / typing_duration
                        # Обрезаем текст по символам
                        char_count = int(len(text) * progress)
                        if char_count < len(text):
                            text = text[:char_count]

                return text

        return None