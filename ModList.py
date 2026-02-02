import os
import re

MOD_FOLDER_PATH = r'.'
OUTPUT_FILE_NAME = 'mod_list_final.txt'#输出的文档和代码文件在同一目录下

def get_clean_name(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'^\[.*?\]', '', name)
    name = re.sub(r'^\(.*?\)', '', name)
    name = re.sub(r'^（.*?）', '', name)
    name = re.sub(r'[\u4e00-\u9fa5]', '', name)
    name = name.strip()

    split_pattern = r'(?i)[-_ ]+(fabric|forge|quilt|neoforge|mc|all|v?\d+\.\d+|v?\d)'

    parts = re.split(split_pattern, name, maxsplit=1)

    # 如果切分成功，取第一部分
    if len(parts) > 0:
        result = parts[0].strip()
        if not result:
            return name
        return result

    return name


def main():
    if not os.path.exists(MOD_FOLDER_PATH):
        print(f"错误：找不到路径！")
        return

    valid_mod_files = []
    clean_names = []
    skipped_items = []

    print(f"正在扫描: {os.path.abspath(MOD_FOLDER_PATH)} ...")

    try:
        all_items = os.listdir(MOD_FOLDER_PATH)
        total_items = len(all_items)

        for item in all_items:
            if item == OUTPUT_FILE_NAME or item.endswith('.py') or item.endswith('.txt'):
                skipped_items.append(f"[忽略文件] {item}")
                continue

            if os.path.isdir(os.path.join(MOD_FOLDER_PATH, item)):
                skipped_items.append(f"[文件夹] {item}")
                continue

            if not (item.endswith('.jar') or item.endswith('.zip') or item.endswith('.litemod')):
                skipped_items.append(f"[非Mod] {item}")
                continue

            clean = get_clean_name(item)

            if clean:
                valid_mod_files.append(item)
                clean_names.append(clean)
            else:
                skipped_items.append(f"[解析为空] {item}")

    except Exception as e:
        print(f"出错: {e}")
        import traceback
        traceback.print_exc()
        return

    unique_names = sorted(list(set(clean_names)), key=lambda x: x.lower())

    with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as f:
        f.write(f"【统计】总项目: {total_items} | 提取Mod: {len(unique_names)} | 跳过/其他: {len(skipped_items)}\n")
        f.write("=" * 40 + "\n\n")

        f.write("【提取结果】\n")
        for name in unique_names:
            f.write(name + "\n")

        f.write("\n" + "=" * 40 + "\n")
        f.write("【失败/跳过列表 (检查是否有误判)】\n")
        for item in skipped_items:
            f.write(item + "\n")

        f.write("\n" + "=" * 40 + "\n")
        f.write("【对照表 (用于核对正则效果)】\n")
        for i in range(len(valid_mod_files)):
            f.write(f"{valid_mod_files[i]}\n -> {clean_names[i]}\n\n")

    print(f"完成！请查看 {OUTPUT_FILE_NAME}")
    input("按回车键退出...")


if __name__ == '__main__':
    main()