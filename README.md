# Nobu C. Shirai's GitHub Pages Repository

このリポジトリは、生成AIを活用したツールのコレクションを含むWebサイトです。各ツールは使いやすさを重視して設計されており、特に議事録作成やプロンプト生成を効率化することを目的としています。

## ファイル構成
### `index.html`
トップページとして機能し、リポジトリ内のツール一覧を表示します。各ツールの概要とリンクが記載されています。

### `prompt-helper-tool.html`
- **概要**: 
  指定された議事録フォーマットとトランスクリプトを基に、議事録を整形するためのプロンプトを生成します。
- **主な機能**:
  - フォーマットおよびトランスクリプトを直接入力またはファイルから読み込み可能。
  - 自動的にプロンプトを生成し、クリップボードにコピー。
  - 生成されたプロンプトを画面に表示。

### `generate-prompt-helper.html`
- **概要**:
  CSVまたはExcelファイルから動的にHTMLテンプレートを生成し、カスタマイズ可能なプロンプト作成ツールを提供します。
- **主な機能**:
  - CSV/Excelファイルをアップロードし、動的な入力フォームを生成。
  - 各入力欄に適切な値を入力してプロンプトを生成。
  - クリップボードへのコピー機能付き。

### `prompt-helper-tool.csv`
サンプルデータとして提供されるCSVファイルです。`generate-prompt-helper.html` にアップロードすることで、`prompt-helper-tool.html` を動的に生成する例を示します。

## ツール一覧
### [生成AI活用ツール一覧](index.html)
以下のツールが含まれています：

1. [プロンプト作成補助ツール](prompt-helper-tool.html)
   - トランスクリプトや議事録フォーマットから、整形された議事録を作成するプロンプトを生成。
2. [CSV/ExcelからHTML生成ツール](generate-prompt-helper.html)
   - CSVやExcelファイルを利用してカスタマイズ可能なプロンプト作成ツールを生成。

## 使用方法
1. **ローカルでテスト**:
   - このリポジトリをクローンまたはダウンロードします。
   - ファイルをローカルのブラウザで開くことで各ツールを試せます。
   - 例: `index.html` をブラウザで開くとツールの概要ページが表示されます。

2. **GitHub Pagesでホスト**:
   - このリポジトリをGitHub Pagesでホストし、URLにアクセスすることで利用可能になります。
   - 例: `https://nobucshirai.github.io/`

## ライセンス
このリポジトリは [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.ja) ライセンスの下で公開されています。

- **概要**:
  - 商用利用、改変、再配布が可能です。
  - 利用する際は、適切なクレジット（著作者名やライセンスリンクなど）を表示してください。
- 詳細は [ライセンスの公式ページ](https://creativecommons.org/licenses/by/4.0/deed.ja) をご覧ください。

---
© 2025 Nobu C. Shirai
