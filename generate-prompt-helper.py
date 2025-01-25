#!/usr/bin/env python3
"""
A script to generate an HTML file containing prompt templates and text/file inputs,
based on a given Excel or CSV file.

Usage:
  generate_prompt_html.py [options] INPUT_FILE

Example:
  generate_prompt_html.py sample.xlsx
  generate_prompt_html.py sample.csv -o output.html

Author:
  (Your Name)
"""

import argparse
import os
import sys
import pandas as pd


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments using argparse.

    Returns:
        argparse.Namespace: Parsed arguments with the following attributes:
            input_file (str): Path to the input Excel or CSV file.
            output_file (str): Path to the output HTML file (optional).
    """
    parser = argparse.ArgumentParser(
        description="Generate an HTML file for prompt templates from an Excel/CSV file."
    )

    parser.add_argument(
        "input_file",
        help="Path to the input Excel (.xlsx, .xls) or CSV (.csv) file."
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        help="Path to the output HTML file. If not specified, uses the same base name as INPUT_FILE with .html extension."
    )

    return parser.parse_args()


def confirm_overwrite(filepath: str) -> bool:
    """
    Ask user to confirm overwrite if a file already exists.

    Args:
        filepath (str): The path to the file to check.

    Returns:
        bool: True if user confirmed overwrite, False otherwise.
    """
    if not os.path.isfile(filepath):
        return True  # ファイルが存在しなければ、特に確認せずOK

    # ファイルが既に存在するときに尋ねる
    answer = input(f"File '{filepath}' already exists. Overwrite? (y)es/(n)o [default: no]: ").strip().lower()
    if answer == "y" or answer == "yes":
        return True
    return False


def generate_html(prompt_format: str, text_columns: list[str]) -> str:
    """
    Generate an HTML string that includes:
      - A fixed template container showing 'Prompt_Format'.
      - Textareas and file inputs for each column in text_columns.

    Args:
        prompt_format (str): The main prompt format string (from "Prompt_Format" column).
        text_columns (list[str]): A list of column names to create text/file input pairs.

    Returns:
        str: The complete HTML content as a string.
    """

    # --- 1) ヘッダーと基本構造 ---
    html_header = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <title>プロンプト作成補助ツール</title>
  <style>
    body {
      max-width: 800px;
      margin: 0 auto;
      font-family: sans-serif;
    }
    h1 {
      margin-top: 1em;
      font-size: 2em;
    }
    textarea {
      width: 100%;
      height: 100px;
      margin-bottom: 1em;
    }
    button {
      padding: 0.5em 1em;
      cursor: pointer;
    }
    .template-container {
      background-color: #f8f8f8;
      padding: 1em;
      margin-bottom: 1em;
      border: 1px solid #ddd;
    }
    .result-box {
      white-space: pre-wrap;  /* 改行やスペースをそのまま表示 */
      border: 1px solid #ddd;
      padding: 1em;
      margin-top: 1em;
    }
    .file-input-box {
      margin-bottom: 1em;
    }
  </style>
</head>
<body>
"""

    # --- 2) テンプレート案内文（"Prompt_Format"列の内容を使用） ---
    # 改行を <br> に変換して見やすくする場合は以下のようにしてもOK:
    # prompt_format_html = prompt_format.replace('\n', '<br>\n')

    template_container = f"""<h1>プロンプト作成補助ツール</h1>
<div class="template-container">
  {prompt_format}
</div>
"""

    # --- 3) テキストボックスとファイルアップロード欄を動的に生成 ---
    textareas_html = ""
    for col in text_columns:
        textareas_html += f"""<h2>{col}</h2>
<textarea id="{col}Input" placeholder="{col}"></textarea>
<div class="file-input-box">
  <input type="file" id="{col}FileInput" />
</div>
"""

    # --- 4) 「プロンプト作成 & クリップボードにコピー」ボタン、出力表示欄 ---
    #   JavaScript部品を後で差し込む
    generate_button_html = """
<button id="generateButton">プロンプト作成 &amp; クリップボードにコピー</button>

<div class="result-box" id="resultPrompt" hidden></div>
"""

    # --- 5) JavaScript部分を動的に生成 ---
    # JavaScriptの中で text_columns の配列を使ってeventListener等を作る
    # 1) ファイル選択 → FileReaderで textarea に書き込み
    # 2) ボタン押下 → 全 textarea の内容を取得 → promptTemplate を作成 → クリップボード書き込み

    # 各ファイル入力のeventListenerを生成
    file_reader_js = ""
    for col in text_columns:
        file_reader_js += f"""
  document.getElementById("{col}FileInput").addEventListener("change", (event) => {{
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {{
      document.getElementById("{col}Input").value = e.target.result;
    }};
    reader.readAsText(file);
  }});
"""

    # ボタンクリック時の動作
    # (1) 各 TextXInput を取得
    # (2) promptTemplate を作成
    # (3) クリップボードコピー & 画面表示
    cols_for_js_collection = "\n".join([
        f'      const {col}Value = document.getElementById("{col}Input").value;' for col in text_columns
    ])

    # 柔軟なプロンプトの作り方の一例:
    # - まず "Prompt_Format" を表示
    # - その後に各 Text 列をまとめて追記
    lines_for_prompt_template = '\n'.join([
        f'  promptTemplate += "\\n~~~ {col}\\n" + {col}Value + "\\n~~~\\n";'
        for col in text_columns
    ])

    js_script = f"""
<script>
  // --- ファイル読み込み処理 ---
  {file_reader_js}

  // --- プロンプト生成ボタン ---
  document.getElementById("generateButton").addEventListener("click", () => {{
{cols_for_js_collection}

    let promptTemplate = `{prompt_format}\\n\\n`;
{lines_for_prompt_template}

    // クリップボードにコピー
    navigator.clipboard.writeText(promptTemplate)
      .then(() => {{
        alert("クリップボードにコピーしました！");
      }})
      .catch((err) => {{
        alert("コピーに失敗しました: " + err);
      }});

    // 画面表示
    const resultPromptDiv = document.getElementById("resultPrompt");
    resultPromptDiv.hidden = false;
    resultPromptDiv.textContent = promptTemplate;
  }});
</script>
"""

    # --- 6) HTMLを結合 ---
    html_footer = """
</body>
</html>
"""
    html_full = (
        html_header +
        template_container +
        textareas_html +
        generate_button_html +
        js_script +
        html_footer
    )

    return html_full


def main() -> None:
    """
    Main function that:
      1) Parses command-line arguments.
      2) Reads the Excel/CSV file using Pandas.
      3) Extracts 'Prompt_Format' and the rest of the text columns.
      4) Generates an HTML string and writes it to the specified output file (with overwrite confirmation).
    """
    args = parse_args()

    input_file = args.input_file
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    # 出力ファイル名のデフォルト設定
    if args.output_file:
        output_file = args.output_file
    else:
        base = os.path.splitext(os.path.basename(input_file))[0]
        output_file = base + ".html"

    # 拡張子で読み分け（.csv または .xls / .xlsx）
    ext = os.path.splitext(input_file)[1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(input_file)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(input_file)
        else:
            print(f"Error: Unsupported file extension '{ext}'. Please provide .csv or .xlsx/.xls.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to read file '{input_file}': {e}")
        sys.exit(1)

    if df.empty:
        print("Error: The input file is empty or could not be read.")
        sys.exit(1)

    # 「Prompt_Format」列があるか確認
    if "Prompt_Format" not in df.columns:
        print("Error: The file must contain a 'Prompt_Format' column.")
        sys.exit(1)

    row = df.iloc[0]
    prompt_format = str(row["Prompt_Format"])

    text_columns = [str(row[col]) for col in df.columns if col != "Prompt_Format"]

    # HTML生成
    html_content = generate_html(prompt_format, text_columns)

    # 上書き確認
    if not confirm_overwrite(output_file):
        print("Canceled. No file was written.")
        sys.exit(0)

    # 書き込み
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML file generated: {output_file}")
    except Exception as e:
        print(f"Error: Could not write to '{output_file}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
