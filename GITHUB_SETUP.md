# GitHub 上传说明

当前项目已经适合接入 Git 版本管理，但这个环境里暂时没有可用的 `git` 命令，所以还不能直接帮你完成 `commit` 和 `push`。

## 当前已准备好的内容

1. 已添加 `.gitignore`
2. 已保留项目内的业务版本存储能力
3. 已添加双击打开 VSCode 的文件 `open_in_vscode.bat`

## 你安装 Git 之后，可以按这个顺序执行

在项目目录打开终端后运行：

```bash
git init
git add .
git commit -m "Initial commit: mapping sql agent"
git branch -M main
git remote add origin <你的 GitHub 仓库地址>
git push -u origin main
```

## 推荐的 GitHub 仓库名

```text
mapping-sql-agent
```

## 建议的后续版本习惯

每次做一个阶段性能力后执行：

```bash
git add .
git commit -m "feat: add xxx"
git push
```

这样你以后就能通过 GitHub 和本地 Git 一起做版本回撤。
