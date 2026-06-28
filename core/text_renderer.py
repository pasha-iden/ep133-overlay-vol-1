from data.text_script import TEXT_BLOCKS
from data import config


class TextRenderer:
    def __init__(self, font):
        self.font = font

    def get_active_text(self, current_time):
        for block in TEXT_BLOCKS:
            if block["start"] <= current_time <= block["end"]:
                text = block["text"]

                if block.get("typing_effect", False):
                    # Если задана длительность — используем её
                    if "typing_duration" in block:
                        typing_duration = block["typing_duration"]
                    else:
                        # Иначе вычисляем из скорости
                        char_count = len(text)
                        typing_duration = char_count / (config.TYPING_SPEED / 60)

                    elapsed = current_time - block["start"]

                    if elapsed < typing_duration:
                        progress = elapsed / typing_duration
                        char_count = int(len(text) * progress)
                        if char_count < len(text):
                            text = text[:char_count]

                return text

        return None