import pygame
import sys
import os
import cv2
import numpy as np
import subprocess
from moviepy import VideoFileClip
from data import config
from data import sequence
from core.sequence_renderer import SequenceRenderer
from core.sequence_loader import SequenceLoader
from core.text_renderer import TextRenderer
from core.ascii_animation import render_ascii_animation
from core.final_logs import render_final_logs


def find_video_file():
    input_folder = "video/input"
    if not os.path.exists(input_folder):
        print(f"Папка {input_folder} не существует")
        return None
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']
    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in video_extensions:
                print(f"Найден видеофайл: {file}")
                return file_path
    print("Видеофайл не найден в папке video/input")
    return None


def get_background_frame_by_frame(cap, frame_number, target_width, target_height):
    if cap is None:
        return None
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (target_width, target_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        frame = np.rot90(frame)
        return pygame.surfarray.make_surface(frame)
    return None


def extract_audio_with_moviepy(video_path, audio_output_path):
    try:
        print(f"Извлекаем аудио из видео...")
        video = VideoFileClip(video_path)
        if video.audio is not None:
            video.audio.write_audiofile(audio_output_path)
            video.close()
            print(f"Аудио успешно извлечено: {audio_output_path}")
            return True
        else:
            print("В видео отсутствует аудиодорожка")
            video.close()
            return False
    except Exception as e:
        print(f"Ошибка при извлечении аудио: {e}")
        return False


def scale_coordinates(value, from_size, to_size):
    return int(value * to_size / from_size)


def add_audio_with_ffmpeg_fallback(video_path, audio_path, output_path):
    ffmpeg_paths = [
        'ffmpeg',
        os.path.join(os.path.dirname(__file__), 'ffmpeg.exe'),
        r'C:\ffmpeg\bin\ffmpeg.exe',
    ]

    ffmpeg_cmd = None
    for path in ffmpeg_paths:
        if os.path.exists(path) or path == 'ffmpeg':
            try:
                subprocess.run([path, '-version'], capture_output=True, check=False)
                ffmpeg_cmd = path
                break
            except:
                continue

    if ffmpeg_cmd is None:
        try:
            from portable_ffmpeg import get_ffmpeg
            ffmpeg_cmd, _ = get_ffmpeg()
            print(f"FFmpeg загружен через portable_ffmpeg")
        except:
            print("FFmpeg не найден")
            return False

    try:
        cmd = [
            ffmpeg_cmd, '-i', video_path, '-i', audio_path,
            '-c:v', 'copy', '-c:a', 'aac',
            output_path, '-y'
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"Готовое видео со звуком: {output_path}")
        return True
    except Exception as e:
        print(f"Ошибка при добавлении аудио: {e}")
        return False


def main():
    pygame.init()

    video_path = find_video_file()
    cap = None
    audio_path = "video/temp_audio.mp3"

    total_frames = 0
    fps = 30

    if video_path is not None:
        print(f"Загружаем видео: {video_path}")
        cap = cv2.VideoCapture(video_path)
        video_orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Исходное видео: {video_orig_width}x{video_orig_height}, FPS: {fps}, Кадров: {total_frames}")

        if os.path.exists(audio_path):
            os.remove(audio_path)
        extract_audio_with_moviepy(video_path, audio_path)
    else:
        print(f"Видео не найдено, используем чёрный фон")
        total_frames = 60 * 30

    # ========== РЕЖИМ ЗАПИСИ ==========
    if config.RENDER_MODE:
        screen_width = config.RECORD_WIDTH
        screen_height = config.RECORD_HEIGHT

        scale_factor = screen_width / config.PREVIEW_WIDTH

        window_x = scale_coordinates(config.WINDOW_X, config.PREVIEW_WIDTH, screen_width)
        window_y = scale_coordinates(config.WINDOW_Y, config.PREVIEW_HEIGHT, screen_height)
        window_width = scale_coordinates(config.WINDOW_WIDTH, config.PREVIEW_WIDTH, screen_width)
        window_height = scale_coordinates(config.WINDOW_HEIGHT, config.PREVIEW_HEIGHT, screen_height)

        text_x = scale_coordinates(config.TEXT_X, config.PREVIEW_WIDTH, screen_width)
        text_y = scale_coordinates(config.TEXT_Y, config.PREVIEW_HEIGHT, screen_height)
        sequence_x = scale_coordinates(config.SEQUENCE_X, config.PREVIEW_WIDTH, screen_width)
        sequence_y = scale_coordinates(config.SEQUENCE_Y, config.PREVIEW_HEIGHT, screen_height)

        ascii_offset_x = scale_coordinates(20, config.PREVIEW_WIDTH, screen_width)
        ascii_offset_y = scale_coordinates(20, config.PREVIEW_HEIGHT, screen_height)
        ascii_logs_offset = scale_coordinates(40, config.PREVIEW_HEIGHT, screen_height)

        scaled_square_width = int(config.SQUARE_WIDTH * scale_factor)
        scaled_square_height = int(config.SQUARE_HEIGHT * scale_factor)
        scaled_square_offset_x = int(config.SQUARE_OFFSET_X * scale_factor)
        scaled_square_offset_y = int(config.SQUARE_OFFSET_Y * scale_factor)

        scaled_text_size = int(config.FONT_SIZE_TEXT * scale_factor)
        scaled_sequence_size = int(config.FONT_SIZE_SEQUENCE * scale_factor)
        scaled_ascii_font_size = int(config.FONT_SIZE_SEQUENCE * scale_factor)

        print(f"Масштаб: {scale_factor}")
        print(f"Оверлей на экране: ({window_x}, {window_y}) {window_width}x{window_height}")
        print(f"Отступы внутри оверлея: sequence=({sequence_x}, {sequence_y}), text=({text_x}, {text_y})")
        print(f"Отступы ASCII: ({ascii_offset_x}, {ascii_offset_y})")

        temp_output_path = "video/output/temp_result.mp4"
        os.makedirs("video/output", exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(temp_output_path, fourcc, int(fps), (screen_width, screen_height))
        print(f"Режим: ЗАПИСЬ. Размер: {screen_width}x{screen_height}")

        screen = pygame.Surface((screen_width, screen_height))

        text_font = pygame.font.SysFont(config.FONT_NAME, scaled_text_size)
        sequence_font = pygame.font.SysFont(config.FONT_NAME, scaled_sequence_size)

        original_square_width = config.SQUARE_WIDTH
        original_square_height = config.SQUARE_HEIGHT
        original_square_offset_x = config.SQUARE_OFFSET_X
        original_square_offset_y = config.SQUARE_OFFSET_Y

        config.SQUARE_WIDTH = scaled_square_width
        config.SQUARE_HEIGHT = scaled_square_height
        config.SQUARE_OFFSET_X = scaled_square_offset_x
        config.SQUARE_OFFSET_Y = scaled_square_offset_y

        renderer = SequenceRenderer(sequence_font)
        loader = SequenceLoader(sequence_font)
        text_renderer = TextRenderer(text_font)
        lines = sequence.SEQUENCE

        frame_number = 0

        try:
            while frame_number < total_frames:
                current_time = frame_number / fps

                print(f"\rКадр: {frame_number + 1}/{total_frames} | Время: {current_time:.2f} сек", end="", flush=True)

                frame_surface = get_background_frame_by_frame(cap, frame_number, screen_width, screen_height)
                if frame_surface is not None:
                    screen.blit(frame_surface, (0, 0))
                else:
                    screen.fill((0, 0, 0))

                window_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

                ascii_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
                ascii_active = render_ascii_animation(
                    ascii_surface, current_time, window_width, window_height,
                    scaled_ascii_font_size, ascii_offset_x, ascii_offset_y, ascii_logs_offset
                )
                if ascii_active:
                    window_surface.blit(ascii_surface, (0, 0))

                # ===== ПРОГРУЖАЕМАЯ СЕКВЕНЦИЯ — ТАК ЖЕ, КАК ГОТОВАЯ (ТОЛЬКО SEQUENCE_SCALE) =====
                loading_surface = loader.render_loading_sequence(
                    lines, current_time, sequence_x, sequence_y, config.SEQUENCE_SCALE
                )
                if loading_surface is not None and isinstance(loading_surface, pygame.Surface):
                    window_surface.blit(loading_surface, (sequence_x, sequence_y))

                final_logs_active = render_final_logs(
                    screen, current_time, window_x, window_y, window_width, window_height,
                    scaled_ascii_font_size, ascii_offset_x, ascii_offset_y
                )

                if not final_logs_active:
                    if not ascii_active:
                        pygame.draw.rect(window_surface, config.BACKGROUND_COLOR, window_surface.get_rect())

                        active_text = text_renderer.get_active_text(current_time)
                        if active_text:
                            text_lines = active_text.split('\n')
                            y_offset = text_y
                            for text_line in text_lines:
                                text_surface = text_font.render(text_line, True, config.COLOR_DARK)
                                window_surface.blit(text_surface, (text_x, y_offset))
                                y_offset += text_surface.get_height() + 5

                        # ===== ГОТОВАЯ СЕКВЕНЦИЯ — ТОЛЬКО SEQUENCE_SCALE =====
                        sequence_surface = renderer.render_sequence(lines, current_time)
                        if sequence_surface is not None:
                            window_surface.blit(sequence_surface, (sequence_x, sequence_y))

                if current_time < config.WINDOW_APPEAR_TIME:
                    pass
                else:
                    elapsed = current_time - config.WINDOW_APPEAR_TIME
                    progress = min(elapsed / config.ANIMATION_DURATION, 1.0)
                    current_height = int(window_height * progress)

                    if current_height > 0:
                        clip_rect = pygame.Rect(0, 0, window_width, current_height)
                        screen.blit(window_surface, (window_x, window_y), clip_rect)

                frame_data = pygame.surfarray.array3d(screen)
                frame_data = np.rot90(frame_data)
                frame_data = cv2.flip(frame_data, 0)
                frame_data = cv2.cvtColor(frame_data, cv2.COLOR_RGB2BGR)
                video_writer.write(frame_data)

                frame_number += 1

        except KeyboardInterrupt:
            print(f"\n\nПрерывание пользователя на кадре {frame_number}")
        except Exception as e:
            print(f"\n\nОшибка: {e}")
        finally:
            config.SQUARE_WIDTH = original_square_width
            config.SQUARE_HEIGHT = original_square_height
            config.SQUARE_OFFSET_X = original_square_offset_x
            config.SQUARE_OFFSET_Y = original_square_offset_y

            video_writer.release()
            print(f"\nВременное видео без звука: {temp_output_path}, кадров: {frame_number}")

            if frame_number > 0 and audio_path and os.path.exists(audio_path) and video_path is not None:
                final_output_path = "video/output/result.mp4"
                print("Добавляем аудио...")
                if add_audio_with_ffmpeg_fallback(temp_output_path, audio_path, final_output_path):
                    if os.path.exists(temp_output_path):
                        os.remove(temp_output_path)
                    print(f"✅ Готовый файл со звуком: {final_output_path}")
                else:
                    print(f"❌ Видео без звука: {temp_output_path}")
            else:
                final_output_path = "video/output/result.mp4"
                if os.path.exists(final_output_path):
                    os.remove(final_output_path)
                os.rename(temp_output_path, final_output_path)
                print(f"❌ Видео без звука: {final_output_path}")

            if cap is not None:
                cap.release()

            print("Завершено")
            pygame.quit()
            sys.exit()

    # ========== РЕЖИМ ПРЕДПРОСМОТРА ==========
    else:
        screen_width = config.PREVIEW_WIDTH
        screen_height = config.PREVIEW_HEIGHT

        print(f"Режим: ПРЕДПРОСМОТР. Размер: {screen_width}x{screen_height}")

        if video_path is not None:
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            print("Звук воспроизводится")

        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("PREVIEW")

        text_font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_TEXT)
        sequence_font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE_SEQUENCE)

        renderer = SequenceRenderer(sequence_font)
        loader = SequenceLoader(sequence_font)
        text_renderer = TextRenderer(text_font)
        lines = sequence.SEQUENCE

        window_x = config.WINDOW_X
        window_y = config.WINDOW_Y
        window_width = config.WINDOW_WIDTH
        window_height = config.WINDOW_HEIGHT
        text_x = config.TEXT_X
        text_y = config.TEXT_Y
        sequence_x = config.SEQUENCE_X
        sequence_y = config.SEQUENCE_Y

        ascii_offset_x = 20
        ascii_offset_y = 20
        ascii_logs_offset = 40

        print(f"Оверлей: ({window_x}, {window_y}) {window_width}x{window_height}")
        print(f"Отступы: text=({text_x}, {text_y}), sequence=({sequence_x}, {sequence_y})")

        clock = pygame.time.Clock()
        running = True
        start_time = pygame.time.get_ticks() / 1000.0

        while running:
            current_time = (pygame.time.get_ticks() / 1000.0) - start_time
            print(f"\rВремя: {current_time:.2f} сек", end="", flush=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if current_time > (total_frames / fps):
                running = False

            frame_surface = get_background_frame_by_frame(cap, int(current_time * fps), screen_width, screen_height)
            if frame_surface is not None:
                screen.blit(frame_surface, (0, 0))
            else:
                screen.fill((0, 0, 0))

            window_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

            ascii_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            ascii_active = render_ascii_animation(
                ascii_surface, current_time, window_width, window_height,
                config.FONT_SIZE_SEQUENCE, ascii_offset_x, ascii_offset_y, ascii_logs_offset
            )
            if ascii_active:
                window_surface.blit(ascii_surface, (0, 0))

            # ===== ПРОГРУЖАЕМАЯ СЕКВЕНЦИЯ — ТАК ЖЕ, КАК ГОТОВАЯ =====
            loading_surface = loader.render_loading_sequence(
                lines, current_time, sequence_x, sequence_y, config.SEQUENCE_SCALE
            )
            if loading_surface is not None and isinstance(loading_surface, pygame.Surface):
                window_surface.blit(loading_surface, (sequence_x, sequence_y))

            final_logs_active = render_final_logs(
                screen, current_time, window_x, window_y, window_width, window_height,
                config.FONT_SIZE_SEQUENCE, ascii_offset_x, ascii_offset_y
            )

            if not final_logs_active:
                if not ascii_active:
                    pygame.draw.rect(window_surface, config.BACKGROUND_COLOR, window_surface.get_rect())

                    active_text = text_renderer.get_active_text(current_time)
                    if active_text:
                        text_lines = active_text.split('\n')
                        y_offset = text_y
                        for text_line in text_lines:
                            text_surface = text_font.render(text_line, True, config.COLOR_DARK)
                            window_surface.blit(text_surface, (text_x, y_offset))
                            y_offset += text_surface.get_height() + 5

                    # ===== ГОТОВАЯ СЕКВЕНЦИЯ =====
                    sequence_surface = renderer.render_sequence(lines, current_time)
                    if sequence_surface is not None:
                        window_surface.blit(sequence_surface, (sequence_x, sequence_y))

            if current_time < config.WINDOW_APPEAR_TIME:
                pass
            else:
                elapsed = current_time - config.WINDOW_APPEAR_TIME
                progress = min(elapsed / config.ANIMATION_DURATION, 1.0)
                current_height = int(window_height * progress)

                if current_height > 0:
                    clip_rect = pygame.Rect(0, 0, window_width, current_height)
                    screen.blit(window_surface, (window_x, window_y), clip_rect)

            pygame.display.flip()
            clock.tick(60)

        if cap is not None:
            cap.release()
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()