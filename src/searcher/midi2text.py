import mido
from typing import List, Dict, Any


def read_midi_text_messages(midi_file_path: str) -> List[Dict[str, Any]]:
    """
    读取MIDI文件中的文本消息（注释等）

    Args:
        midi_file_path: MIDI文件的路径

    Returns:
        包含所有文本消息的列表，每个消息是一个字典，包含：
        - type: 消息类型（text, lyric, marker, cue_point等）
        - text: 文本内容
        - track: 所在轨道索引
        - time: 消息在轨道中的时间位置
    """
    text_messages = []

    try:
        # 加载MIDI文件
        midi_file = mido.MidiFile(midi_file_path)

        # 遍历所有轨道
        for track_idx, track in enumerate(midi_file.tracks):
            # 遍历轨道中的所有消息
            for msg in track:
                # 检查是否为文本相关消息
                if msg.type in ['text', 'lyrics', 'marker', 'cue_point']:
                    text_messages.append({
                        'type': msg.type,
                        'text': msg.text,
                        'track': track_idx,
                        'time': msg.time
                    })

    except FileNotFoundError:
        print(f"错误: 找不到MIDI文件 {midi_file_path}")
    except Exception as e:
        print(f"读取MIDI文件时出错: {e}")

    return text_messages


def read_midi_metadata(midi_file_path: str) -> Dict[str, Any]:
    """
    读取MIDI文件的元数据

    Args:
        midi_file_path: MIDI文件的路径

    Returns:
        包含MIDI文件元数据的字典
    """
    metadata = {
        'file_path': midi_file_path,
        'text_messages': [],
        'tracks_count': 0,
        'ticks_per_beat': 0,
        'length_seconds': 0
    }

    try:
        midi_file = mido.MidiFile(midi_file_path)

        metadata['tracks_count'] = len(midi_file.tracks)
        metadata['ticks_per_beat'] = midi_file.ticks_per_beat

        # 获取所有文本消息
        metadata['text_messages'] = read_midi_text_messages(midi_file_path)

        # 计算总时长（秒）
        metadata['length_seconds'] = midi_file.length

    except FileNotFoundError:
        print(f"错误: 找不到MIDI文件 {midi_file_path}")
    except Exception as e:
        print(f"读取MIDI文件元数据时出错: {e}")

    return metadata
