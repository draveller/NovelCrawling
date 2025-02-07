import json
import os
import re

def chinese_to_number(chinese_num):
    chinese_num_dict = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    if chinese_num in chinese_num_dict:
        return chinese_num_dict[chinese_num]
    else:
        # 处理十以上的数字
        match = re.match(r'十([一二三四五六七八九])?', chinese_num)
        if match:
            if match.group(1):
                return 10 + chinese_num_dict[match.group(1)]
            else:
                return 10
        return 0

def extract_chapter_number(chapter):
    # 匹配章节编号，例如 "第一章", "第十二章", "前言", "尾声"
    match = re.match(r'(第[一二三四五六七八九十百千]+章)|前言|尾声', chapter)
    if match:
        chapter_num = match.group(0)
        if chapter_num.startswith('第'):
            # 提取中文数字并转换为阿拉伯数字
            num = re.findall(r'[一二三四五六七八九十百千]+', chapter_num)[0]
            return chinese_to_number(num)
        elif chapter_num == '前言':
            return -1  # 将前言放在最前面
        elif chapter_num == '尾声':
            return float('inf')  # 将尾声放在最后面
    return 0  # 其他情况按0处理

def process_jsonl_to_txt(jsonl_file_path, output_directory):
    books = {}
    # output_directory目录不存在则创建:
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    with open(jsonl_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            novel = data['novel']
            chapter = data['chapter']
            content = data['content']

            content = content.replace('\r\n', '\n').replace('\t', '    ')

            if novel not in books:
                books[novel] = []

            books[novel].append((chapter, content))

    for novel, chapters in books.items():
        # 根据章节编号排序
        sorted_chapters = sorted(chapters, key=lambda x: (extract_chapter_number(x[0]), x[0]))

        output_file_path = f"{output_directory}/{novel}.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for chapter, content in sorted_chapters:
                output_file.write(f"{chapter}\n\n{content}\n\n")

process_jsonl_to_txt(
    r'D:\my-work-space\NovelCrawling\novel.jsonl',
    r'D:\my-work-space\NovelCrawling\output')
