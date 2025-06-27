import os
import csv
from pathlib import Path
import argparse

HEADER = [
    "ID", "duration",
    "mix_wav", "mix_wav_format", "mix_wav_opts",
    "s1_wav", "s1_wav_format", "s1_wav_opts",
    "s2_wav", "s2_wav_format", "s2_wav_opts",
    "s3_wav", "s3_wav_format", "s3_wav_opts",
    "s4_wav", "s4_wav_format", "s4_wav_opts",
]

def find_mixture_and_sources_v2(root: Path):
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirpath = Path(dirpath)
        # 如果包含 array 和 source 两个子目录
        if "array" in dirnames and "source" in dirnames:
            array_dir = dirpath / "array"
            source_dir = dirpath / "source"

            # 检查至少有 source-1.wav 存在
            if not (source_dir / "source-1.wav").exists():
                continue

            # 获取 source 路径（缺失则填空）
            s_paths = {}
            for i in range(1, 5):
                fp = source_dir / f"source-{i}.wav"
                s_paths[i] = str(fp.resolve()) if fp.exists() else ""

            # 遍历 array 下所有 mixture-*.wav
            for mix in sorted(array_dir.glob("mixture-*.wav")):
                row = [
                    None, 1,  # ID, duration
                    str(mix.resolve()), "wav", "",

                    s_paths[1], "wav", "",
                    s_paths[2], "wav", "",
                    s_paths[3], "wav", "",
                    s_paths[4], "wav", "",
                ]
                rows.append(row)
    return rows

def build_csv(root_dir: Path, csv_out: Path):
    rows = find_mixture_and_sources_v2(root_dir)

    for idx, row in enumerate(rows):
        row[0] = idx  # 填写 ID

    csv_out.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)

    print(f"✅ 已生成 {len(rows)} 行到 {csv_out}")

def main():
    parser = argparse.ArgumentParser() # /work105/youzhenghai/data/data-new
    parser.add_argument("audio_root", help="音频数据的根目录")
    parser.add_argument("-o", "--out_csv", default="mixture_metadata.csv",
                        help="输出 CSV 路径，默认 mixture_metadata.csv")
    args = parser.parse_args()

    build_csv(Path(args.audio_root), Path(args.out_csv))

if __name__ == "__main__":
    main()
